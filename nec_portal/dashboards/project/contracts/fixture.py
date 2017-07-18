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

"""Contract data detail
CONTRACT_DATA_LIST[0]
CONTRACT_DATA_LIST[1]
CONTRACT_DATA_LIST[2]
CONTRACT_DATA_LIST[3]
CONTRACT_DATA_LIST[4]
CONTRACT_DATA_LIST[5]
"""

json_data = '{"contract_info": {' \
            '     "ticket_detail": {' \
            '         "Bronze vCPU x 10 CORE(S)": 1,' \
            '         "Gold vCPU x 10": 1,' \
            '         "Message": "",' \
            '         "RAM 20 GB": 1,' \
            '         "Silver vCPU x 10 CORE(S)": 1,' \
            '         "Volume Storage 50 GB": 1' \
            '     }' \
            ' },' \
            ' "ticket_info": {' \
            '     "cancelling_template": {' \
            '         "id": "1"' \
            '     }' \
            ' }' \
            '}'

CONTRACT_DATA_LIST = [
    {
        "contract_id": "02262dc1-9906-41bc-822d-426a5ba3f763",
        "region_id": "",
        "project_id": "7a867af0702c435981cfb970998b2337",
        "project_name": "test_project",
        "catalog_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "catalog_name": "test_goods",
        "num": "10",
        "parent_ticket_template_id": "7a867af0702c435981cfb970998b1000",
        "ticket_template_id": "7a867af0702c435981cfb970998b2000",
        "parent_ticket_template_name": "parent_ticket_template_name",
        "ticket_template_name": "ticket_template_name",
        "parent_application_kinds_name": "parent_application_kinds_name",
        "application_kinds_name": "application_kinds_name",
        "cancel_application_id": "7a867af0702c435981cfb970998b3000",
        "application_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "application_name": "application_name",
        "application_date": "2015-08-08T17:51:53.000001",
        "parent_contract_id": "7a867af0702c435981cfb970998b4000",
        "lifetime_start": "2015-08-08T17:51:53.000001",
        "lifetime_end": "2999-12-31T23:59:59.999999",
        "created_at": "2015-08-08T17:51:53.000001",
        "updated_at": "2015-08-08T17:51:53.000001",
        "deleted_at": "",
        "deleted": "",
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5",
        },
        "expansions_text": {
            "expansion_text": json_data
        },
    },
    {
        "contract_id": "02262dc1-9906-41bc-822d-426a5ba3f764",
        "region_id": "",
        "project_id": "7a867af0702c435981cfb970998b2337",
        "project_name": "test_project",
        "catalog_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "catalog_name": "test_goods",
        "num": "10",
        "parent_ticket_template_id": "7a867af0702c435981cfb970998b1000",
        "ticket_template_id": "7a867af0702c435981cfb970998b2000",
        "parent_ticket_template_name": "parent_ticket_template_name",
        "ticket_template_name": "ticket_template_name",
        "parent_application_kinds_name": "parent_application_kinds_name",
        "application_kinds_name": "application_kinds_name",
        "cancel_application_id": "7a867af0702c435981cfb970998b3000",
        "application_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "application_name": "application_name",
        "application_date": "2015-08-08T17:51:53.000001",
        "parent_contract_id": "7a867af0702c435981cfb970998b4000",
        "lifetime_start": "2015-08-08T17:51:53.000001",
        "lifetime_end": "2999-12-31T23:59:59.999999",
        "created_at": "2015-08-08T17:51:53.000001",
        "updated_at": "2015-08-08T17:51:53.000001",
        "deleted_at": "",
        "deleted": "",
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5",
        },
        "expansions_text": {
            "expansion_text": json_data
        },
    },
    {
        "contract_id": "02262dc1-9906-41bc-822d-426a5ba3f765",
        "region_id": "",
        "project_id": "7a867af0702c435981cfb970998b2337",
        "project_name": "test_project",
        "catalog_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "catalog_name": "test_goods",
        "num": "10",
        "parent_ticket_template_id": "7a867af0702c435981cfb970998b1000",
        "ticket_template_id": "7a867af0702c435981cfb970998b2000",
        "parent_ticket_template_name": "parent_ticket_template_name",
        "ticket_template_name": "ticket_template_name",
        "parent_application_kinds_name": "parent_application_kinds_name",
        "application_kinds_name": "application_kinds_name",
        "cancel_application_id": "7a867af0702c435981cfb970998b3000",
        "application_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "application_name": "application_name",
        "application_date": "2015-08-08T17:51:53.000001",
        "parent_contract_id": "7a867af0702c435981cfb970998b4000",
        "lifetime_start": "2015-08-08T17:51:53.000001",
        "lifetime_end": "2999-12-31T23:59:59.999999",
        "created_at": "2015-08-08T17:51:53.000001",
        "updated_at": "2015-08-08T17:51:53.000001",
        "deleted_at": "",
        "deleted": "",
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5",
        },
        "expansions_text": {
            "expansion_text": json_data
        },
    },
    {
        "contract_id": "02262dc1-9906-41bc-822d-426a5ba3f766",
        "region_id": "",
        "project_id": "7a867af0702c435981cfb970998b2337",
        "project_name": "test_project",
        "catalog_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "catalog_name": "test_goods",
        "num": "10",
        "parent_ticket_template_id": "7a867af0702c435981cfb970998b1000",
        "ticket_template_id": "7a867af0702c435981cfb970998b2000",
        "parent_ticket_template_name": "parent_ticket_template_name",
        "ticket_template_name": "ticket_template_name",
        "parent_application_kinds_name": "parent_application_kinds_name",
        "application_kinds_name": "application_kinds_name",
        "cancel_application_id": "7a867af0702c435981cfb970998b3000",
        "application_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "application_name": "application_name",
        "application_date": "2015-08-08T17:51:53.000001",
        "parent_contract_id": "7a867af0702c435981cfb970998b4000",
        "lifetime_start": "2015-08-08T17:51:53.000001",
        "lifetime_end": "2999-12-31T23:59:59.999999",
        "created_at": "2015-08-08T17:51:53.000001",
        "updated_at": "2015-08-08T17:51:53.000001",
        "deleted_at": "",
        "deleted": "",
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5",
        },
        "expansions_text": {
            "expansion_text": json_data
        },
    },
    {
        "contract_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "region_id": "",
        "project_id": "7a867af0702c435981cfb970998b2337",
        "project_name": "test_project",
        "catalog_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "catalog_name": "test_goods",
        "num": "10",
        "parent_ticket_template_id": "7a867af0702c435981cfb970998b1000",
        "ticket_template_id": "7a867af0702c435981cfb970998b2000",
        "parent_ticket_template_name": "parent_ticket_template_name",
        "ticket_template_name": "ticket_template_name",
        "parent_application_kinds_name": "parent_application_kinds_name",
        "application_kinds_name": "application_kinds_name",
        "cancel_application_id": "7a867af0702c435981cfb970998b3000",
        "application_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "application_name": "application_name",
        "application_date": "2015-08-08T17:51:53.000001",
        "parent_contract_id": "7a867af0702c435981cfb970998b4000",
        "lifetime_start": "2015-08-08T17:51:53.000001",
        "lifetime_end": "2999-12-31T23:59:59.999999",
        "created_at": "2015-08-08T17:51:53.000001",
        "updated_at": "2015-08-08T17:51:53.000001",
        "deleted_at": "",
        "deleted": "",
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5",
        },
        "expansions_text": {
            "expansion_text": json_data
        },
    }
]

