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

LOG = logging.getLogger(__name__)


class TicketFilterAction(tables.FilterAction):
    """Ticket filter action class"""
    filter_type = "server"
    filter_choices = (('tenant_id', _('Project ='), True),
                      ('ticket_type', _('Category ='), True),
                      ('ticket_template_name', _('Type ='), True),
                      ('ticket_id', _('ID ='), True),
                      ('application_kinds_name', _('Request Form ='), True),
                      ('owner_at', _('Issue Date ='), True),
                      ('owner_name', _('Issuer ='), True),
                      ('last_confirmed_at', _('Last Update ='), True),
                      ('last_confirmer_name', _('Updated By ='), True),
                      ('last_status_code', _('Status ='), True))


def get_detail_link_url(ticket):
    url = 'horizon:admin:ticket_list:wf_engine_detail:index'
    return reverse(url, args=[ticket.ticket_id])


class TicketTable(tables.DataTable):
    """Ticket table class"""
    project_name = tables.Column('project_name',
                                 verbose_name=_('Project'))
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
        name = "admin_ticket_list"
        verbose_name = 'Contract Requests'

        multi_select = False

        table_actions = (TicketFilterAction,)
        pagination_param = "admin_ticket_marker"
