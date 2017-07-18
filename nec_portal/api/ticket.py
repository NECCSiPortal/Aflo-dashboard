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

from __future__ import absolute_import

import datetime
import decimal
from decimal import Decimal
from decimal import ROUND_DOWN
import itertools
import logging

from django.conf import settings
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

import afloclient as aflo_client
from afloclient import exc

from horizon import exceptions
from horizon.utils import functions as utils
from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard.api import base

from nec_portal.local import nec_portal_settings as nec_set

LOG = logging.getLogger(__name__)
VERSIONS = base.APIVersionManager("ticket", preferred_version=2)

SCOPE_DEFAULT = 'Default'

CURRENCY_FORMAT = getattr(nec_set, 'CURRENCY_FORMAT', '{0:,.2f}')
PRICE_FORMAT = getattr(nec_set, 'PRICE_FORMAT', [',', '.', 2])


def _get_price_string(value):
    """Get Price string from value.
    :Param value: price string
    """
    try:
        if 0 < PRICE_FORMAT[2]:
            rd_format = '.' + '1'.zfill(PRICE_FORMAT[2])
            price = Decimal(value).quantize(Decimal(rd_format),
                                            rounding=ROUND_DOWN)
        else:
            price = Decimal(value).quantize(Decimal('1.'),
                                            rounding=ROUND_DOWN)

        return CURRENCY_FORMAT.format(price)

    except (TypeError, decimal.InvalidOperation):
        return value


class ProjectCatalog(object):
    '''Project Catalog Class
    '''
    def __init__(self,
                 catalog_id,
                 scope,
                 seq_no,
                 catalog_name,
                 price,
                 project_id):

        self.catalog_id = escape(catalog_id)
        self.scope = escape(scope)
        self.seq_no = escape(seq_no)
        self.catalog_name = _(escape(catalog_name))  # noqa
        self.price = _get_price_string(escape(price))
        self.project_id = escape(project_id)


@memoized
def afloclient(request, version='1'):
    url = base.url_for(request, 'ticket')
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    return aflo_client.Client(version, url, token=request.user.token.id,
                              insecure=insecure, cacert=cacert)


# Get ticket list
def ticket_list_detailed(request,
                         marker=None,
                         sort_dir='desc',
                         sort_key='created_at',
                         filters=None,
                         paginate=False,
                         ticket_type=None):
    if not filters or ('ticket_id' not in filters):
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        page_size = utils.get_page_size(request)

        if paginate:
            request_size = page_size + 1
        else:
            request_size = limit

        kwargs = {'limit': limit,
                  'sort_dir': sort_dir,
                  'sort_key': sort_key, }

        if marker:
            kwargs['marker'] = marker
        if filters or filters is not None:
            kwargs.update(filters)

        if ticket_type:
            if 'ticket_type' in kwargs:
                kwargs['ticket_type'] = [kwargs['ticket_type']]
                kwargs['ticket_type'].append(ticket_type)
            else:
                kwargs['ticket_type'] = ticket_type

        LOG.debug('Ticket List Filter= ' + str(kwargs))
        tickets_list = afloclient(request).tickets.list(kwargs)
        has_prev_data = False
        has_more_data = False

        if paginate:
            tickets = list(itertools.islice(tickets_list, request_size))

            # first and middle page condition
            if len(tickets) > page_size:
                tickets.pop(-1)
                has_more_data = True
                # middle page condition
                if marker is not None:
                    has_prev_data = True
            # first page condition when reached via prev back
            elif sort_dir == 'asc' and marker is not None:
                has_more_data = True
            # last page condition
            elif marker is not None:
                has_prev_data = True
        else:
            tickets = list(tickets_list)

        return (tickets, has_more_data, has_prev_data)

    else:
        ticket_list = []
        # if user selected ticket_id,
        # Use ticket-get API.
        try:
            ticket = ticket_get_detailed(request, filters['ticket_id'])

            # Filtering project id
            if 'tenant_id' in filters and \
                    ticket.tenant_id != filters['tenant_id']:

                return (ticket_list, False, False)

            # Convert get data to list data
            last_workflow = filter(lambda workflow:
                                   workflow['status'] == 1,
                                   ticket.workflow)
            setattr(ticket, 'last_workflow', last_workflow[0])
            ticket_list.append(ticket)

        except exc.HTTPNotFound:
            pass

        return (ticket_list, False, False)


