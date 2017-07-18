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

import json
import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from nec_portal.dashboards.project.contracts \
    import constants

LOG = logging.getLogger(__name__)


class ContractFilterAction(tables.FilterAction):
    """Contract filter action class"""
    filter_type = "server"
    filter_choices = (('ticket_template_name', _('Request Type ='), True),
                      ('parent_contract_id', _('Contract ID ='), True),
                      ('application_name', _('Issuer ='), True),
                      ('application_date', _('Issue Date ='), True),
                      ('lifetime_start', _('Start Date ='), True),
                      ('lifetime_end', _('End Date ='), True),
                      ('lifetime', _('Contracting Date'), True))


class DeleteContract(tables.LinkAction):
    """Delete contract class"""
    name = "delete"
    verbose_name = _("Cancelling")
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, constants=None):
        base_url = ''
        contract = json.loads(constants.expansion_text)
        if contract['ticket_info'] == '':
            return base_url
        elif contract['ticket_info']['cancelling_template'] is not None:
            cancel_info = contract['ticket_info']['cancelling_template']
            url = 'horizon:project:contracts:wf_engine_create:index'
            base_url = reverse(url,
                               args=[cancel_info['id'], constants.contract_id])
        return base_url

    def allowed(self, request, datum):
        contract = json.loads(datum.expansion_text)
        if contract['ticket_info'] == '':
            return False
        return True


def get_contract_end(contract):
    if '2999-12-31' in contract.lifetime_end or \
       '9999-12-31' in contract.lifetime_end or \
       contract.lifetime_end == 'None':
        return '-'

    return getattr(contract, 'lifetime_end', '-')


class ContractTable(tables.DataTable):
    """Contract table class"""
    ticket_template_name = \
        tables.Column('ticket_template_name',
                      verbose_name=_('Request Type'))
    parent_contract_id = tables.Column('parent_contract_id',
                                       verbose_name=_('Contract ID'),
                                       link=constants.CONTRACTS_DETAIL_URL)
    application_name = tables.Column('application_name',
                                     verbose_name=_('Issuer'))
    application_date = tables.Column('application_date',
                                     verbose_name=_('Issue Date'))
    lifetime_start = tables.Column('lifetime_start',
                                   verbose_name=_('Start Date'))
    lifetime_end = tables.Column(get_contract_end,
                                 verbose_name=_('End Date'))

    def get_object_id(self, contract):
        return contract.contract_id

    class Meta(object):
        """Meta class"""
        name = "contracts"
        verbose_name = 'Contracts'

        row_actions = (DeleteContract,)
        multi_select = False

        table_actions = (ContractFilterAction,)
        pagination_param = "contract_marker"
