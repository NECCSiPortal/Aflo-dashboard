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

from django.core.urlresolvers import reverse_lazy
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import tabs
from horizon.utils import memoized

from nec_portal import api

from nec_portal.dashboards.project.private_price_lists import \
    constants
from nec_portal.dashboards.project.private_price_lists import \
    tables as catalog_tables
from nec_portal.dashboards.project.private_price_lists import \
    tabs as catalog_tabs

LOG = logging.getLogger(__name__)

SCOPE_DEFAULT = 'Default'


class Catalog(object):
    """Catalog class"""
    def __init__(self, catalog_id, catalog_name,
                 lifetime_start, lifetime_end, price, description,
                 catalog_scope_id, price_seq_no):

        self.catalog_id = escape(catalog_id)
        self.catalog_name = _(escape(catalog_name))  # noqa
        self.lifetime_start = \
            _get_format_datetime_string(escape(lifetime_start))
        lifetime_end = \
            _get_format_datetime_string(escape(lifetime_end))
        self.lifetime_end = _get_format_enddate(lifetime_end)
        self.price = api.ticket._get_price_string(escape(price))
        self.description = escape(description)
        self.catalog_scope_id = escape(catalog_scope_id)
        self.price_seq_no = escape(price_seq_no)


class IndexView(tables.DataTableView):
    """Index view class"""
    table_class = catalog_tables.CatalogsTable
    template_name = constants.CATALOG_INDEX_TEMPLATE
    page_title = _("Price List")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        catalogs = []

        search_filters = self.get_filters()
        prev_marker = self.request.GET.get(
            catalog_tables.CatalogsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                catalog_tables.CatalogsTable._meta.pagination_param, None)

        try:
            project_id = self.request.user.project_id
            catalog_list, self._prev, self._more = \
                api.ticket.valid_catalog_list(self.request,
                                              scope=project_id,
                                              refine_flg=False,
                                              marker=marker,
                                              paginate=True,
                                              filters=search_filters,
                                              sort_dir=sort_dir)

            if prev_marker is not None:
                catalog_list = sorted(catalog_list,
                                      key=lambda catalog:
                                      getattr(catalog, 'catalog_id'),
                                      reverse=True)

            for catalog_row in catalog_list:

                catalog = Catalog(catalog_row.catalog_id,
                                  catalog_row.catalog_name,
                                  "",
                                  "",
                                  catalog_row.price,
                                  "",
                                  catalog_row.catalog_scope_id,
                                  catalog_row.price_seq_no)

                catalogs.append(catalog)

        except Exception:
            catalogs = []
            msg = _('Price list can not be retrieved.')
            exceptions.handle(self.request, msg)
        return catalogs

    def get_filters(self):
        lifetime = api.ticket.get_datetime_now()

        filters = {"lifetime": lifetime}

        filter_field = self.table.get_filter_field()
        filter_string = self.table.get_filter_string().strip()

        if filter_field == 'catalog_name' and filter_string:
            filters[filter_field] = _(filter_string)  # noqa

        elif filter_field and filter_string:
            filters[filter_field] = filter_string

        return filters


class DetailView(tabs.TabView):
    """Detail view class"""
    tab_group_class = catalog_tabs.CatalogDetailTabs
    template_name = 'horizon/common/_detail.html'
    page_title = None

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        catalog = self.get_data()
        context["catalog"] = catalog

        self.page_title = catalog.catalog_name

        return context

    @memoized.memoized_method
    def get_data(self):
        catalog_id = self.kwargs['catalog_id'].split('|')[0]
        try:
            catalog_data = self._get_catalog_data(catalog_id)

            return catalog_data

        except Exception:
            msg = _('Unable to retrieve details for catalog "%s".') \
                % (catalog_id)
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

    @staticmethod
    def get_redirect_url():
        return reverse_lazy(constants.CATALOG_INDEX_URL)

    def get_tabs(self, request, *args, **kwargs):
        catalog = self.get_data()
        return self.tab_group_class(request, catalog=catalog, **kwargs)

    @memoized.memoized_method
    def _get_catalog_data(self, catalog_id):
        try:
            project_id = self.request.user.project_id
            catalog_data, unused_p, unused_m = \
                api.ticket.valid_catalog_list(self.request,
                                              scope=project_id,
                                              refine_flg=False,
                                              filters={'catalog_id':
                                                       catalog_id})

            catalog_data_wk = catalog_data[0]
            lifetime_s = catalog_data_wk.catalog_lifetime_start
            if lifetime_s < catalog_data_wk.catalog_scope_lifetime_start:
                lifetime_s = catalog_data_wk.catalog_scope_lifetime_start
            if lifetime_s < catalog_data_wk.price_lifetime_start:
                lifetime_s = catalog_data_wk.price_lifetime_start

            lifetime_e = catalog_data_wk.catalog_lifetime_end
            if lifetime_e > catalog_data_wk.catalog_scope_lifetime_end:
                lifetime_e = catalog_data_wk.catalog_scope_lifetime_end
            if lifetime_e > catalog_data_wk.price_lifetime_end:
                lifetime_e = catalog_data_wk.price_lifetime_end

            catalog_info = api.ticket.catalog_get_detailed(self.request,
                                                           catalog_id)
            exp_text = catalog_info.expansions_text['expansion_text']
            description = ''
            if(exp_text is not None):
                exp_text = json.loads(exp_text)
                description = exp_text['description']

            catalog = Catalog(catalog_data_wk.catalog_id,
                              catalog_data_wk.catalog_name,
                              lifetime_s,
                              lifetime_e,
                              catalog_data_wk.price,
                              description,
                              '',
                              '')

        except Exception:
            msg = _('Unable to retrieve details for catalog "%s".') \
                % (catalog_id)
            exceptions.handle(self.request, msg,
                              redirect=self.get_redirect_url())

        return catalog


def _get_format_datetime_string(value):
    """Get Datetime string from value.
    :Param value: datetime string
    """
    try:
        format_datetime = datetime.datetime.\
            strptime(value,
                     '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')

        return format_datetime

    except Exception:
        return value


def _get_format_enddate(value):
    """Get indefinite if value is enddate.
    :Param value: datetime string
    """
    if '2999-12-31' in value or \
       '9999-12-31' in value:
        return "-"
    else:
        return value