# Get ticket template list(get all data)
def tickettemplates_list_detailed_get_all(request, marker=None):
    kwargs = {}
    if marker:
        kwargs['marker'] = marker

    tickets_iter = afloclient(request).tickettemplates.list(kwargs)

    return tickets_iter


def ticket_get_detailed(request, ticket_id):
    ticket = afloclient(request).tickets.get(ticket_id)

    return ticket


# Get ticket template list
def tickettemplates_list_detailed(request,
                                  ticket_type=None,
                                  marker=None,
                                  sort_dir=['desc'],
                                  sort_key=['id'],
                                  filters=None,
                                  paginate=False,
                                  enable_expansion_filters=False):
    limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    kwargs = {'limit': limit,
              'sort_dir': sort_dir,
              'sort_key': sort_key,
              'enable_expansion_filters': enable_expansion_filters, }

    if ticket_type:
        kwargs['ticket_type'] = ticket_type

    if marker:
        kwargs['marker'] = marker

    tickets_list = afloclient(request).tickettemplates.list(kwargs)
    has_prev_data = False
    has_more_data = False

    if paginate:
        tickets = list(itertools.islice(tickets_list, request_size))

        # first and middle page condition
        if len(tickets) > page_size:
            tickets.pop(-1)
            has_more_data = True
            # middle page condition
            if marker is not None:
                has_prev_data = True
        # first page condition when reached via prev back
        elif sort_dir == ['asc'] and marker is not None:
            has_more_data = True
        # last page condition
        elif marker is not None:
            has_prev_data = True
    else:
        tickets = list(tickets_list)

    return (tickets, has_more_data, has_prev_data)


# Get ticket template
def tickettemplates_get(request, target_id):
    ticket = afloclient(request).tickettemplates.get(target_id)

    return ticket


# Crate ticket
def ticket_create(request, fields):
    afloclient(request).tickets.create(fields)


# Update ticket
def ticket_update(request, ticket_id, fields):
    afloclient(request).tickets.update(ticket_id, fields)


# Get contract list
def contract_list_detailed(request,
                           marker=None,
                           sort_dir='desc,desc',
                           sort_key='lifetime_start,contract_id',
                           filters=None,
                           paginate=False):
    limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    kwargs = {'limit': limit,
              'sort_dir': sort_dir,
              'sort_key': sort_key, }

    if marker:
        kwargs['marker'] = marker
    if filters or filters is not None:
        kwargs.update(filters)

    contract_list = afloclient(request).contracts.list(kwargs)
    has_prev_data = False
    has_more_data = False

    if paginate:
        contracts = list(itertools.islice(contract_list, request_size))

        # first and middle page condition
        if len(contracts) > page_size:
            contracts.pop(-1)
            has_more_data = True
            # middle page condition
            if marker is not None:
                has_prev_data = True
        # first page condition when reached via prev back
        elif sort_dir == 'asc,asc' and marker is not None:
            has_more_data = True
        # last page condition
        elif marker is not None:
            has_prev_data = True
    else:
        contracts = list(contract_list)

    return (contracts, has_more_data, has_prev_data)


def contract_get_detailed(request, contract_id):
    return afloclient(request).contracts.get(contract_id)


def catalog_list_detailed(request,
                          marker=None,
                          limit=None,
                          sort_key='catalog_id',
                          sort_dir='desc',
                          force_show_deleted=None,
                          filters=None,
                          paginate=False):

    limit = limit or getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    kwargs = {'limit': limit,
              'sort_dir': sort_dir,
              'sort_key': sort_key, }

    if marker is not None:
        kwargs['marker'] = marker
    if force_show_deleted is not None:
        kwargs['force_show_deleted'] = force_show_deleted
    if filters is not None:
        kwargs.update(filters)

    catalog_list = afloclient(request).catalogs.list(kwargs)

    has_prev_data = False
    has_more_data = False

    if paginate:
        catalogs = list(itertools.islice(catalog_list, request_size))

        if sort_dir == 'desc':
            if len(catalogs) > page_size:
                catalogs.pop(-1)
                has_more_data = True
            else:
                has_more_data = False

            if marker is not None:
                has_prev_data = True
        else:
            if len(catalogs) > page_size:
                catalogs.pop(-1)
                has_prev_data = True
            else:
                has_prev_data = False

            has_more_data = True
            catalogs.reverse()
    else:
        catalogs = list(catalog_list)

    return (catalogs, has_prev_data, has_more_data)


