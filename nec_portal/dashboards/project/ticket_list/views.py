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

from django.conf.global_settings import DEFAULT_CHARSET
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.project.ticket_list \
    import constants
from nec_portal.dashboards.project.ticket_list \
    import tables as ticket_list_tables
from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils

LOG = logging.getLogger(__name__)

# Catalog string for view and filtering value
TICKET_TYPE = {
    'New Contract': _('New Contract'),
    'Cancel Contract': _('Cancel Contract'),
    'Work': _('Work'),
}


class TicketService(object):
    """Ticket service class"""
    def __init__(self,
                 ticket_type,
                 ticket_template_name,
                 ticket_id,
                 application_kinds_name,
                 owner_at, owner_name,
                 confirmed_at, confirmer_name,
                 status_name,
                 template_contents,
                 last_workflow):

        self.ticket_type = escape(_(ticket_type))  # noqa
        self.ticket_template_name = escape(ticket_template_name)
        self.ticket_id = escape(ticket_id)
        self.application_kinds_name = escape(application_kinds_name)
        self.owner_at = escape(owner_at)
        self.owner_name = escape(owner_name)
        self.confirmed_at = escape(confirmed_at)
        self.confirmer_name = escape(confirmer_name)
        self.status_name = escape(status_name)
        self.last_workflow = last_workflow


class IndexView(tables.DataTableView):
    """Index view class"""
    table_class = ticket_list_tables.TicketTable
    template_name = constants.TICKET_LIST_INDEX_VIEW_TEMPLATE
    page_title = _("Issued Requests")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        tickets = []

        search_filters = self.get_filters()
        prev_marker = self.request.GET.get(
            ticket_list_tables.TicketTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                ticket_list_tables.TicketTable._meta.pagination_param, None)

        try:
            ticket_list, self._more, self._prev = \
                ticket_api.ticket_list_detailed(self.request,
                                                marker=marker,
                                                paginate=True,
                                                filters=search_filters,
                                                sort_dir=sort_dir)

            if prev_marker is not None:
                ticket_list = sorted(ticket_list,
                                     key=lambda ticket:
                                     getattr(ticket, 'created_at'),
                                     reverse=True)
            # Set View Rows
            for ticket_row in ticket_list:
                ticket_template_id = ticket_row.ticket_template_id
                w_last_workflow = ticket_row.last_workflow

                # Get Tickettemplate data
                template_contents = ticket_utils.get_ticket_template_contents(
                    self.request,
                    ticket_template_id)

                # Workflow data
                status_detail = w_last_workflow['status_detail']
                status_name = ticket_utils.get_language_name(
                    self.request,
                    status_detail['status_name'])

                # Ticket data
                ticket_template_name = ticket_utils.get_language_name(
                    self.request,
                    template_contents['ticket_template_name'])
                application_kinds_name = ticket_utils.get_language_name(
                    self.request,
                    template_contents['application_kinds_name'])

                owner_at = ticket_utils.get_localize_display_datetime(
                    self.request, ticket_row.owner_at)
                owner_name = ticket_row.owner_name

                confirmed_at = ticket_utils.get_localize_display_datetime(
                    self.request, w_last_workflow['confirmed_at'])
                confirmer_name = w_last_workflow['confirmer_name']

                # Create View Rows
                service = TicketService(ticket_row.ticket_type,
                                        ticket_template_name,
                                        ticket_row.id,
                                        application_kinds_name,
                                        owner_at, owner_name,
                                        confirmed_at, confirmer_name,
                                        status_name,
                                        template_contents,
                                        ticket_row.last_workflow)

                tickets.append(service)

        except Exception:
            self._prev = False
            self._more = False

            exceptions.handle(self.request,
                              _('Unable to retrieve requests information.'))

        return tickets

    def _get_filter_field(self):
        return self.table.get_filter_field()

    def _get_filter_string(self):
        return self.table.get_filter_string().strip()

    def _get_timezone(self):
        return self.request.session.\
            get('django_timezone',
                self.request.COOKIES.get('django_timezone',
                                         'UTC'))

    def _get_project_id(self):
        return self.request.user.project_id

    def get_filters(self):
        filters = {'tenant_id': self._get_project_id()}
        filter_field = self._get_filter_field()
        filter_string = self._get_filter_string()

        if filter_field and filter_string:
            try:
                if filter_field in ['owner_at']:
                    if ticket_utils.is_date(filter_field, filter_string):
                        tzinfo = self._get_timezone()
                        filters['owner_at_from'] = \
                            ticket_utils.get_datetime_from(filter_string,
                                                           tzinfo)
                        filters['owner_at_to'] = \
                            ticket_utils.get_datetime_to(filter_string, tzinfo)

                elif filter_field in ['last_confirmed_at']:
                    if ticket_utils.is_date(filter_field, filter_string):
                        tzinfo = self._get_timezone()
                        filters['last_confirmed_at_from'] = \
                            ticket_utils.get_datetime_from(filter_string,
                                                           tzinfo)
                        filters['last_confirmed_at_to'] = \
                            ticket_utils.get_datetime_to(filter_string, tzinfo)

                elif filter_field in ['last_status_code']:
                    filters[filter_field] = \
                        ticket_utils.get_status_code(self.request,
                                                     filter_string)

                elif filter_field in ['ticket_type']:
                    for key, val in TICKET_TYPE.items():
                        if val == filter_string:
                            filters['ticket_type'] = key

                    if 'ticket_type' not in filters:
                        encoding = self.request.encoding \
                            if self.request.encoding is not None \
                            else DEFAULT_CHARSET

                        filters['ticket_type'] = filter_string.encode(encoding)

                else:
                    filters[filter_field] = filter_string

            except Exception:
                msg = \
                    ('An error occurred when creating filters: %s=%s'
                     % (filter_field, filter_string))
                exceptions.handle(self.request, msg)

        return filters
