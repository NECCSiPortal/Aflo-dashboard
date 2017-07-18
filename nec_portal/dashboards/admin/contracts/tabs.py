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

from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from nec_portal.api import ticket as ticket_api


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = "admin/contracts/_detail.html"

    def get_context_data(self, request):
        contract = self.tab_group.kwargs['contract']
        if contract.lifetime_end is None or \
           '2999-12-31' in contract.lifetime_end or \
           '9999-12-31' in contract.lifetime_end:
                contract.lifetime_end = '-'
        else:
            contract.lifetime_end = datetime.datetime.\
                strptime(contract.lifetime_end,
                         '%Y-%m-%dT%H:%M:%S.%f').strftime("%Y-%m-%d %H:%M:%S")
        if contract.lifetime_start is not None:
            contract.lifetime_start = datetime.datetime.\
                strptime(contract.lifetime_start,
                         '%Y-%m-%dT%H:%M:%S.%f').strftime("%Y-%m-%d %H:%M:%S")
        if contract.application_date is not None:
            contract.application_date = datetime.datetime.\
                strptime(contract.application_date,
                         '%Y-%m-%dT%H:%M:%S.%f').strftime("%Y-%m-%d %H:%M:%S")

        catalogs = json.loads(contract.expansions_text['expansion_text'])

        ticket_detail = catalogs['contract_info']['ticket_detail']
        if 'Message' in ticket_detail:
            del ticket_detail['Message']
        elif 'message' in ticket_detail:
            del ticket_detail['message']

        ticket_template_id = contract.ticket_template_id
        ticket_template = ticket_api.tickettemplates_get(
            self.request, ticket_template_id)

        template_contents = ticket_template.template_contents

        ticket_catalog_list = []
        for param_dict in template_contents['create']['parameters']:
            param_key = param_dict['key']
            param_name = param_dict["label"]

            if param_key != "message":
                language_name = param_name.get('Default',
                                               param_name.get('default'))
                language_code = self.request.LANGUAGE_CODE
                if language_code in param_name:
                    language_name = param_name.get(language_code)
                catalog_num = ticket_detail.get(param_key)
                catalog = ContractCatalog(language_name, catalog_num)
                ticket_catalog_list.append(catalog)

        return {"contract": contract,
                "ticket_list": ticket_catalog_list}


class ContractsDetailTabs(tabs.TabGroup):
    slug = "contracts_details"
    tabs = (OverviewTab,)


class ContractCatalog(object):
    """Contract catalog class"""

    def __init__(self,
                 catalog_name,
                 catalog_num):
        self.catalog_name = escape(catalog_name)
        self.catalog_num = escape(catalog_num)