def catalog_get_detailed(request, catalog_id):
    return afloclient(request).catalogs.get(catalog_id)


def catalog_contents_get_detailed(request, catalog_id):
    return afloclient(request).catalog_contents.get(catalog_id)


def price_list_detailed(request,
                        catalog_id,
                        scope=None,
                        lifetime=None,
                        marker=None,
                        limit=None,
                        sort_key='lifetime_start',
                        sort_dir='desc',
                        force_show_deleted=None,
                        filters=None,
                        paginate=False):

    limit = limit or getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    kwargs = {'limit': limit,
              'sort_dir': sort_dir,
              'sort_key': sort_key, }

    if scope:
        kwargs['scope'] = scope
    if lifetime:
        kwargs['lifetime'] = lifetime
    if marker is not None:
        kwargs['marker'] = marker
    if force_show_deleted is not None:
        kwargs['force_show_deleted'] = force_show_deleted
    if filters is not None:
        kwargs.update(filters)

    price_list = afloclient(request).price.list(catalog_id, kwargs)

    has_prev_data = False
    has_more_data = False

    if paginate:
        prices = list(itertools.islice(price_list, request_size))

        if sort_dir == 'desc':
            if len(prices) > page_size:
                prices.pop(-1)
                has_more_data = True
            else:
                has_more_data = False

            if marker is not None:
                has_prev_data = True
        else:
            if len(prices) > page_size:
                prices.pop(-1)
                has_prev_data = True
            else:
                has_prev_data = False

            has_more_data = True
            prices.reverse()

    else:
        prices = list(price_list)

    return (prices, has_prev_data, has_more_data)


def catalog_price_list(request,
                       project_id,
                       marker=None,
                       limit=None,
                       sort_key=None,
                       sort_dir=None,
                       force_show_deleted=None,
                       filters=None,
                       paginate=False):

    details = []

    _prev = False
    _more = False

    try:
        catalogs, _prev, _more = \
            catalog_list_detailed(request,
                                  marker=marker,
                                  sort_key=sort_key,
                                  sort_dir=sort_dir,
                                  force_show_deleted=force_show_deleted,
                                  filters=filters,
                                  paginate=paginate)

        lifetime = get_datetime_now()
        for catalog in catalogs:
            prices, unsued_p, unsed_n = price_list_detailed(request,
                                                            catalog.catalog_id,
                                                            lifetime=lifetime)
            if prices is None or len(prices) == 0:
                continue

            price = None
            for p in prices:
                if p.scope and p.scope == project_id:
                    price = p
                    break
                else:
                    if price is None and p.scope and p.scope == SCOPE_DEFAULT:
                        price = p

            if price is None:
                continue

            detail = ProjectCatalog(catalog.catalog_id,
                                    price.scope,
                                    price.seq_no,
                                    catalog.catalog_name,
                                    price.price,
                                    project_id)

            details.append(detail)

    except Exception:
        _prev = False
        _more = False
        exceptions.handle(request,
                          _("Unable to retrieve project catalog list."))

    return details, _prev, _more


def price_get_with_project_id(request, project_id, catalog_id, scope, seq_no):

    prices, _prev, _more = price_list_detailed(request, catalog_id,
                                               filters={'scope':
                                                        project_id},
                                               lifetime=get_datetime_now(),
                                               paginate=False)

    price = prices[0] if prices and 0 < len(prices) else None

    if price is None:
        price = afloclient(request).price.get(catalog_id, scope, seq_no)

    return price


def price_update_or_create(request,
                           catalog_id,
                           scope,
                           fields,
                           now=None,
                           del_flg=False):

    if now is None:
        now = get_datetime_now()

    old_lifetime = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S.%f')
    old_lifetime = old_lifetime - datetime.timedelta(seconds=1)
    old_lifetime_str = old_lifetime.strftime('%Y-%m-%dT%H:%M:%S.%f')

    new_lifetime = now
    fields["lifetime_start"] = new_lifetime
    fields["lifetime_end"] = "9999-12-31T23:59:59.999999"

    prices, _prev, _more = price_list_detailed(request, catalog_id,
                                               filters={'scope': scope},
                                               lifetime=now,
                                               paginate=False)

    price = prices[0] if prices and 0 < len(prices) else None

    if price is not None:
        afloclient(request).price.update(price.catalog_id,
                                         price.scope,
                                         price.seq_no,
                                         {"lifetime_end": old_lifetime_str})
    if del_flg:
        return {}

    return afloclient(request).price.create(catalog_id,
                                            scope,
                                            fields)


