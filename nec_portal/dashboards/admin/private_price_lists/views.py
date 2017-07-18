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

import logging

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tables

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.admin.private_price_lists \
    import constants
from nec_portal.dashboards.admin.private_price_lists \
    import tables as project_catalog_tables
from openstack_dashboard.api import keystone as keystone_api
from openstack_dashboard import policy

LOG = logging.getLogger(__name__)

SCOPE_DEFAULT = 'Default'


class IndexView(tables.DataTableView):
    table_class = project_catalog_tables.TenantsTable
    template_name = constants.PROJECT_CATALOG_INDEX_TEMPLATE
    page_title = _("Price Lists for Projects")

    def get_data(self):
        tenants = []
        domain_context = self.request.session.get('domain_context', None)

        if policy.check((("identity", "identity:list_projects"),),
                        self.request):
            try:
                tenants, _more = keystone_api.tenant_list(
                    self.request,
                    domain=domain_context,
                    paginate=False)
            except Exception:
                exceptions.handle(self.request,
                                  _("Unable to retrieve project list."))
        elif policy.check((("identity", "identity:list_user_projects"),),
                          self.request):
            try:
                tenants, _more = keystone_api.tenant_list(
                    self.request,
                    user=self.request.user.id,
                    paginate=False,
                    admin=False)
            except Exception:
                exceptions.handle(self.request,
                                  _("Unable to retrieve project information."))
        else:
            msg = \
                _("Insufficient privilege level to view project information.")
            messages.info(self.request, msg)
        return tenants


class PrivatePriceViews(tables.DataTableView):
    table_class = project_catalog_tables.PrivatePriceTable
    template_name = constants.PRIVATE_PRICE_TEMPLATE
    page_title = _("Edit Private Price List")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):

        project_id = self.kwargs['project_id']

        try:
            project = keystone_api.tenant_get(self.request, project_id)
            self.page_title = _("Edit Private Price List") + ": %s" % \
                project.name
        except Exception:
            exceptions.handle(self.request, _("Unable to retrieve project."))

        prev_marker = self.request.GET.get(
            project_catalog_tables.PrivatePriceTable._meta
            .prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                project_catalog_tables.PrivatePriceTable._meta
                .pagination_param, None)

        if marker is not None:
            marker = marker.split('|')[0]

        filters = self.get_filters()

        self._prev = False
        self._more = False

        catalog_scope_list, self._prev, self._more = \
            ticket_api.catalog_scope_list(self.request,
                                          project_id,
                                          marker=marker,
                                          sort_key='catalog_id',
                                          sort_dir=sort_dir,
                                          filters=filters,
                                          paginate=True)

        return catalog_scope_list

    def get_filters(self):
        filters = {}
        filter_field = self.table.get_filter_field()
        filter_string = self.table.get_filter_string()

        if filter_field == 'catalog_name' and filter_string:
            filters[filter_field] = _(filter_string)  # noqa

        elif filter_field and filter_string:
            filters[filter_field] = filter_string

        return filters


class PublicPriceViews(tables.DataTableView):
    table_class = project_catalog_tables.PublicPriceTable
    template_name = constants.PUBLIC_PRICE_TEMPLATE
    page_title = _("Edit Public Price List")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        prev_marker = self.request.GET.get(
            project_catalog_tables.PublicPriceTable._meta
            .prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                project_catalog_tables.PublicPriceTable._meta
                .pagination_param, None)

        if marker is not None:
            marker = marker.split('|')[0]

        filters = self.get_filters()

        self._prev = False
        self._more = False

        catalog_scope_list, self._prev, self._more = \
            ticket_api.catalog_scope_list(self.request,
                                          SCOPE_DEFAULT,
                                          marker=marker,
                                          sort_key='catalog_id',
                                          sort_dir=sort_dir,
                                          filters=filters,
                                          paginate=True)

        return catalog_scope_list

    def get_filters(self):
        filters = {}
        filter_field = self.table.get_filter_field()
        filter_string = self.table.get_filter_string()

        if filter_field == 'catalog_name' and filter_string:
            filters[filter_field] = _(filter_string)  # noqa

        elif filter_field and filter_string:
            filters[filter_field] = filter_string

        return filters
