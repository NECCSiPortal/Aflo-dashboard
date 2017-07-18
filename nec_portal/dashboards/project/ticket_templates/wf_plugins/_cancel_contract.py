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

from nec_portal.api import ticket
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import plugin as base_plugin


class CancelContract(base_plugin.BasePlugin):
    """Cancel contract class"""

    def set_context_data(
            self, called_object, context, form_template, **kwargs):

        contract, lifetime_end = self._get_contract(
            called_object,
            kwargs['template_contents'].get('target_id'),
            kwargs['template_contents'].get('target_key'),
            called_object.kwargs['contract_id'])

        context['contract'] = contract

        # To disable a submit in the case of contract breakage
        if context['allowed_submit'] and '9999-12-31' not in lifetime_end:
            context['allowed_submit'] = False

    def _get_contract(self,
                      called_object,
                      target_ids,
                      target_keys,
                      contract_id):
        contract = []
        # Get contract detail
        contract_detail = ticket.contract_get_detailed(called_object.request,
                                                       contract_id)
        lifetime_end = contract_detail.lifetime_end

        expansion_text = \
            json.loads(contract_detail.expansions_text['expansion_text'])
        ticket_details = \
            expansion_text['contract_info']['ticket_detail']

        # Get a contract information
        for key, value in ticket_details.items():
            if key == 'message':
                continue

            contract.append({
                'contract_key': key,
                'contract_num': value,
            })

        return contract, lifetime_end