def price_list_detailed2(request, catalog_id):
    kwargs = {'lifetime': get_datetime_utcnow(), }
    return afloclient(request).price.list(catalog_id, kwargs)


def get_datetime_now():
    now = datetime.datetime.utcnow()
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f')


def get_datetime_utcnow():
    utcnow = datetime.datetime.utcnow()
    return utcnow.strftime('%Y-%m-%dT%H:%M:%S.%f')


class ValidCatalog(object):
    '''Valid Catalog Class
    '''
    def __init__(self,
                 catalog_id,
                 catalog_name,
                 public_seq_no,
                 public_price,
                 private_seq_no,
                 private_price,
                 project_id):

        self.catalog_id = escape(catalog_id)
        self.catalog_name = _(escape(catalog_name))  # noqa
        self.public_seq_no = escape(public_seq_no)
        self.public_price = _get_price_string(
            escape(_get_format_price(public_price)))
        self.private_seq_no = escape(private_seq_no)
        self.private_price = _get_price_string(
            escape(_get_format_price(private_price)))
        self.project_id = escape(project_id)


def catalog_scope_list(request,
                       project_id,
                       marker=None,
                       limit=None,
                       sort_key=None,
                       sort_dir=None,
                       force_show_deleted=None,
                       filters=None,
                       paginate=False):

    catalog_scope_lists = []
    public_lists = {}
    private_lists = {}

    _prev = False
    _more = False

    try:
        catalogs, _prev, _more = catalog_list_detailed(
            request,
            marker=marker,
            sort_key=sort_key,
            sort_dir=sort_dir,
            force_show_deleted=force_show_deleted,
            filters=filters,
            paginate=paginate)

        lifetime = get_datetime_now()
        res_public, unused_p, unused_m = valid_catalog_list(request,
                                                            refine_flg=True,
                                                            lifetime=lifetime)
        catalog_id_wk = None
        for public_wk in res_public:
            if catalog_id_wk == public_wk.catalog_id:
                continue
            public_lists[public_wk.catalog_id] = public_wk
            catalog_id_wk = public_wk.catalog_id

        res_private, unused_p, unused_m = valid_catalog_list(request,
                                                             scope=project_id,
                                                             refine_flg=True,
                                                             lifetime=lifetime)
        catalog_id_wk = None
        for private_wk in res_private:
            if catalog_id_wk == private_wk.catalog_id:
                continue
            private_lists[private_wk.catalog_id] = private_wk
            catalog_id_wk = private_wk.catalog_id

        for catalog in catalogs:
            seq_no_pub = None
            seq_no_pri = None
            price_pub = None
            price_pri = None

            if catalog.catalog_id in public_lists:
                seq_no_pub = public_lists[catalog.catalog_id].price_seq_no
                price_pub = public_lists[catalog.catalog_id].price
            if catalog.catalog_id in private_lists:
                seq_no_pri = private_lists[catalog.catalog_id].price_seq_no
                price_pri = private_lists[catalog.catalog_id].price

            catalog_scope = ValidCatalog(catalog.catalog_id,
                                         catalog.catalog_name,
                                         seq_no_pub,
                                         price_pub,
                                         seq_no_pri,
                                         price_pri,
                                         project_id)

            catalog_scope_lists.append(catalog_scope)

    except Exception:
        _prev = False
        _more = False
        exceptions.handle(request,
                          _("Unable to retrieve catalog scope list."))

    return catalog_scope_lists, _prev, _more


