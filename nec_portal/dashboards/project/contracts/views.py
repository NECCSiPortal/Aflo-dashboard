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
import json
import logging
import pytz
import six.moves.urllib.parse as urlparse

from django.core.urlresolvers import reverse_lazy
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from openstack_auth import utils as auth_utils

from horizon import exceptions
from horizon import tables
from horizon import tabs
from horizon.utils import memoized

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.project.contracts \
    import constants
from nec_portal.dashboards.project.contracts \
    import tables as contract_table
from nec_portal.dashboards.project.contracts \
    import tabs as contracts_tabs
from nec_portal.local import nec_portal_settings

LOG = logging.getLogger(__name__)


class ColumnsEscape(object):

    """Columns Escape class"""
    def __init__(self, contract_id, parent_contract_id, ticket_template_name,
                 application_name, application_date, lifetime_start,
                 lifetime_end, expansion_text):

        self.contract_id = escape(contract_id)
        self.parent_contract_id = escape(parent_contract_id)
        self.ticket_template_name = _(escape(ticket_template_name))  # noqa
        self.application_name = escape(application_name)
        self.application_date = escape(application_date)
        self.lifetime_start = escape(lifetime_start)
        self.lifetime_end = escape(lifetime_end)
        self.expansion_text = expansion_text


class IndexView(tables.DataTableView):
    """Index view class"""
    table_class = contract_table.ContractTable
    template_name = constants.CONTRACTS_INDEX_VIEW_TEMPLATE
    page_title = _("Contracts")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        contracts = []

        search_filters = self.get_filters()

        prev_marker = self.request.GET.get(
            contract_table.ContractTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = 'asc,asc'
            marker = prev_marker
        else:
            sort_dir = 'desc,desc'
            marker = self.request.GET.get(
                contract_table.ContractTable._meta.pagination_param, None)

        try:
            contract_list, self._more, self._prev = \
                ticket_api.contract_list_detailed(self.request,
                                                  marker=marker,
                                                  paginate=True,
                                                  filters=search_filters,
                                                  sort_dir=sort_dir)

            if prev_marker is not None:
                contract_list = sorted(contract_list,
                                       key=lambda contract:
                                       getattr(contract, 'lifetime_start'),
                                       reverse=True)

            for contract_row in contract_list:

                parent_contract_id = contract_row.parent_contract_id
                ticket_template_name = contract_row.ticket_template_name
                application_name = contract_row.application_name
                application_date = None
                lifetime_start = None
                lifetime_end = None
                if contract_row.application_date is not None:
                    application_date = datetime.datetime.strptime(
                        contract_row.application_date,
                        '%Y-%m-%dT%H:%M:%S.%f').strftime("%Y-%m-%d %H:%M:%S")
                if contract_row.lifetime_start is not None:
                    lifetime_start = datetime.datetime.strptime(
                        contract_row.lifetime_start,
                        '%Y-%m-%dT%H:%M:%S.%f').strftime("%Y-%m-%d %H:%M:%S")
                if contract_row.lifetime_end is not None:
                    lifetime_end = datetime.datetime.strptime(
                        contract_row.lifetime_end,
                        '%Y-%m-%dT%H:%M:%S.%f').strftime("%Y-%m-%d %H:%M:%S")
                expansion_text = contract_row.expansions_text['expansion_text']

                columns = ColumnsEscape(contract_row.contract_id,
                                        parent_contract_id,
                                        ticket_template_name,
                                        application_name,
                                        application_date,
                                        lifetime_start,
                                        lifetime_end,
                                        expansion_text)

                contracts.append(columns)

        except Exception:
            self._prev = False
            self._more = False

            exceptions.handle(self.request,
                              _('Unable to retrieve contracts information.'))

        return contracts

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['region_list'] = []

        roles = self._get_user_roles()
        region_list = self._get_region_links()

        for region in region_list:
            role_list = region.get('role', None)
            if not role_list:
                context['region_list'].append(self._create_link(region))
                continue

            for role_select in role_list:
                if role_select in roles:
                    context['region_list'].append(self._create_link(region))
                    break

        return context

    def _get_region_links(self):
        return getattr(nec_portal_settings, 'REGION_CONTRACTS_LINKS', [])

    def _get_user_roles(self):
        user = auth_utils.get_user(self.request)
        return [role['name'] for role in user.roles]

    def _create_link(self, link):
        _url = link.get('root_url', '')

        return {
            'name': link.get('name', ''),
            'url': urlparse.urljoin(_url, constants.CONTRACTS_REGION_URL)
        }

    def get_filters(self):
        filters = {'project_id': self.request.user.project_id}
        filter_field = self.table.get_filter_field()
        filter_string = self.table.get_filter_string().strip()
        if filter_field and filter_string:

            try:
                if filter_field in ['ticket_template_name']:
                    filters[filter_field] = _(filter_string)  # noqa
                elif filter_field in ['parent_contract_id']:
                    filters[filter_field] = filter_string
                elif filter_field in ['application_name']:
                    filters[filter_field] = filter_string
                elif filter_field in ['application_date']:
                    if self._is_date(filter_field, filter_string):
                        tzinfo = self.request.session.\
                            get('django_timezone',
                                self.request.COOKIES.get('django_timezone',
                                                         'UTC'))
                        filters['application_date_from'] = \
                            self._get_datetime_from(filter_string, tzinfo)
                        filters['application_date_to'] = \
                            self._get_datetime_to(filter_string, tzinfo)
                elif filter_field in ['lifetime_start']:
                    if self._is_date(filter_field, filter_string):
                        tzinfo = self.request.session.\
                            get('django_timezone',
                                self.request.COOKIES.get('django_timezone',
                                                         'UTC'))
                        filters['lifetime_start_from'] = \
                            self._get_datetime_from(filter_string, tzinfo)
                        filters['lifetime_start_to'] = \
                            self._get_datetime_to(filter_string, tzinfo)
                elif filter_field in ['lifetime_end']:
                    if self._is_date(filter_field, filter_string):
                        tzinfo = self.request.session.\
                            get('django_timezone',
                                self.request.COOKIES.get('django_timezone',
                                                         'UTC'))
                        filters['lifetime_end_from'] = \
                            self._get_datetime_from(filter_string, tzinfo)
                        filters['lifetime_end_to'] = \
                            self._get_datetime_to(filter_string, tzinfo)
                elif filter_field in ['lifetime']:
                    if self._is_date(filter_field, filter_string):
                        filters['date_in_lifetime'] = filter_string
                else:
                    filters[filter_field] = filter_string
            except Exception:
                msg = \
                    ('An error occurred when creating filters: %s=%s'
                     % (filter_field, filter_string))
                exceptions.handle(self.request, msg)

        return filters

    def _is_date(self, filter_field, dt):
        try:
            datetime.datetime.strptime(dt, "%Y-%m-%d")
        except Exception:
            invalid_msg = ('API query is not valid and is ignored: %s=%s'
                           % (filter_field, dt))
            LOG.warning(invalid_msg)
            return False

        return True

    def _get_datetime_from(self, dt, tzinfo):
        zone = pytz.timezone(tzinfo)
        from_date = datetime.datetime.strptime(dt, "%Y-%m-%d")

        local_dt = zone.localize(from_date, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)

        return utc_dt.strftime("%Y-%m-%dT%H:%M:%S.%f")

    def _get_datetime_to(self, dt, tzinfo):
        zone = pytz.timezone(tzinfo)
        to_date = datetime.datetime.strptime(dt, "%Y-%m-%d")

        local_dt = zone.localize(to_date, is_dst=None)
        local_dt = local_dt + datetime.timedelta(days=1)
        local_dt = local_dt - datetime.timedelta(microseconds=1)

        utc_dt = local_dt.astimezone(pytz.utc)

        return utc_dt.strftime("%Y-%m-%dT%H:%M:%S.%f")


class DetailView(tabs.TabView):
    tab_group_class = contracts_tabs.ContractsDetailTabs
    template_name = constants.CONTRACTS_DETAIL_VIEW_TEMPLATE
    page_title = None
    contract = None

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        self.contract = self.get_data()
        context["contract"] = self.contract
        context["action_url"] = self.get_redirect_url()
        self.page_title = self.contract.application_kinds_name

        return context

    def get_redirect_url(self):
        expansion_text = json.loads(
            self.contract.expansions_text['expansion_text'])
        cancel_info = expansion_text['ticket_info']['cancelling_template']
        url = 'horizon:project:contracts:wf_engine_create:index'

        return reverse_lazy(
            url, args=[cancel_info['id'], self.kwargs['id']])

    @memoized.memoized_method
    def get_data(self):
        try:
            contract_data = ticket_api.contract_get_detailed(
                self.request,
                self.kwargs['id'])

            ticket_template_name = contract_data.ticket_template_name
            application_kinds_name = contract_data.application_kinds_name
            contract_data.ticket_template_name = \
                _(ticket_template_name)  # noqa
            contract_data.application_kinds_name = \
                _(application_kinds_name)  # noqa

        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve contracts details.'),
                              redirect=self.get_redirect_url())

        return contract_data

    def get_tabs(self, request, *args, **kwargs):
        contract = self.get_data()
        return self.tab_group_class(request, contract=contract, **kwargs)
