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

from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from nec_portal.api import ticket
from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils
from nec_portal.dashboards.project.ticket_templates.application_kinds \
    import tables as ticket_templates_tables


class TicketTemplate(object):
    """Ticket template class"""

    def __init__(self, ticket_template_name, target_id,
                 application_kinds_name,
                 ticket_templates_apply_cnt, ticket_type,
                 ticket_first_status_code):
        self.ticket_template_name = escape(ticket_template_name)
        self.target_id = escape(target_id)
        self.application_kinds_name = escape(application_kinds_name)
        self.ticket_templates_apply_cnt = escape(ticket_templates_apply_cnt)
        self.ticket_type = escape(ticket_type)
        self.ticket_first_status_code = escape(ticket_first_status_code)


class ContractTab(tabs.TableTab):
    """Contract tab class"""

    table_classes = (ticket_templates_tables.TicketTemplatesListContractTable,)
    name = _("New Contract")
    slug = "contract_tab"
    template_name = "project/ticket_templates/application_kinds/application_kinds_tables.html"  # noqa
    preload = False

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_tickettemplates_data(self):
        # Get ticket template list
        datum = []

        tt_meta = \
            ticket_templates_tables.TicketTemplatesListContractTable._meta

        prev_marker = self.request.GET.get(tt_meta.prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = ['asc']
            marker = prev_marker
        else:
            sort_dir = ['desc']
            marker = self.request.GET.get(tt_meta.pagination_param, None)

        try:
            ticket_iter, self._more, self._prev = \
                ticket.tickettemplates_list_detailed(
                    self.request,
                    ticket_type="New Contract",
                    marker=marker,
                    paginate=True,
                    filters=None,
                    sort_dir=sort_dir,
                    enable_expansion_filters=True)

            if prev_marker is not None:
                ticket_iter = sorted(ticket_iter,
                                     key=lambda ticket:
                                     getattr(ticket, 'id'),
                                     reverse=True)

            for ticket_row in ticket_iter:
                contents = ticket_row.template_contents
                ticket_template_name = ticket_utils.get_language_name(
                    self.request,
                    contents["ticket_template_name"])
                application_kinds_name = ticket_utils.get_language_name(
                    self.request,
                    contents["application_kinds_name"])

                ticket_template = TicketTemplate(
                    ticket_template_name,
                    ticket_row.id,
                    application_kinds_name,
                    1,
                    contents["ticket_type"],
                    contents["first_status_code"])

                datum.append(ticket_template)

        except Exception:
            self._prev = False
            self._more = False

            exceptions.handle(self.request,
                              _('Unable to retrieve services information.'))

        return datum


class RequestTab(tabs.TableTab):
    """Request tab class"""

    table_classes = (ticket_templates_tables.TicketTemplatesListRequestTable,)
    name = _("Work")
    slug = "request_tab"
    template_name = "project/ticket_templates/application_kinds/application_kinds_tables.html"  # noqa
    preload = False

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_tickettemplates_data(self):
        # Get ticket template list
        datum = []

        tt_meta = \
            ticket_templates_tables.TicketTemplatesListRequestTable._meta

        prev_marker = self.request.GET.get(tt_meta.prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = ['asc']
            marker = prev_marker
        else:
            sort_dir = ['desc']
            marker = self.request.GET.get(tt_meta.pagination_param, None)

        try:
            ticket_iter, self._more, self._prev = \
                ticket.tickettemplates_list_detailed(
                    self.request,
                    ticket_type="Work",
                    marker=marker,
                    paginate=True,
                    filters=None,
                    sort_dir=sort_dir,
                    enable_expansion_filters=True)

            if prev_marker is not None:
                ticket_iter = sorted(ticket_iter,
                                     key=lambda ticket:
                                     getattr(ticket, 'id'),
                                     reverse=True)

            for ticket_row in ticket_iter:
                contents = ticket_row.template_contents
                ticket_template_name = ticket_utils.get_language_name(
                    self.request,
                    contents["ticket_template_name"])
                application_kinds_name = ticket_utils.get_language_name(
                    self.request,
                    contents["application_kinds_name"])

                ticket_template = TicketTemplate(
                    ticket_template_name,
                    ticket_row.id,
                    application_kinds_name,
                    1,
                    contents["ticket_type"],
                    contents["first_status_code"])

                datum.append(ticket_template)

        except Exception:
            self._prev = False
            self._more = False

            exceptions.handle(self.request,
                              _('Unable to retrieve services information.'))

        return datum


class TicketTemplatesGroupTabs(tabs.TabGroup):
    """Ticket templates group tabs class"""

    slug = "ticket_templates_group_tabs"
    tabs = (ContractTab, RequestTab,)
    sticky = True
