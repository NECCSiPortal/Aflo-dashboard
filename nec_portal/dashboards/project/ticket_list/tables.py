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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from nec_portal.dashboards.project.ticket_list import utils

LOG = logging.getLogger(__name__)


class TicketFilterAction(tables.FilterAction):
    """Ticket filter action class"""
    filter_type = "server"
    filter_choices = (('ticket_type', _('Category ='), True),
                      ('ticket_template_name', _('Type ='), True),
                      ('ticket_id', _('ID ='), True),
                      ('application_kinds_name', _('Request Form ='), True),
                      ('owner_at', _('Issue Date ='), True),
                      ('owner_name', _('Issuer ='), True),
                      ('last_confirmed_at', _('Last Update ='), True),
                      ('last_confirmer_name', _('Updated By ='), True),
                      ('last_status_code', _('Status ='), True))


class EditTicket(tables.LinkAction):
    """Edit ticket class"""
    name = "edit"
    verbose_name = _("Edit Request")
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, ticket=None):
        url = 'horizon:project:ticket_list:wf_engine_update:index'
        return reverse(url, args=[ticket.ticket_id])

    def allowed(self, request, datum):
        return utils.allowed_grant_role(request,
                                        datum.status_name,
                                        datum.last_workflow)


def get_detail_link_url(ticket):
    url = 'horizon:project:ticket_list:wf_engine_detail:index'
    return reverse(url, args=[ticket.ticket_id])


class TicketTable(tables.DataTable):
    """Ticket table class"""
    ticket_type = tables.Column('ticket_type',
                                verbose_name=_('Category'))
    ticket_template_name = tables.Column('ticket_template_name',
                                         verbose_name=_('Type'))
    ticket_id = tables.Column('ticket_id',
                              verbose_name=_('ID'),
                              link=get_detail_link_url)
    application_kinds_name = tables.Column('application_kinds_name',
                                           verbose_name=_('Request Form'))
    owner_at = tables.Column('owner_at',
                             verbose_name=_('Issue Date'))
    owner_name = tables.Column('owner_name',
                               verbose_name=_('Issuer'))
    confirmed_at = tables.Column('confirmed_at',
                                 verbose_name=_('Last Update'))
    confirmer_name = tables.Column('confirmer_name',
                                   verbose_name=_('Updated By'))
    status_name = tables.Column('status_name',
                                verbose_name=_('Status'))

    def get_object_id(self, svr):
        return svr.ticket_id

    class Meta(object):
        """Meta class"""
        name = "ticket_list"
        verbose_name = 'Issued Requests'

        row_actions = (EditTicket,)
        multi_select = False

        table_actions = (TicketFilterAction,)
        pagination_param = "ticket_marker"
