#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

import datetime
from decimal import Decimal
from decimal import InvalidOperation
import logging
import pytz

from openstack_auth import utils as auth_utils

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import constants

LOG = logging.getLogger(__name__)
CURRENCY_FORMAT = getattr(settings, 'CURRENCY_FORMAT', '{0:,.2f}')
CURRENCY_UNIT = getattr(settings, 'CURRENCY_UNIT', 'USD')
NONE_PRICE_STRING = "-"

DISPLAY_DATE_FORMAT = '%Y-%m-%d'
DISPLAY_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
INTERNAL_UTC_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

# TODO(hiramatsu):In the future, and transfer a function to
#                 the base class of workflow engine.


def allowed_grant_role(request, status_name, workflow):
    """Check a user have grant role.
    :param request: HTTP Request.
    :param status_name: Status NAME.
        if a name is error, return False.
    :param workflow: One workflow row data.
    """
    if status_name == _('Error'):
        return False

    all_status = workflow["status_detail"]

    if not all_status:
        return False

    next_status = get_next_status_list(request, all_status)

    if not next_status:
        return False

    return True


def get_next_status_list(request, all_status):
    """Get next status list from all status by user has role
    :param all_status: All status list
    """
    user = auth_utils.get_user(request)
    user_roles = [role['name'] for role in user.roles]
    next_status_list = []

    for status in all_status.get('next_status', []):
        grant_role = status.get('grant_role', [])
        if not isinstance(grant_role, list):
            grant_role = [grant_role]

        for role in grant_role:
            if role in user_roles:
                next_status_list.append(status)
                break

    return next_status_list


def get_ticket_template_contents(request, ticket_template_id):
    """Get a template contents of a ticket template.
    :param request: request of view
    :param ticket_template_id: target uuid from a ticket template
    """
    tickettemplate = ticket_api.\
        tickettemplates_get(request, ticket_template_id)

    return tickettemplate.template_contents


def get_language_name(request, language_name):
    languageCode = request.LANGUAGE_CODE

    if not language_name:
        return ''

    # 'Default' is for workflow format v1.0 and it's deprecated now.
    # Currently this key is changed from 'Default' to 'default'.
    if languageCode in language_name:
        return language_name.get(languageCode)
    elif 'default' in language_name:
        return language_name.get('default')
    else:
        return language_name.get('Default')


def is_date(filter_field, dt):
    try:
        datetime.datetime.strptime(dt, DISPLAY_DATE_FORMAT)
    except Exception:
        invalid_msg = ('API query is not valid and is ignored: %s=%s'
                       % (filter_field, dt))
        LOG.warning(invalid_msg)
        return False

    return True


def get_datetime_from(dt, tzinfo):
    zone = pytz.timezone(tzinfo)
    from_date = datetime.datetime.strptime(dt, DISPLAY_DATE_FORMAT)

    local_dt = zone.localize(from_date, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.strftime(INTERNAL_UTC_DATETIME_FORMAT)


def get_datetime_to(dt, tzinfo):
    zone = pytz.timezone(tzinfo)
    to_date = datetime.datetime.strptime(dt, DISPLAY_DATE_FORMAT)

    local_dt = zone.localize(to_date, is_dst=None)
    local_dt = local_dt + datetime.timedelta(days=1)
    local_dt = local_dt - datetime.timedelta(microseconds=1)

    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt.strftime(INTERNAL_UTC_DATETIME_FORMAT)


def get_utc_datetime(request, date):
    date_string = "%sT00:00:00.000000" % date.strftime(DISPLAY_DATE_FORMAT)
    date = datetime.datetime.strptime(date_string,
                                      INTERNAL_UTC_DATETIME_FORMAT)
    zone = _get_time_zone(request)
    local_dt = zone.localize(date, is_dst=None)
    return local_dt.astimezone(pytz.utc)


def get_utc_datetime_str(request, date):
    if not date:
        return ''

    return get_utc_datetime(request, date).strftime(
        INTERNAL_UTC_DATETIME_FORMAT)


def get_localize_display_date(request, utc_date_str):
    if not utc_date_str:
        return ''

    zone = _get_time_zone(request)
    utc_date = datetime.datetime.strptime(utc_date_str,
                                          INTERNAL_UTC_DATETIME_FORMAT)
    return zone.fromutc(utc_date).strftime(DISPLAY_DATE_FORMAT)


def get_localize_display_datetime(request, utc_date_str):
    if not utc_date_str:
        return ''

    zone = _get_time_zone(request)
    utc_date = datetime.datetime.strptime(utc_date_str,
                                          INTERNAL_UTC_DATETIME_FORMAT)
    return zone.fromutc(utc_date).strftime(DISPLAY_DATETIME_FORMAT)


def get_currency_unit():
    return CURRENCY_UNIT


def get_price_string(value):
    """Get to format price string from value.
    :param value: price string
    """
    try:
        return CURRENCY_FORMAT.format(Decimal(value))
    except (TypeError, InvalidOperation):
        return value


def get_status_code(request, status_name):
    """Convert it into a 'status code'
    using a status name displaying to a screen.
    :param request: request of view
    :param status_name: a status name displaying to a screen
    """
    status_code = 0
    marker = None

    while True:
        ticket_list, has_more_data, has_prev_data = \
            ticket_api.ticket_list_detailed(request,
                                            marker=marker)

        if 0 == len(ticket_list):
            break

        for ticket_row in ticket_list:
            last_workflow = ticket_row.last_workflow
            status_detail = last_workflow['status_detail']
            name = status_detail['status_name']

            if status_name == get_language_name(request, name):
                status_code = status_detail['status_code']
                return status_code

        marker = ticket_list[len(ticket_list) - 1].id

    return status_code


def get_price_from_catalog(request, catalog_id):
    """Get a price from a product
    in consideration of a project price.
    :param request: request of view
    :param catalog_id: target uuid from a catalog
    """
    scope = request.user.project_id

    prices = ticket_api.price_list_detailed2(
        request, catalog_id)

    if 0 == len(prices):
        return NONE_PRICE_STRING

    my_projcet_prices = filter(lambda row:
                               row.scope == scope,
                               prices)
    # Get project price, not exists is default price
    if 0 < len(my_projcet_prices):
        return ticket_api._get_price_string(my_projcet_prices[0].price)

    else:
        default = filter(lambda row:
                         row.scope == "" or
                         row.scope == "Default",
                         prices)
        return ticket_api._get_price_string(default[0].price)


def get_total_price(values):
    """Get total price.
    :param values: price string list
    """
    total_price = 0
    for value in values:
        try:
            price = Decimal(value)
        except (TypeError, InvalidOperation):
            return NONE_PRICE_STRING

        total_price = total_price + price

    return total_price


def is_decimal_string(values):
    """Check decimal string values.
    It becomes 'True' in all cases decimal string value.
    :param values: decimal string value list
    """
    for value in values:
        try:
            Decimal(value)
        except (TypeError, InvalidOperation):
            return False

    return True


def sort_ticket_workflow_by_confirmed_at(ticket_workflow):
    """Sort ticket has workflow data
    that has already been updated to updated date order.
    :param ticket_workflow: target workflow data
    """
    valid_last_status_rows = filter(
        lambda row:
        row["status"] != constants.WORKFLOW_STATUS_INITIAL,
        ticket_workflow)
    return sorted(valid_last_status_rows,
                  key=lambda status:
                  status.get('confirmed_at'),
                  reverse=False)


def _get_time_zone(request):
    tzinfo = request.session.get(
        'django_timezone', request.COOKIES.get('django_timezone', 'UTC'))
    return pytz.timezone(tzinfo)