"""Contract get data detail"""
CONTRACT_GET_DATA = [
    {
        "contract_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "region_id": "",
        "project_id": "7a867af0702c435981cfb970998b2337",
        "project_name": "test_project",
        "catalog_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "catalog_name": "test_goods",
        "num": "10",
        "parent_ticket_template_id": "7a867af0702c435981cfb970998b1000",
        "ticket_template_id": "7a867af0702c435981cfb970998b2000",
        "parent_ticket_template_name": "parent_ticket_template_name",
        "ticket_template_name": "ticket_template_name",
        "parent_application_kinds_name": "parent_application_kinds_name",
        "application_kinds_name": "application_kinds_name",
        "cancel_application_id": "7a867af0702c435981cfb970998b3000",
        "application_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "application_name": "application_name",
        "application_date": "2015-08-08T17:51:53.000001",
        "parent_contract_id": "7a867af0702c435981cfb970998b4000",
        "lifetime_start": "2015-08-08T17:51:53.000001",
        "lifetime_end": "2999-12-31T23:59:59.999999",
        "created_at": "2015-08-08T17:51:53.000001",
        "updated_at": "2015-08-08T17:51:53.000001",
        "deleted_at": "",
        "deleted": "",
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5",
        },
        "expansions_text": {
            "expansion_text": json_data
        }
    }
]


"""Contract id"""
CONTRACT_ID = "02262dc1-9906-41bc-822d-426a5ba3f767"


"""Region contract link setting for nec_portal_settings"""
REGION_CONTRACTS_LINKS = [
    {
        'name': 'RegionPortal(DC1)',
        'root_url': 'https://xxxx/',
        'role': ['T__DC1__ProjectMember']
    },
    {
        'name': 'RegionPortal(DC2)',
        'root_url': 'https://xxxx/',
        'role': ['T__DC2__ProjectMember']
    },
    {
        'name': 'RegionPortal(DC3)',
        'root_url': 'https://xxxx/',
        'role': ['T__DC3__ProjectMember']
    },
]
REGION_CONTRACTS_LINKS_NO_SET_ROLE = [
    {
        'name': 'RegionPortal(DC1)',
        'root_url': 'https://xxxx/',
    },
]