def valid_catalog_list(request,
                       catalog_id=None,
                       scope='Default',
                       refine_flg=None,
                       lifetime=None,
                       marker=None,
                       limit=None,
                       sort_key='catalog_id',
                       sort_dir='asc',
                       filters=None,
                       paginate=False):

    if lifetime is None:
        lifetime = get_datetime_now()

    limit = limit or getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    kwargs = {'limit': limit,
              'sort_dir': sort_dir,
              'sort_key': sort_key, }

    kwargs['scope'] = scope
    kwargs['lifetime'] = lifetime
    if catalog_id is not None:
        kwargs['catalog_id'] = catalog_id
    if refine_flg is not None:
        kwargs['refine_flg'] = refine_flg
    if marker is not None:
        kwargs['catalog_marker'] = marker.split('|')[0]
        kwargs['catalog_scope_marker'] = marker.split('|')[1]
        kwargs['price_marker'] = marker.split('|')[2]
    if filters is not None:
        kwargs.update(filters)

    valid_catalog = afloclient(request).valid_catalog.list(kwargs)

    has_prev_data = False
    has_more_data = False

    if paginate:
        valid_catalog_wk = list(itertools.islice(valid_catalog, request_size))

        if sort_dir == 'desc':
            if len(valid_catalog_wk) > page_size:
                valid_catalog_wk.pop(-1)
                has_more_data = True
            else:
                has_more_data = False

            if marker is not None:
                has_prev_data = True
        else:
            if len(valid_catalog_wk) > page_size:
                valid_catalog_wk.pop(-1)
                has_prev_data = True
            else:
                has_prev_data = False

            has_more_data = True
            valid_catalog_wk.reverse()

    else:
        valid_catalog_wk = list(valid_catalog)

    return (valid_catalog_wk, has_prev_data, has_more_data)


def _get_format_price(value):
    if None == value:
        return "-"
    else:
        return value


def catalog_scope_update_or_create(request,
                                   catalog_id,
                                   scope,
                                   fields,
                                   now=None,
                                   del_flg=False):

    if now is None:
        now = get_datetime_now()

    old_lifetime = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S.%f')
    old_lifetime = old_lifetime - datetime.timedelta(seconds=1)
    old_lifetime_str = old_lifetime.strftime('%Y-%m-%dT%H:%M:%S.%f')

    new_lifetime = now
    fields['lifetime_start'] = new_lifetime
    fields['lifetime_end'] = '9999-12-31T23:59:59.999999'

    catalog_scape, _prev, _more = catalog_scope_list_detailed(request,
                                                              catalog_id,
                                                              scope,
                                                              now,
                                                              paginate=False)

    catalog_scape = catalog_scape[0] \
        if catalog_scape and 0 < len(catalog_scape) else None

    if catalog_scape is not None:
        afloclient(request).catalog_scope.update(
            catalog_scape.id,
            {'lifetime_end': old_lifetime_str})

    if del_flg:
        return {}

    return afloclient(request).catalog_scope.create(catalog_id,
                                                    scope,
                                                    fields)


def catalog_scope_list_detailed(request,
                                catalog_id,
                                scope=None,
                                lifetime=None,
                                marker=None,
                                limit=None,
                                sort_key='lifetime_start',
                                sort_dir='desc',
                                force_show_deleted=None,
                                filters=None,
                                paginate=False):

    limit = limit or getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    kwargs = {'limit': limit,
              'sort_dir': sort_dir,
              'sort_key': sort_key, }

    if catalog_id:
        kwargs['catalog_id'] = catalog_id
    if scope:
        kwargs['scope'] = scope
    if lifetime:
        kwargs['lifetime'] = lifetime
    if marker is not None:
        kwargs['marker'] = marker
    if force_show_deleted is not None:
        kwargs['force_show_deleted'] = force_show_deleted
    if filters is not None:
        kwargs.update(filters)

    c_scope_list = afloclient(request).catalog_scope.list(kwargs)

    has_prev_data = False
    has_more_data = False

    if paginate:
        catalog_scope = list(itertools.islice(c_scope_list, request_size))

        if sort_dir == 'desc':
            if len(catalog_scope) > page_size:
                catalog_scope.pop(-1)
                has_more_data = True
            else:
                has_more_data = False

            if marker is not None:
                has_prev_data = True
        else:
            if len(catalog_scope) > page_size:
                catalog_scope.pop(-1)
                has_prev_data = True
            else:
                has_prev_data = False

            has_more_data = True
            catalog_scope.reverse()

    else:
        catalog_scope = list(c_scope_list)

    return (catalog_scope, has_prev_data, has_more_data)
