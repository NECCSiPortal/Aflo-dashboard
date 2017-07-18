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
from django.utils.datastructures import SortedDict
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from horizon import conf
from horizon import tables

STRING_SEPARATOR = "__"

LOG = logging.getLogger(__name__)


def get_link_url(datum):

    # make url link
    ticket_template_id = datum.target_id

    url = 'horizon:project:ticket_templates:wf_engine_create:index'
    return reverse(url, args=[ticket_template_id])


class TicketTemplatesListRow(tables.base.Row):
    """Ticket templates list row class"""

    # ticket list cell
    def load_cells(self, datum=None):
        # table > td > rowspan
        # Compile all the cells on instantiation.

        table = self.table
        if datum:
            self.datum = datum
        else:
            datum = self.datum
        cells = []

        # chg Begin
        for column in table.columns.values():
            # svr_apply_cnt
            if column.name == 'service_type'.lower() \
                and (not datum or
                     not hasattr(datum, 'ticket_templates_apply_cnt')):
                LOG.debug('there is no attrs rowspan in cell.')
                continue

            cell = table._meta.cell_class(datum, column, self)
            if column.name == 'service_type'.lower():
                # rowspan
                cell.attrs['rowspan'] = getattr(datum,
                                                'ticket_templates_apply_cnt')
                cell.attrs['style'] = 'background-color:white'
            cells.append((column.name or column.auto, cell))
        # chg    End

        self.cells = SortedDict(cells)

        if self.ajax:
            interval = conf.HORIZON_CONFIG['ajax_poll_interval']
            self.attrs['data-update-interval'] = interval
            self.attrs['data-update-url'] = self.get_ajax_update_url()
            self.classes.append("ajax-update")

        self.attrs['data-object-id'] = table.get_object_id(datum)

        # Add the row's status class and id to the attributes to be rendered.
        self.classes.append(self.status_class)
        id_vals = {"table": self.table.name,
                   "sep": STRING_SEPARATOR,
                   "id": table.get_object_id(datum)}
        self.id = "%(table)s%(sep)srow%(sep)s%(id)s" % id_vals
        self.attrs['id'] = self.id

        # Add the row's display name if available
        display_name = table.get_object_display(datum)
        if display_name:
            self.attrs['data-display'] = escape(display_name)


class TicketTemplatesListContractTable(tables.DataTable):
    """Ticket templates list contract table class"""

    type = tables.Column("ticket_template_name",
                         verbose_name=_("Type"),
                         sortable=False)
    kinds = tables.Column("application_kinds_name",
                          link=get_link_url,
                          verbose_name=_("Request Form"),
                          link_classes=("ajax-modal", "btn-create"),
                          sortable=False)

    def get_object_id(self, ticket_template):
        return ticket_template.target_id

    class Meta(object):
        """Meta class"""

        name = "tickettemplates"
        verbose_name = "Request Menu"

        row_class = TicketTemplatesListRow
        pagination_param = "ticket_templates_contract_marker"


class TicketTemplatesListRequestTable(tables.DataTable):
    """Ticket templates list request table class"""

    type = tables.Column("ticket_template_name",
                         verbose_name=_("Type"),
                         sortable=False)
    kinds = tables.Column("application_kinds_name",
                          link=get_link_url,
                          verbose_name=_("Request Form"),
                          link_classes=("ajax-modal", "btn-create"),
                          sortable=False)

    def get_object_id(self, ticket_template):
        return ticket_template.target_id

    class Meta(object):
        """Meta class"""

        name = "tickettemplates"
        verbose_name = "Request Menu"

        row_class = TicketTemplatesListRow
        pagination_param = "ticket_templates_request_marker"
