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

"""Contract tickettemplate data detail
CONTRACT_TICKET_TEMPLATE_DATA_LIST[0]:contract
    inner data of special string : "'<>\%
    id:10
CONTRACT_TICKET_TEMPLATE_DATA_LIST[1]:contracted
    id:11
"""
CONTRACT_TICKET_TEMPLATE_DATA_LIST = [
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "created_at": "2015-09-08T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "10",
        "template_contents": {
            "action": {
                "broker": [
                    {
                        "broker_method":
                            "integrity_check_for_purchase_contract",
                        "status": "awaiting approval",
                        "timing": "before",
                        "validation": "param_check"
                    },
                    {
                        "broker_method": "",
                        "status": "awaiting approval",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "withdrawn",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "withdrawn",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "check",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "check",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "reject",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "reject",
                        "timing": "after"
                    },
                    {
                        "broker_method":
                            "integrity_check_for_purchase_contract",
                        "status": "approval",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method":
                            "contract_data_registration_for_purchase_contract",
                        "status": "approval",
                        "timing": "after"
                    }
                ],
                "broker_class":
                    "aflo.tickets.broker."
                    "sample_set_catalog_monthly.SampleSetCatalogBroker"
            },
            "application_kinds_name": {
                "Default":
                    "Gold VCPU 10, Silver VCPU 10, Bronze VCPU 10, "
                    "RAM 20GB, Volume Storage 50GB",
                "ja":
                    "\"'<>\%\u677e VCPU 10, \u7af9 VCPU 10, \u6885 VCPU 10, "
                    "RAM 20GB, \u30dc\u30ea\u30e5\u30fc"
                    "\u30e0\u30b9\u30c8\u30ec\u30fc\u30b8 50GB"
            },
            "cancelling_template": {
                "id": "11"
            },
            "change_template": {
                "id": "11"
            },
            "first_status_code": "awaiting approval",
            "create": {
                "parameters": [
                    {
                        "key": "vcpu",
                        "label": {
                            "Default": "VCPU x 10 CORE(S)",
                            "ja": "VCPU x 10 CORE(S)"},
                        "type": "number",
                        "constraints": {
                            "required": True,
                            "range": {
                                "max": "9999",
                                "min": "0"
                            }
                        }
                    },
                    {
                        "key": "ram",
                        "label": {
                            "Default": "RAM 20 GB",
                            "ja": "RAM 20 GB"},
                        "type": "number",
                        "constraints": {
                            "required": True,
                            "range": {
                                "max": "9999",
                                "min": "0"
                            }
                        }
                    },
                    {
                        "key": "volume_storage",
                        "label": {
                            "Default": "Volume Storage 50 GB",
                            "ja": "\\u30dc\\u30ea\\u30e5\\u30fc\\u30e0"
                            "\\u30b9\\u30c8\\u30ec\\u30fc\\u30b8 50 GB"},
                        "type": "number",
                        "constraints": {
                            "required": True,
                            "range": {
                                "max": "9999",
                                "min": "0"
                            }
                        }
                    },
                    {
                        "key": "Message",
                        "type": "string",
                        "label": {
                            "Default": "Message",
                            "ja": "\\u30e1\\u30c3\\u30bb\\u30fc\\u30b8"},
                        "constraints": {
                            "length": {
                                "max": "512",
                                "min": "0"
                            }
                        }
                    }
                ]
            },
            "target_id": [
                "catalog0-1111-2222-3333-000000000005",
                "catalog0-1111-2222-3333-000000000002",
                "catalog0-1111-2222-3333-000000000001"
            ],
            "target_key": [
                "vcpu",
                "ram",
                "volume_storage"
            ],
            "ticket_template_name": {
                "Default": "flat-rate",
                "ja": "Quota\u8cb7\u3044"
            },
            "ticket_type": "contract",
            "wf_pattern_code": "contract_workflow"
        },
        "ticket_type": "contract",
        "updated_at": None,
        "workflow_pattern_id": "10"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "created_at": "2015-09-08T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "11",
        "template_contents": {
            "action": {
                "broker": [
                    {
                        "broker_method": "",
                        "status": "awaiting approval",
                        "timing": "before",
                        "validation": "integrity_check_for_cancellation"
                    },
                    {
                        "broker_method": "",
                        "status": "awaiting approval",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "withdrawn",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "withdrawn",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "check",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "check",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "reject",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "reject",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "approval",
                        "timing": "before",
                        "validation": "integrity_check_for_cancellation"
                    },
                    {
                        "broker_method":
                            "contract_data_registration_for_cancellation",
                        "status": "approval",
                        "timing": "after"
                    }
                ],
                "broker_class":
                    "aflo.tickets.broker."
                    "sample_set_catalog_monthly.SampleSetCatalogBroker"
            },
            "application_kinds_name": {
                "Default":
                    "Gold VCPU 10, Silver VCPU 10, Bronze VCPU 10, "
                    "RAM 20GB, Volume Storage 50GB",
                "ja":
                    "\u677e VCPU 10, \u7af9 VCPU 10, \u6885 VCPU 10, "
                    "RAM 20GB, \u30dc\u30ea\u30e5\u30fc"
                    "\u30e0\u30b9\u30c8\u30ec\u30fc\u30b8 50GB"
            },
            "first_status_code": "awaiting approval",
            "create": {"parameters": [
                {
                    "key": "Message",
                    "type": "string",
                    "label": {
                        "Default": "Message",
                        "ja": "\\u30e1\\u30c3\\u30bb\\u30fc\\u30b8"},
                    "constraints": {
                        "length": {
                            "max": "512",
                            "min": "0"
                        }
                    }
                }
            ]},
            "target_id": [
                "catalog0-1111-2222-3333-000000000005",
                "catalog0-1111-2222-3333-000000000002",
                "catalog0-1111-2222-3333-000000000001"
            ],
            "target_key": [
                "vcpu",
                "ram",
                "volume_storage"
            ],
            "ticket_template_name": {
                "Default": "flat-rate",
                "ja": "Quota\u8cb7\u3044"
            },
            "ticket_type": "contracted",
            "wf_pattern_code": "contract_workflow"
        },
        "ticket_type": "contracted",
        "updated_at": None,
        "workflow_pattern_id": "10"
    }
]


"""Contract ticket data detail
CONTRACT_TICKET_DATA_LIST[0]:contract
    last_status_code:awaiting approval
CONTRACT_TICKET_DATA_LIST[1]:contract
    last_status_code:check
CONTRACT_TICKET_DATA_LIST[2]:contract
    last_status_code:approval
CONTRACT_TICKET_DATA_LIST[3]:contracted
    last_status_code:awaiting approval
CONTRACT_TICKET_DATA_LIST[4]:contracted
    last_status_code:check
CONTRACT_TICKET_DATA_LIST[5]:contracted
    last_status_code:approval
"""
CONTRACT_TICKET_DATA_LIST = [
    {
        "roles": [
            "wf_approval",
            "project_manager_b",
            "_member_"
        ],
        "workflow": [
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:14:19.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "2858d1f2-2bd1-4bc9-834b-2d63ea4dd6f3",
                "status": 0,
                "status_code": "reject",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "reject",
                    "status_name": {
                        "Default": "Reject",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "ab3dcc3a-92d6-4729-b715-a38d51f4ac5a",
                "updated_at": "2015-09-28T20:14:19.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": "2015-09-28T20:14:19.000000",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "confirmer_name": "user-a",
                "created_at": "2015-09-28T20:14:19.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "7e7ec23a-a8e7-4c54-994e-a193f9b16893",
                "status": 1,
                "status_code": "awaiting approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "check"
                        },
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "_member_",
                            "next_status_code": "withdrawn"
                        }
                    ],
                    "status_code": "awaiting approval",
                    "status_name": {
                        "Default": "Awaiting Approval",
                        "ja": "\u7533\u8acb\u4e2d"
                    }
                },
                "target_role": "none",
                "ticket_id": "ab3dcc3a-92d6-4729-b715-a38d51f4ac5a",
                "updated_at": "2015-09-28T20:14:19.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:14:19.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "ab0afc54-9cea-4372-b76b-ce6133fa1d9c",
                "status": 0,
                "status_code": "check",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "approval"
                        }
                    ],
                    "status_code": "check",
                    "status_name": {
                        "Default": "Check",
                        "ja": "\u67fb\u95b2"
                    }
                },
                "target_role": "none",
                "ticket_id": "ab3dcc3a-92d6-4729-b715-a38d51f4ac5a",
                "updated_at": "2015-09-28T20:14:19.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:14:19.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "b4ab29cb-8846-4770-b19e-890a78044aa6",
                "status": 0,
                "status_code": "withdrawn",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "withdrawn",
                    "status_name": {
                        "Default": "Withdrawn",
                        "ja": "\u53d6\u308a\u4e0b\u3052"
                    }
                },
                "target_role": "none",
                "ticket_id": "ab3dcc3a-92d6-4729-b715-a38d51f4ac5a",
                "updated_at": "2015-09-28T20:14:19.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:14:19.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "f52e4d9b-29f7-4950-af06-647de7b6f88c",
                "status": 0,
                "status_code": "approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "approval",
                    "status_name": {
                        "Default": "Approval",
                        "ja": "\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "ab3dcc3a-92d6-4729-b715-a38d51f4ac5a",
                "updated_at": "2015-09-28T20:14:19.000000"
            }
        ],
        "action_detail": "",
        "created_at": "2015-09-28T20:14:19.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "ab3dcc3a-92d6-4729-b715-a38d51f4ac5a",
        "last_workflow": {
            "additional_data": "",
            "confirmed_at": "2015-09-28T20:14:19.000000",
            "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
            "confirmer_name": "user-a",
            "created_at": "2015-09-28T20:14:19.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "7e7ec23a-a8e7-4c54-994e-a193f9b16893",
            "status": 1,
            "status_code": "awaiting approval",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "wf_check",
                        "next_status_code": "check"
                    },
                    {
                        "grant_role": "wf_check",
                        "next_status_code": "reject"
                    },
                    {
                        "grant_role": "_member_",
                        "next_status_code": "withdrawn"
                    }
                ],
                "status_code": "awaiting approval",
                "status_name": {
                    "Default": "Awaiting Approval",
                    "ja": "\u7533\u8acb\u4e2d"
                }
            },
            "target_role": "none",
            "ticket_id": "ab3dcc3a-92d6-4729-b715-a38d51f4ac5a",
            "updated_at": "2015-09-28T20:14:19.000000"
        },
        "owner_at": "2015-09-28T20:14:19.000000",
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230",
        "owner_name": "user-a",
        "target_id": [
            "catalog0-1111-2222-3333-000000000005",
            "catalog0-1111-2222-3333-000000000004",
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "tenant_name": "project-a",
        "ticket_detail":
            "{\"Volume Storage 50 GB\": 5, "
            "\"RAM 20 GB\": 4, "
            "\"Silver VCPU x 10 CORE(S)\": 2, "
            "\"Bronze VCPU x 10 CORE(S)\": 3, "
            "\"Gold VCPU x 10 CORE(S)\": 1, "
            "\"Message\": \"registration apply.\"}",
        "ticket_template_id": "10",
        "ticket_type": "contract",
        "updated_at": "2015-09-28T20:14:19.000000"
    },
    {
        "roles": [
            "wf_approval",
            "project_manager_b",
            "_member_"
        ],
        "workflow": [
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:14:58.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "22005c81-6622-4604-b1bc-17c9fcb52f43",
                "status": 0,
                "status_code": "reject",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "reject",
                    "status_name": {
                        "Default": "Reject",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
                "updated_at": "2015-09-28T20:14:58.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": "2015-09-28T20:14:57.000000",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "confirmer_name": "user-a",
                "created_at": "2015-09-28T20:14:58.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "7a480cc5-ee72-4391-a496-fd3e1b70b442",
                "status": 2,
                "status_code": "awaiting approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "check"
                        },
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "_member_",
                            "next_status_code": "withdrawn"
                        }
                    ],
                    "status_code": "awaiting approval",
                    "status_name": {
                        "Default": "Awaiting Approval",
                        "ja": "\u7533\u8acb\u4e2d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
                "updated_at": "2015-09-28T20:16:20.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:14:58.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "8e2257b9-25f7-44db-8faf-e67562773a7b",
                "status": 0,
                "status_code": "withdrawn",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "withdrawn",
                    "status_name": {
                        "Default": "Withdrawn",
                        "ja": "\u53d6\u308a\u4e0b\u3052"
                    }
                },
                "target_role": "none",
                "ticket_id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
                "updated_at": "2015-09-28T20:14:58.000000"
            },
            {
                "additional_data": "{\"Message\": \"check.\"}",
                "confirmed_at": "2015-09-28T20:16:20.000000",
                "confirmer_id": "44f7d4c7b1424cb3a9fc00f704d3beec",
                "confirmer_name": "muser-a",
                "created_at": "2015-09-28T20:14:58.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "8e71ecd1-80cc-4916-a0ac-4fb5aa014c7c",
                "status": 1,
                "status_code": "check",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "approval"
                        }
                    ],
                    "status_code": "check",
                    "status_name": {
                        "Default": "Check",
                        "ja": "\u67fb\u95b2"
                    }
                },
                "target_role": "none",
                "ticket_id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
                "updated_at": "2015-09-28T20:16:20.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:14:58.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "ac48f9da-6d0c-4aaa-b431-414b0c86bbd9",
                "status": 0,
                "status_code": "approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "approval",
                    "status_name": {
                        "Default": "Approval",
                        "ja": "\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
                "updated_at": "2015-09-28T20:14:58.000000"
            }
        ],
        "action_detail": "",
        "created_at": "2015-09-28T20:14:58.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
        "last_workflow": {
            "additional_data": "{\"Message\": \"check.\"}",
            "confirmed_at": "2015-09-28T20:16:20.000000",
            "confirmer_id": "44f7d4c7b1424cb3a9fc00f704d3beec",
            "confirmer_name": "muser-a",
            "created_at": "2015-09-28T20:14:58.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "8e71ecd1-80cc-4916-a0ac-4fb5aa014c7c",
            "status": 1,
            "status_code": "check",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "wf_approval",
                        "next_status_code": "reject"
                    },
                    {
                        "grant_role": "wf_approval",
                        "next_status_code": "approval"
                    }
                ],
                "status_code": "check",
                "status_name": {
                    "Default": "Check",
                    "ja": "\u67fb\u95b2"
                }
            },
            "target_role": "none",
            "ticket_id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
            "updated_at": "2015-09-28T20:16:20.000000"
        },
        "owner_at": "2015-09-28T20:14:57.000000",
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230",
        "owner_name": "user-a",
        "target_id": [
            "catalog0-1111-2222-3333-000000000005",
            "catalog0-1111-2222-3333-000000000004",
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "tenant_name": "project-a",
        "ticket_detail":
            "{\"Volume Storage 50 GB\": 5, "
            "\"RAM 20 GB\": 4, "
            "\"Silver VCPU x 10 CORE(S)\": 2, "
            "\"Bronze VCPU x 10 CORE(S)\": 3, "
            "\"Gold VCPU x 10 CORE(S)\": 1, "
            "\"Message\": \"registration apply check.\"}",
        "ticket_template_id": "10",
        "ticket_type": "contract",
        "updated_at": "2015-09-28T20:14:58.000000"
    },
    {
        "roles": [
            "wf_approval",
            "project_manager_b",
            "_member_"
        ],
        "workflow": [
            {
                "additional_data": "{\"Message\": \"check.\"}",
                "confirmed_at": "2015-09-28T20:16:30.000000",
                "confirmer_id": "44f7d4c7b1424cb3a9fc00f704d3beec",
                "confirmer_name": "muser-a",
                "created_at": "2015-09-28T20:15:18.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "192384c5-7b7b-4806-835e-a82b8c620531",
                "status": 2,
                "status_code": "check",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "approval"
                        }
                    ],
                    "status_code": "check",
                    "status_name": {
                        "Default": "Check",
                        "ja": "\u67fb\u95b2"
                    }
                },
                "target_role": "none",
                "ticket_id": "24961079-b8ff-4c97-b8c5-3a0d1445b46b",
                "updated_at": "2015-09-28T20:17:55.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:15:18.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "1c2c2c40-5291-40e0-921d-d8b4f5a8e769",
                "status": 0,
                "status_code": "reject",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "reject",
                    "status_name": {
                        "Default": "Reject",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "24961079-b8ff-4c97-b8c5-3a0d1445b46b",
                "updated_at": "2015-09-28T20:15:18.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T20:15:18.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "4a79326d-4815-4c83-9827-79bfeb5e6069",
                "status": 0,
                "status_code": "withdrawn",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "withdrawn",
                    "status_name": {
                        "Default": "Withdrawn",
                        "ja": "\u53d6\u308a\u4e0b\u3052"
                    }
                },
                "target_role": "none",
                "ticket_id": "24961079-b8ff-4c97-b8c5-3a0d1445b46b",
                "updated_at": "2015-09-28T20:15:18.000000"
            },
            {
                "additional_data": "{\"Message\": \"approval.\"}",
                "confirmed_at": "2015-09-28T20:17:55.000000",
                "confirmer_id": "63b2288dcdcb4fa7b62cb25c956168c4",
                "confirmer_name": "muser-b",
                "created_at": "2015-09-28T20:15:18.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "c80f74ee-00b1-4713-a286-94c17d9a64fe",
                "status": 1,
                "status_code": "approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "approval",
                    "status_name": {
                        "Default": "Approval",
                        "ja": "\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "24961079-b8ff-4c97-b8c5-3a0d1445b46b",
                "updated_at": "2015-09-28T20:17:55.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": "2015-09-28T20:15:18.000000",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "confirmer_name": "user-a",
                "created_at": "2015-09-28T20:15:18.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "d013297c-3abe-4450-a2e4-4631a49ac597",
                "status": 2,
                "status_code": "awaiting approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "check"
                        },
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "_member_",
                            "next_status_code": "withdrawn"
                        }
                    ],
                    "status_code": "awaiting approval",
                    "status_name": {
                        "Default": "Awaiting Approval",
                        "ja": "\u7533\u8acb\u4e2d"
                    }
                },
                "target_role": "none",
                "ticket_id": "24961079-b8ff-4c97-b8c5-3a0d1445b46b",
                "updated_at": "2015-09-28T20:16:30.000000"
            }
        ],
        "action_detail": "",
        "created_at": "2015-09-28T20:15:18.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "24961079-b8ff-4c97-b8c5-3a0d1445b46b",
        "last_workflow": {
            "additional_data": "{\"Message\": \"approval.\"}",
            "confirmed_at": "2015-09-28T20:17:55.000000",
            "confirmer_id": "63b2288dcdcb4fa7b62cb25c956168c4",
            "confirmer_name": "muser-b",
            "created_at": "2015-09-28T20:15:18.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "c80f74ee-00b1-4713-a286-94c17d9a64fe",
            "status": 1,
            "status_code": "approval",
            "status_detail": {
                "next_status": [
                    {}
                ],
                "status_code": "approval",
                "status_name": {
                    "Default": "Approval",
                    "ja": "\u627f\u8a8d"
                }
            },
            "target_role": "none",
            "ticket_id": "24961079-b8ff-4c97-b8c5-3a0d1445b46b",
            "updated_at": "2015-09-28T20:17:55.000000"
        },
        "owner_at": "2015-09-28T20:15:18.000000",
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230",
        "owner_name": "user-a",
        "target_id": [
            "catalog0-1111-2222-3333-000000000005",
            "catalog0-1111-2222-3333-000000000004",
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "tenant_name": "project-a",
        "ticket_detail":
            "{\"Volume Storage 50 GB\": 5, "
            "\"RAM 20 GB\": 4, "
            "\"Silver VCPU x 10 CORE(S)\": 2, "
            "\"Bronze VCPU x 10 CORE(S)\": 3, "
            "\"Gold VCPU x 10 CORE(S)\": 1, "
            "\"Message\": \"registration apply approval.\"}",
        "ticket_template_id": "10",
        "ticket_type": "contract",
        "updated_at": "2015-09-28T20:15:18.000000"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "additional_data": "",
                "confirmed_at": "2015-09-28T22:08:35.000000",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "confirmer_name": "user-a",
                "created_at": "2015-09-28T22:08:41.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "0ceecbdf-c77e-40ea-ba87-ce7576f7be8f",
                "status": 1,
                "status_code": "awaiting approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "check"
                        },
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "_member_",
                            "next_status_code": "withdrawn"
                        }
                    ],
                    "status_code": "awaiting approval",
                    "status_name": {
                        "Default": "Awaiting Approval",
                        "ja": "\u7533\u8acb\u4e2d"
                    }
                },
                "target_role": "none",
                "ticket_id": "90a60aab-0c88-42c6-8da9-f807d439e4dc",
                "updated_at": "2015-09-28T22:08:41.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:08:42.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "290a0351-6661-4e2d-865b-69139122fa93",
                "status": 0,
                "status_code": "reject",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "reject",
                    "status_name": {
                        "Default": "Reject",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "90a60aab-0c88-42c6-8da9-f807d439e4dc",
                "updated_at": "2015-09-28T22:08:42.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:08:42.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "3f89eb4c-ba6f-45e6-8506-d262d1c08163",
                "status": 0,
                "status_code": "check",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "approval"
                        }
                    ],
                    "status_code": "check",
                    "status_name": {
                        "Default": "Check",
                        "ja": "\u67fb\u95b2"
                    }
                },
                "target_role": "none",
                "ticket_id": "90a60aab-0c88-42c6-8da9-f807d439e4dc",
                "updated_at": "2015-09-28T22:08:42.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:08:42.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "5bed2eb8-665e-4968-af71-53e634663d0b",
                "status": 0,
                "status_code": "withdrawn",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "withdrawn",
                    "status_name": {
                        "Default": "Withdrawn",
                        "ja": "\u53d6\u308a\u4e0b\u3052"
                    }
                },
                "target_role": "none",
                "ticket_id": "90a60aab-0c88-42c6-8da9-f807d439e4dc",
                "updated_at": "2015-09-28T22:08:42.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:08:42.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "bdb3108c-f0e5-49d0-9b00-5fc22b715a71",
                "status": 0,
                "status_code": "approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "approval",
                    "status_name": {
                        "Default": "Approval",
                        "ja": "\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "90a60aab-0c88-42c6-8da9-f807d439e4dc",
                "updated_at": "2015-09-28T22:08:42.000000"
            }
        ],
        "action_detail": "",
        "created_at": "2015-09-28T22:08:41.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "90a60aab-0c88-42c6-8da9-f807d439e4dc",
        "last_workflow": {
            "additional_data": "",
            "confirmed_at": "2015-09-28T22:08:35.000000",
            "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
            "confirmer_name": "user-a",
            "created_at": "2015-09-28T22:08:41.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "0ceecbdf-c77e-40ea-ba87-ce7576f7be8f",
            "status": 1,
            "status_code": "awaiting approval",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "wf_check",
                        "next_status_code": "check"
                    },
                    {
                        "grant_role": "wf_check",
                        "next_status_code": "reject"
                    },
                    {
                        "grant_role": "_member_",
                        "next_status_code": "withdrawn"
                    }
                ],
                "status_code": "awaiting approval",
                "status_name": {
                    "Default": "Awaiting Approval",
                    "ja": "\u7533\u8acb\u4e2d"
                }
            },
            "target_role": "none",
            "ticket_id": "90a60aab-0c88-42c6-8da9-f807d439e4dc",
            "updated_at": "2015-09-28T22:08:41.000000"
        },
        "owner_at": "2015-09-28T22:08:35.000000",
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230",
        "owner_name": "user-a",
        "target_id": [
            "catalog0-1111-2222-3333-000000000005",
            "catalog0-1111-2222-3333-000000000004",
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "tenant_name": "project-a",
        "ticket_detail":
            "{\"Message\": \"cancel apply.\", "
            "\"contract_id\": \"ad89a38a-9b32-4dd4-886e-8249531ce603\"}",
        "ticket_template_id": "11",
        "ticket_type": "contracted",
        "updated_at": "2015-09-28T22:08:41.000000"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:09:03.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "40de5321-df7e-411a-b930-7cfcc02118ed",
                "status": 0,
                "status_code": "approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "approval",
                    "status_name": {
                        "Default": "Approval",
                        "ja": "\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "7200afd4-a75a-4f58-898c-dcccd7e9b7fa",
                "updated_at": "2015-09-28T22:09:03.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:09:03.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "69e15c97-511c-49bb-9e9a-ca57d45d5eb9",
                "status": 0,
                "status_code": "reject",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "reject",
                    "status_name": {
                        "Default": "Reject",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "7200afd4-a75a-4f58-898c-dcccd7e9b7fa",
                "updated_at": "2015-09-28T22:09:03.000000"
            },
            {
                "additional_data": "{\"Message\": \"check.\"}",
                "confirmed_at": "2015-09-28T22:10:08.000000",
                "confirmer_id": "44f7d4c7b1424cb3a9fc00f704d3beec",
                "confirmer_name": "muser-a",
                "created_at": "2015-09-28T22:09:02.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "8629543f-3baa-4f78-90f3-86f9cb1922e4",
                "status": 1,
                "status_code": "check",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "approval"
                        }
                    ],
                    "status_code": "check",
                    "status_name": {
                        "Default": "Check",
                        "ja": "\u67fb\u95b2"
                    }
                },
                "target_role": "none",
                "ticket_id": "7200afd4-a75a-4f58-898c-dcccd7e9b7fa",
                "updated_at": "2015-09-28T22:10:08.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": "2015-09-28T22:09:00.000000",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "confirmer_name": "user-a",
                "created_at": "2015-09-28T22:09:02.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "8bb51221-2950-4baa-ac18-7ad98835fb04",
                "status": 2,
                "status_code": "awaiting approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "check"
                        },
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "_member_",
                            "next_status_code": "withdrawn"
                        }
                    ],
                    "status_code": "awaiting approval",
                    "status_name": {
                        "Default": "Awaiting Approval",
                        "ja": "\u7533\u8acb\u4e2d"
                    }
                },
                "target_role": "none",
                "ticket_id": "7200afd4-a75a-4f58-898c-dcccd7e9b7fa",
                "updated_at": "2015-09-28T22:10:08.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:09:03.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "bff57eae-fd78-4085-b7d9-ec53490a49ac",
                "status": 0,
                "status_code": "withdrawn",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "withdrawn",
                    "status_name": {
                        "Default": "Withdrawn",
                        "ja": "\u53d6\u308a\u4e0b\u3052"
                    }
                },
                "target_role": "none",
                "ticket_id": "7200afd4-a75a-4f58-898c-dcccd7e9b7fa",
                "updated_at": "2015-09-28T22:09:03.000000"
            }
        ],
        "action_detail": "",
        "created_at": "2015-09-28T22:09:02.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "7200afd4-a75a-4f58-898c-dcccd7e9b7fa",
        "last_workflow": {
            "additional_data": "{\"Message\": \"check.\"}",
            "confirmed_at": "2015-09-28T22:10:08.000000",
            "confirmer_id": "44f7d4c7b1424cb3a9fc00f704d3beec",
            "confirmer_name": "muser-a",
            "created_at": "2015-09-28T22:09:02.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "8629543f-3baa-4f78-90f3-86f9cb1922e4",
            "status": 1,
            "status_code": "check",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "wf_approval",
                        "next_status_code": "reject"
                    },
                    {
                        "grant_role": "wf_approval",
                        "next_status_code": "approval"
                    }
                ],
                "status_code": "check",
                "status_name": {
                    "Default": "Check",
                    "ja": "\u67fb\u95b2"
                }
            },
            "target_role": "none",
            "ticket_id": "7200afd4-a75a-4f58-898c-dcccd7e9b7fa",
            "updated_at": "2015-09-28T22:10:08.000000"
        },
        "owner_at": "2015-09-28T22:09:00.000000",
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230",
        "owner_name": "user-a",
        "target_id": [
            "catalog0-1111-2222-3333-000000000005",
            "catalog0-1111-2222-3333-000000000004",
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "tenant_name": "project-a",
        "ticket_detail":
            "{\"Message\": \"cancel check.\", "
            "\"contract_id\": \"3ac86a31-a03e-4713-a909-a4422091cded\"}",
        "ticket_template_id": "11",
        "ticket_type": "contracted",
        "updated_at": "2015-09-28T22:09:02.000000"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "additional_data": "",
                "confirmed_at": "2015-09-28T22:09:19.000000",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "confirmer_name": "user-a",
                "created_at": "2015-09-28T22:09:20.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "087d4028-ffe1-4979-b2e8-d03f11e01f7b",
                "status": 2,
                "status_code": "awaiting approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "check"
                        },
                        {
                            "grant_role": "wf_check",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "_member_",
                            "next_status_code": "withdrawn"
                        }
                    ],
                    "status_code": "awaiting approval",
                    "status_name": {
                        "Default": "Awaiting Approval",
                        "ja": "\u7533\u8acb\u4e2d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1812d5c2-e7bc-4623-8b92-fd1fcd0d097c",
                "updated_at": "2015-09-28T22:10:23.000000"
            },
            {
                "additional_data": "{\"Message\": \"approval.\"}",
                "confirmed_at": "2015-09-28T22:11:02.000000",
                "confirmer_id": "63b2288dcdcb4fa7b62cb25c956168c4",
                "confirmer_name": "muser-b",
                "created_at": "2015-09-28T22:09:20.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "68b90dcc-8d29-4099-884a-fce848163de2",
                "status": 1,
                "status_code": "approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "approval",
                    "status_name": {
                        "Default": "Approval",
                        "ja": "\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1812d5c2-e7bc-4623-8b92-fd1fcd0d097c",
                "updated_at": "2015-09-28T22:11:04.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:09:20.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "8a674c55-c85b-438b-b44f-7fedd45e473f",
                "status": 0,
                "status_code": "withdrawn",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "withdrawn",
                    "status_name": {
                        "Default": "Withdrawn",
                        "ja": "\u53d6\u308a\u4e0b\u3052"
                    }
                },
                "target_role": "none",
                "ticket_id": "1812d5c2-e7bc-4623-8b92-fd1fcd0d097c",
                "updated_at": "2015-09-28T22:09:20.000000"
            },
            {
                "additional_data": "{\"Message\": \"check.\"}",
                "confirmed_at": "2015-09-28T22:10:22.000000",
                "confirmer_id": "44f7d4c7b1424cb3a9fc00f704d3beec",
                "confirmer_name": "muser-a",
                "created_at": "2015-09-28T22:09:20.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "b0d2729b-765c-4098-9503-895597676517",
                "status": 2,
                "status_code": "check",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "reject"
                        },
                        {
                            "grant_role": "wf_approval",
                            "next_status_code": "approval"
                        }
                    ],
                    "status_code": "check",
                    "status_name": {
                        "Default": "Check",
                        "ja": "\u67fb\u95b2"
                    }
                },
                "target_role": "none",
                "ticket_id": "1812d5c2-e7bc-4623-8b92-fd1fcd0d097c",
                "updated_at": "2015-09-28T22:11:04.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2015-09-28T22:09:20.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "d97d8cd7-b5f5-4035-86e2-b3d97b5dea11",
                "status": 0,
                "status_code": "reject",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "reject",
                    "status_name": {
                        "Default": "Reject",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1812d5c2-e7bc-4623-8b92-fd1fcd0d097c",
                "updated_at": "2015-09-28T22:09:20.000000"
            }
        ],
        "action_detail": "",
        "created_at": "2015-09-28T22:09:20.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "1812d5c2-e7bc-4623-8b92-fd1fcd0d097c",
        "last_workflow": {
            "additional_data": "{\"Message\": \"approval.\"}",
            "confirmed_at": "2015-09-28T22:11:02.000000",
            "confirmer_id": "63b2288dcdcb4fa7b62cb25c956168c4",
            "confirmer_name": "muser-b",
            "created_at": "2015-09-28T22:09:20.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "68b90dcc-8d29-4099-884a-fce848163de2",
            "status": 1,
            "status_code": "approval",
            "status_detail": {
                "next_status": [
                    {}
                ],
                "status_code": "approval",
                "status_name": {
                    "Default": "Approval",
                    "ja": "\u627f\u8a8d"
                }
            },
            "target_role": "none",
            "ticket_id": "1812d5c2-e7bc-4623-8b92-fd1fcd0d097c",
            "updated_at": "2015-09-28T22:11:04.000000"
        },
        "owner_at": "2015-09-28T22:09:19.000000",
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230",
        "owner_name": "user-a",
        "target_id": [
            "catalog0-1111-2222-3333-000000000005",
            "catalog0-1111-2222-3333-000000000004",
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "tenant_name": "project-a",
        "ticket_detail":
            "{\"Message\": \"cancel approval.\", "
            "\"contract_id\": \"7ca8409f-2024-4960-a69d-c8911ce08f65\"}",
        "ticket_template_id": "11",
        "ticket_type": "contracted",
        "updated_at": "2015-09-28T22:09:20.000000"
    }
]


"""Approval flags detail
APPROVAL_FLAGS[0]:
    next_status_code:check last_status_code:awaiting approval
APPROVAL_FLAGS[1]:
    next_status_code:reject last_status_code:awaiting approval
APPROVAL_FLAGS[2]:
    next_status_code:withdrawn last_status_code:awaiting approval
APPROVAL_FLAGS[3]:
    next_status_code:approval last_status_code:check
"""
APPROVAL_FLAGS = \
    [[('check:'
       '772a52569-8d9a-4156-b5a9-357a09181320:'
       'awaiting approval:'
       '0a8dfe64-0e20-4add-b870-029d4f687d39'), u'Check'],
     [('reject:'
       '0e6ae7ee-e703-4916-8785-8b440638a709:'
       'awaiting approval:'
       '0a8dfe64-0e20-4add-b870-029d4f687d39'), u'Reject'],
     [('withdrawn:'
       '8dae74e0-f1e4-4703-a274-308d72217061:'
       'awaiting approval:'
       '0a8dfe64-0e20-4add-b870-029d4f687d39'), u'Awaiting approval'],
     [('approval:'
       '33c824ca-7ec8-44de-ba35-364cb9a380df:'
       'check:'
       '72a52569-8d9a-4156-b5a9-357a09181320'), u'Approval']]


"""Project get data detail
PROJECT_GET_DATA:project a
"""
PROJECT_GET_DATA = {
    "enabled": True,
    "description": "project a",
    "name": "project-a",
    "id": "7a867af0702c435981cfb970998b2337"
}


"""Request tickettemplate data detail
REQUEST_TICKET_TEMPLATE_DATA_LIST[0]:request_user_entry
    id:20
REQUEST_TICKET_TEMPLATE_DATA_LIST[1]:request_contact
    id:21
"""
REQUEST_TICKET_TEMPLATE_DATA_LIST = [
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "deleted": False,
        "created_at": "2015-09-08T00:00:00.000000",
        "updated_at": None,
        "workflow_pattern_id": "20",
        "ticket_type": "request",
        "id": "20",
        "deleted_at": None,
        "template_contents": {
            "wf_pattern_code": "request_workflow",
            "ticket_type": "request",
            "target_id": "",
            "create": {"parameters": [
                {
                    "key": "Message",
                    "type": "string",
                    "label": {
                        "Default": "Message",
                        "ja": "\\u30e1\\u30c3\\u30bb\\u30fc\\u30b8"},
                    "constraints": {
                        "length": {
                            "max": "512",
                            "min": "0"
                        }
                    }
                }
            ]},
            "first_status_code": "inquiring",
            "application_kinds_name": {
                "Default": "Request User Entry",
                "ja": "\u30e6\u30fc\u30b6\u30fc\u767b\u9332\u7533\u8acb"
            },
            "action": {
                "broker_class":
                    "aflo.tickets.broker."
                    "common_request_handler.UserEntryRequestHandler",
                "broker": [
                    {
                        "status": "inquiring",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "inquiring",
                        "timing": "after",
                        "validation": "",
                        "broker_method": "mail_to_support"
                    },
                    {
                        "status": "working",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "working",
                        "timing": "after",
                        "validation": "",
                        "broker_method": "mail_to_member"
                    },
                    {
                        "status": "close request",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "close request",
                        "timing": "after",
                        "validation": "",
                        "broker_method": "mail_to_member"
                    },
                    {
                        "status": "close",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "close",
                        "timing": "after",
                        "validation": "",
                        "broker_method": ""
                    }
                ]
            },
            "ticket_template_name": {
                "Default": "Work Request",
                "ja": "\u4f5c\u696d\u4f9d\u983c"
            },
        }
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "deleted": False,
        "created_at": "2015-09-08T00:00:00.000000",
        "updated_at": None,
        "workflow_pattern_id": "20",
        "ticket_type": "request",
        "id": "21",
        "deleted_at": None,
        "template_contents": {
            "wf_pattern_code": "request_workflow",
            "ticket_type": "request",
            "target_id": "",
            "create": {"parameters": [
                {
                    "key": "Message",
                    "type": "string",
                    "label": {
                        "Default": "Message",
                        "ja": "\\u30e1\\u30c3\\u30bb\\u30fc\\u30b8"},
                    "constraints": {
                        "length": {
                            "max": "512",
                            "min": "1"
                        }
                    }
                }
            ]},
            "first_status_code": "inquiring",
            "application_kinds_name": {
                "Default": "Other Request",
                "ja": "\u304a\u554f\u3044\u5408\u308f\u305b"
            },
            "action": {
                "broker_class":
                    "aflo.tickets.broker."
                    "common_request_handler.CommonRequestHandler",
                "broker": [
                    {
                        "status": "inquiring",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "inquiring",
                        "timing": "after",
                        "validation": "",
                        "broker_method": "mail_to_support"
                    },
                    {
                        "status": "working",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "working",
                        "timing": "after",
                        "validation": "",
                        "broker_method": "mail_to_member"
                    },
                    {
                        "status": "close request",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "close request",
                        "timing": "after",
                        "validation": "",
                        "broker_method": "mail_to_member"
                    },
                    {
                        "status": "close",
                        "timing": "before",
                        "validation": "param_check",
                        "broker_method": ""
                    },
                    {
                        "status": "close",
                        "timing": "after",
                        "validation": "",
                        "broker_method": ""
                    }
                ]
            },
            "ticket_template_name": {
                "Default": "Other Request",
                "ja": "\u304a\u554f\u3044\u5408\u308f\u305b"
            },
        }
    }
]


"""Request ticket data detail
REQUEST_TICKET_DATA_LIST[0]:request_user_entry
    last_status_code:inquiring
REQUEST_TICKET_DATA_LIST[1]:request_contact
    last_status_code:inquiring
REQUEST_TICKET_DATA_LIST[2]:request_user_entry
    last_status_code:close request
REQUEST_TICKET_DATA_LIST[3]:request_contact
    last_status_code:close request
REQUEST_TICKET_DATA_LIST[4]:request_user_entry
    last_status_code:approval
REQUEST_TICKET_DATA_LIST[5]:request_contact
    last_status_code:approval
"""
REQUEST_TICKET_DATA_LIST = [
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "status": 1,
                "deleted_at": None,
                "confirmer_name": "user-a",
                "deleted": False,
                "status_code": "inquiring",
                "created_at": "2015-09-24T13:38:11.000000",
                "updated_at": "2015-09-24T13:38:11.000000",
                "status_detail": {
                    "status_code": "inquiring",
                    "status_name": {
                        "Default": "Inquiring",
                        "ja": "\u4f9d\u983c\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "working",
                            "grant_role": "wf_request_support"
                        },
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "634aa838-e010-4f57-bf29-f721e868d11b",
                "confirmed_at": "2015-09-24T13:38:07.000000",
                "id": "5321dd80-e8ce-49a4-afa5-ab1d3ac29f25",
                "additional_data": "",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "close",
                "created_at": "2015-09-24T13:38:11.000000",
                "updated_at": "2015-09-24T13:38:11.000000",
                "status_detail": {
                    "status_code": "close",
                    "status_name": {
                        "Default": "Close",
                        "ja": "\u30af\u30ed\u30fc\u30ba"
                    },
                    "next_status": [{}]
                },
                "ticket_id": "634aa838-e010-4f57-bf29-f721e868d11b",
                "confirmed_at": None,
                "id": "77f19546-d689-453d-92a5-7fa9992ee5c8",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "working",
                "created_at": "2015-09-24T13:38:11.000000",
                "updated_at": "2015-09-24T13:38:11.000000",
                "status_detail": {
                    "status_code": "working",
                    "status_name": {
                        "Default": "Working",
                        "ja": "\u4f5c\u696d\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "634aa838-e010-4f57-bf29-f721e868d11b",
                "confirmed_at": None,
                "id": "b60b7aef-411d-4f76-939f-0a1e7d2ec6c1",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "close request",
                "created_at": "2015-09-24T13:38:11.000000",
                "updated_at": "2015-09-24T13:38:11.000000",
                "status_detail": {
                    "status_code": "close request",
                    "status_name": {
                        "Default": "Close Request",
                        "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close",
                            "grant_role": "_member_"
                        }
                    ]
                },
                "ticket_id": "634aa838-e010-4f57-bf29-f721e868d11b",
                "confirmed_at": None,
                "id": "fc642934-3c61-4c1e-ba63-617427143211",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            }
        ],
        "ticket_template_id": "20",
        "deleted": False,
        "tenant_name": "project-a",
        "target_id": "",
        "updated_at": "2015-09-24T13:38:11.000000",
        "owner_name": "user-a",
        "owner_at": "2015-09-24T13:38:07.000000",
        "deleted_at": None,
        "ticket_detail":
            "{\"Message\": \"request user entry.\", "
            "\"Role\": [\"wf_check\"], "
            "\"Email\": \"aflo@xxx.com\", "
            "\"User Name\": \"request user\"}",
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "created_at": "2015-09-24T13:38:11.000000",
        "id": "634aa838-e010-4f57-bf29-f721e868d11b",
        "ticket_type": "request",
        "action_detail": "",
        "last_workflow": {
            "status": 1,
            "deleted_at": None,
            "confirmer_name": "user-a",
            "deleted": False,
            "status_code": "inquiring",
            "created_at": "2015-09-24T13:38:11.000000",
            "updated_at": "2015-09-24T13:38:11.000000",
            "status_detail": {
                "status_code": "inquiring",
                "status_name": {
                    "Default": "Inquiring",
                    "ja": "\u4f9d\u983c\u4e2d"
                },
                "next_status": [
                    {
                        "next_status_code": "working",
                        "grant_role": "wf_request_support"
                    },
                    {
                        "next_status_code": "close request",
                        "grant_role": "wf_request_support"
                    }
                ]
            },
            "ticket_id": "634aa838-e010-4f57-bf29-f721e868d11b",
            "confirmed_at": "2015-09-24T13:38:07.000000",
            "id": "5321dd80-e8ce-49a4-afa5-ab1d3ac29f25",
            "additional_data": "",
            "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
            "target_role": "none"
        },
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "status": 1,
                "deleted_at": None,
                "confirmer_name": "user-a",
                "deleted": False,
                "status_code": "inquiring",
                "created_at": "2015-09-24T13:38:24.000000",
                "updated_at": "2015-09-24T13:38:24.000000",
                "status_detail": {
                    "status_code": "inquiring",
                    "status_name": {
                        "Default": "Inquiring",
                        "ja": "\u4f9d\u983c\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "working",
                            "grant_role": "wf_request_support"
                        },
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "82aa7d90-6873-4558-a277-e2445cb983c2",
                "confirmed_at": "2015-09-24T13:38:23.000000",
                "id": "5ef55c09-cae7-45ae-a4e7-c4ca76240e71",
                "additional_data": "",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "working",
                "created_at": "2015-09-24T13:38:24.000000",
                "updated_at": "2015-09-24T13:38:24.000000",
                "status_detail": {
                    "status_code": "working",
                    "status_name": {
                        "Default": "Working",
                        "ja": "\u4f5c\u696d\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "82aa7d90-6873-4558-a277-e2445cb983c2",
                "confirmed_at": None,
                "id": "60cefb36-dcab-4271-a8cb-3a3064c1d96c",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "close",
                "created_at": "2015-09-24T13:38:24.000000",
                "updated_at": "2015-09-24T13:38:24.000000",
                "status_detail": {
                    "status_code": "close",
                    "status_name": {
                        "Default": "Close",
                        "ja": "\u30af\u30ed\u30fc\u30ba"
                    },
                    "next_status": [{}]
                },
                "ticket_id": "82aa7d90-6873-4558-a277-e2445cb983c2",
                "confirmed_at": None,
                "id": "63ce5e0c-bf57-4601-a6a8-3e64d935f96d",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "close request",
                "created_at": "2015-09-24T13:38:24.000000",
                "updated_at": "2015-09-24T13:38:24.000000",
                "status_detail": {
                    "status_code": "close request",
                    "status_name": {
                        "Default": "Close Request",
                        "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close",
                            "grant_role": "_member_"
                        }
                    ]
                },
                "ticket_id": "82aa7d90-6873-4558-a277-e2445cb983c2",
                "confirmed_at": None,
                "id": "b6259419-b284-44a3-9e74-1cb360848e40",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            }
        ],
        "ticket_template_id": "21",
        "deleted": False,
        "tenant_name": "project-a",
        "target_id": "",
        "updated_at": "2015-09-24T13:38:24.000000",
        "owner_name": "user-a",
        "owner_at": "2015-09-24T13:38:23.000000",
        "deleted_at": None,
        "ticket_detail": "{\"Message\": \"contact.\"}",
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "created_at": "2015-09-24T13:38:24.000000",
        "id": "82aa7d90-6873-4558-a277-e2445cb983c2",
        "ticket_type": "request",
        "action_detail": "",
        "last_workflow": {
            "status": 1,
            "deleted_at": None,
            "confirmer_name": "user-a",
            "deleted": False,
            "status_code": "inquiring",
            "created_at": "2015-09-24T13:38:24.000000",
            "updated_at": "2015-09-24T13:38:24.000000",
            "status_detail": {
                "status_code": "inquiring",
                "status_name": {
                    "Default": "Inquiring",
                    "ja": "\u4f9d\u983c\u4e2d"
                },
                "next_status": [
                    {
                        "next_status_code": "working",
                        "grant_role": "wf_request_support"
                    },
                    {
                        "next_status_code": "close request",
                        "grant_role": "wf_request_support"
                    }
                ]
            },
            "ticket_id": "82aa7d90-6873-4558-a277-e2445cb983c2",
            "confirmed_at": "2015-09-24T13:38:23.000000",
            "id": "5ef55c09-cae7-45ae-a4e7-c4ca76240e71",
            "additional_data": "",
            "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
            "target_role": "none"
        },
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "working",
                "created_at": "2015-09-24T16:00:35.000000",
                "updated_at": "2015-09-24T16:00:35.000000",
                "status_detail": {
                    "status_code": "working",
                    "status_name": {
                        "Default": "Working",
                        "ja": "\u4f5c\u696d\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "c5b0af42-7f6e-4fb2-8abc-be4ee47c424b",
                "confirmed_at": None,
                "id": "34d1cc8e-48d0-42f6-bc73-5b8e8823f4be",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            },
            {
                "status": 1,
                "deleted_at": None,
                "confirmer_name": "suser-a",
                "deleted": False,
                "status_code": "close request",
                "created_at": "2015-09-24T16:00:35.000000",
                "updated_at": "2015-09-24T16:02:01.000000",
                "status_detail": {
                    "status_code": "close request",
                    "status_name": {
                        "Default": "Close Request",
                        "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close",
                            "grant_role": "_member_"
                        }
                    ]
                },
                "ticket_id": "c5b0af42-7f6e-4fb2-8abc-be4ee47c424b",
                "confirmed_at": "2015-09-24T16:01:59.000000",
                "id": "3637af4b-fc0f-4555-8a28-49ef0e4888d4",
                "additional_data": "{\"Message\": \"close request.\"}",
                "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
                "target_role": "none"
            },
            {
                "status": 2,
                "deleted_at": None,
                "confirmer_name": "user-a",
                "deleted": False,
                "status_code": "inquiring",
                "created_at": "2015-09-24T16:00:35.000000",
                "updated_at": "2015-09-24T16:02:01.000000",
                "status_detail": {
                    "status_code": "inquiring",
                    "status_name": {
                        "Default": "Inquiring",
                        "ja": "\u4f9d\u983c\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "working",
                            "grant_role": "wf_request_support"
                        },
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "c5b0af42-7f6e-4fb2-8abc-be4ee47c424b",
                "confirmed_at": "2015-09-24T16:00:30.000000",
                "id": "882deb35-dacf-4148-bbb0-0361e107c14a",
                "additional_data": "",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "close",
                "created_at": "2015-09-24T16:00:35.000000",
                "updated_at": "2015-09-24T16:00:35.000000",
                "status_detail": {
                    "status_code": "close",
                    "status_name": {
                        "Default": "Close",
                        "ja": "\u30af\u30ed\u30fc\u30ba"
                    },
                    "next_status": [{}]
                },
                "ticket_id": "c5b0af42-7f6e-4fb2-8abc-be4ee47c424b",
                "confirmed_at": None,
                "id": "c1cb84d2-fdcd-41fe-bdbd-69da565ebba9",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            }
        ],
        "ticket_template_id": "20",
        "deleted": False,
        "tenant_name": "project-a",
        "target_id": "",
        "updated_at": "2015-09-24T16:00:33.000000",
        "owner_name": "user-a",
        "owner_at": "2015-09-24T16:00:30.000000",
        "deleted_at": None,
        "ticket_detail":
            "{\"Message\": \"last status is close request and no role.\", "
            "\"Role\": [], "
            "\"Email\": \"aflo@xxx.com\", "
            "\"User Name\": \"close request user\"}",
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "created_at": "2015-09-24T16:00:33.000000",
        "id": "c5b0af42-7f6e-4fb2-8abc-be4ee47c424b",
        "ticket_type": "request",
        "action_detail": "",
        "last_workflow": {
            "status": 1,
            "deleted_at": None,
            "confirmer_name": "suser-a",
            "deleted": False,
            "status_code": "close request",
            "created_at": "2015-09-24T16:00:35.000000",
            "updated_at": "2015-09-24T16:02:01.000000",
            "status_detail": {
                "status_code": "close request",
                "status_name": {
                    "Default": "Close Request",
                    "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                },
                "next_status": [
                    {
                        "next_status_code": "close",
                        "grant_role": "_member_"
                    }
                ]
            },
            "ticket_id": "c5b0af42-7f6e-4fb2-8abc-be4ee47c424b",
            "confirmed_at": "2015-09-24T16:01:59.000000",
            "id": "3637af4b-fc0f-4555-8a28-49ef0e4888d4",
            "additional_data": "{\"Message\": \"close request.\"}",
            "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
            "target_role": "none"
        },
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "close",
                "created_at": "2015-09-24T16:02:57.000000",
                "updated_at": "2015-09-24T16:02:57.000000",
                "status_detail": {
                    "status_code": "close",
                    "status_name": {
                        "Default": "Close",
                        "ja": "\u30af\u30ed\u30fc\u30ba"
                    },
                    "next_status": [{}]
                },
                "ticket_id": "cebcab5c-35fc-4c4b-b5b2-2c26a3888ded",
                "confirmed_at": None,
                "id": "05ee3e8c-1851-47dc-8b64-1aecf84332f2",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            },
            {
                "status": 1,
                "deleted_at": None,
                "confirmer_name": "suser-a",
                "deleted": False,
                "status_code": "close request",
                "created_at": "2015-09-24T16:02:57.000000",
                "updated_at": "2015-09-24T16:14:06.000000",
                "status_detail": {
                    "status_code": "close request",
                    "status_name": {
                        "Default": "Close Request",
                        "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close",
                            "grant_role": "_member_"
                        }
                    ]
                },
                "ticket_id": "cebcab5c-35fc-4c4b-b5b2-2c26a3888ded",
                "confirmed_at": "2015-09-24T16:14:05.000000",
                "id": "37c28da2-c7b5-4169-aa5d-ad674cd56ed6",
                "additional_data": "{\"Message\": \"close request.\"}",
                "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
                "target_role": "none"
            },
            {
                "status": 2,
                "deleted_at": None,
                "confirmer_name": "user-a",
                "deleted": False,
                "status_code": "inquiring",
                "created_at": "2015-09-24T16:02:57.000000",
                "updated_at": "2015-09-24T16:14:06.000000",
                "status_detail": {
                    "status_code": "inquiring",
                    "status_name": {
                        "Default": "Inquiring",
                        "ja": "\u4f9d\u983c\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "working",
                            "grant_role": "wf_request_support"
                        },
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "cebcab5c-35fc-4c4b-b5b2-2c26a3888ded",
                "confirmed_at": "2015-09-24T16:02:57.000000",
                "id": "8084703c-57e0-49c5-bbca-26dc04262b5e",
                "additional_data": "",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "working",
                "created_at": "2015-09-24T16:02:57.000000",
                "updated_at": "2015-09-24T16:02:57.000000",
                "status_detail": {
                    "status_code": "working",
                    "status_name": {
                        "Default": "Working",
                        "ja": "\u4f5c\u696d\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "cebcab5c-35fc-4c4b-b5b2-2c26a3888ded",
                "confirmed_at": None,
                "id": "c740e054-1948-4a27-9165-e1f70f3d370b",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            }
        ],
        "ticket_template_id": "21",
        "deleted": False,
        "tenant_name": "project-a",
        "target_id": "",
        "updated_at": "2015-09-24T16:02:57.000000",
        "owner_name": "user-a",
        "owner_at": "2015-09-24T16:02:57.000000",
        "deleted_at": None,
        "ticket_detail": "{\"Message\": \"last status is close request.\"}",
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "created_at": "2015-09-24T16:02:57.000000",
        "id": "cebcab5c-35fc-4c4b-b5b2-2c26a3888ded",
        "ticket_type": "request",
        "action_detail": "",
        "last_workflow": {
            "status": 1,
            "deleted_at": None,
            "confirmer_name": "suser-a",
            "deleted": False,
            "status_code": "close request",
            "created_at": "2015-09-24T16:02:57.000000",
            "updated_at": "2015-09-24T16:14:06.000000",
            "status_detail": {
                "status_code": "close request",
                "status_name": {
                    "Default": "Close Request",
                    "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                },
                "next_status": [
                    {
                        "next_status_code": "close",
                        "grant_role": "_member_"
                    }
                ]
            },
            "ticket_id": "cebcab5c-35fc-4c4b-b5b2-2c26a3888ded",
            "confirmed_at": "2015-09-24T16:14:05.000000",
            "id": "37c28da2-c7b5-4169-aa5d-ad674cd56ed6",
            "additional_data": "{\"Message\": \"close request.\"}",
            "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
            "target_role": "none"
        },
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "status": 2,
                "deleted_at": None,
                "confirmer_name": "suser-a",
                "deleted": False,
                "status_code": "close request",
                "created_at": "2015-09-24T16:10:58.000000",
                "updated_at": "2015-09-24T16:15:51.000000",
                "status_detail": {
                    "status_code": "close request",
                    "status_name": {
                        "Default": "Close Request",
                        "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close",
                            "grant_role": "_member_"
                        }
                    ]
                },
                "ticket_id": "a105e8e0-d179-49c2-b67f-930a9b2cbbbf",
                "confirmed_at": "2015-09-24T16:14:38.000000",
                "id": "698fa183-2270-4b3c-899e-9c2f2699e1eb",
                "additional_data": "{\"Message\": \"close request.\"}",
                "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
                "target_role": "none"
            },
            {
                "status": 2,
                "deleted_at": None,
                "confirmer_name": "user-a",
                "deleted": False,
                "status_code": "inquiring",
                "created_at": "2015-09-24T16:10:58.000000",
                "updated_at": "2015-09-24T16:14:39.000000",
                "status_detail": {
                    "status_code": "inquiring",
                    "status_name": {
                        "Default": "Inquiring",
                        "ja": "\u4f9d\u983c\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "working",
                            "grant_role": "wf_request_support"
                        },
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "a105e8e0-d179-49c2-b67f-930a9b2cbbbf",
                "confirmed_at": "2015-09-24T16:10:57.000000",
                "id": "6ab52c8f-b814-4054-9677-0affcbb3eb26",
                "additional_data": "",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "target_role": "none"
            },
            {
                "status": 1,
                "deleted_at": None,
                "confirmer_name": "suser-a",
                "deleted": False,
                "status_code": "close",
                "created_at": "2015-09-24T16:10:58.000000",
                "updated_at": "2015-09-24T16:15:51.000000",
                "status_detail": {
                    "status_code": "close",
                    "status_name": {
                        "Default": "Close",
                        "ja": "\u30af\u30ed\u30fc\u30ba"
                    },
                    "next_status": [{}]
                },
                "ticket_id": "a105e8e0-d179-49c2-b67f-930a9b2cbbbf",
                "confirmed_at": "2015-09-24T16:15:51.000000",
                "id": "a5d5830c-a5c3-4ce7-9bb7-665e455c023c",
                "additional_data": "{\"Message\": \"close.\"}",
                "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "working",
                "created_at": "2015-09-24T16:10:58.000000",
                "updated_at": "2015-09-24T16:10:58.000000",
                "status_detail": {
                    "status_code": "working",
                    "status_name": {
                        "Default": "Working",
                        "ja": "\u4f5c\u696d\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "a105e8e0-d179-49c2-b67f-930a9b2cbbbf",
                "confirmed_at": None,
                "id": "b884b85c-7263-4dcd-9dbe-c72dc3b02e92",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            }
        ],
        "ticket_template_id": "20",
        "deleted": False,
        "tenant_name": "project-a",
        "target_id": "",
        "updated_at": "2015-09-24T16:10:58.000000",
        "owner_name": "user-a",
        "owner_at": "2015-09-24T16:10:57.000000",
        "deleted_at": None,
        "ticket_detail":
            "{\"Message\": \"last status is close and no role.\", "
            "\"Role\": [], "
            "\"Email\": \"aflo@xxx.com\", "
            "\"User Name\": \"close user\"}",
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "created_at": "2015-09-24T16:10:58.000000",
        "id": "a105e8e0-d179-49c2-b67f-930a9b2cbbbf",
        "ticket_type": "request",
        "action_detail": "",
        "last_workflow": {
            "status": 1,
            "deleted_at": None,
            "confirmer_name": "suser-a",
            "deleted": False,
            "status_code": "close",
            "created_at": "2015-09-24T16:10:58.000000",
            "updated_at": "2015-09-24T16:15:51.000000",
            "status_detail": {
                "status_code": "close",
                "status_name": {
                    "Default": "Close",
                    "ja": "\u30af\u30ed\u30fc\u30ba"
                },
                "next_status": [{}]
            },
            "ticket_id": "a105e8e0-d179-49c2-b67f-930a9b2cbbbf",
            "confirmed_at": "2015-09-24T16:15:51.000000",
            "id": "a5d5830c-a5c3-4ce7-9bb7-665e455c023c",
            "additional_data": "{\"Message\": \"close.\"}",
            "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
            "target_role": "none"
        },
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230"
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow": [
            {
                "status": 2,
                "deleted_at": None,
                "confirmer_name": "user-a",
                "deleted": False,
                "status_code": "inquiring",
                "created_at": "2015-09-24T16:11:16.000000",
                "updated_at": "2015-09-24T16:14:58.000000",
                "status_detail": {
                    "status_code": "inquiring",
                    "status_name": {
                        "Default": "Inquiring",
                        "ja": "\u4f9d\u983c\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "working",
                            "grant_role": "wf_request_support"
                        },
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "50038a31-6c80-4c1c-a4af-327a16f18cbc",
                "confirmed_at": "2015-09-24T16:11:16.000000",
                "id": "ba007587-e4b3-49ec-b58e-aa60acda34a4",
                "additional_data": "",
                "confirmer_id": "6b4e00ee920d4a97b6f9c466098db230",
                "target_role": "none"
            },
            {
                "status": 1,
                "deleted_at": None,
                "confirmer_name": "suser-a",
                "deleted": False,
                "status_code": "close",
                "created_at": "2015-09-24T16:11:16.000000",
                "updated_at": "2015-09-24T16:16:19.000000",
                "status_detail": {
                    "status_code": "close",
                    "status_name": {
                        "Default": "Close",
                        "ja": "\u30af\u30ed\u30fc\u30ba"
                    },
                    "next_status": [{}]
                },
                "ticket_id": "50038a31-6c80-4c1c-a4af-327a16f18cbc",
                "confirmed_at": "2015-09-24T16:16:18.000000",
                "id": "c198f485-05bb-499b-9a0a-12f801d11a92",
                "additional_data": "{\"Message\": \"close.\"}",
                "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
                "target_role": "none"
            },
            {
                "status": 0,
                "deleted_at": None,
                "confirmer_name": None,
                "deleted": False,
                "status_code": "working",
                "created_at": "2015-09-24T16:11:16.000000",
                "updated_at": "2015-09-24T16:11:16.000000",
                "status_detail": {
                    "status_code": "working",
                    "status_name": {
                        "Default": "Working",
                        "ja": "\u4f5c\u696d\u4e2d"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close request",
                            "grant_role": "wf_request_support"
                        }
                    ]
                },
                "ticket_id": "50038a31-6c80-4c1c-a4af-327a16f18cbc",
                "confirmed_at": None,
                "id": "d0cd17b4-f7b6-4824-b588-f644cb4d875b",
                "additional_data": "",
                "confirmer_id": None,
                "target_role": "none"
            },
            {
                "status": 2,
                "deleted_at": None,
                "confirmer_name": "suser-a",
                "deleted": False,
                "status_code": "close request",
                "created_at": "2015-09-24T16:11:16.000000",
                "updated_at": "2015-09-24T16:16:19.000000",
                "status_detail": {
                    "status_code": "close request",
                    "status_name": {
                        "Default": "Close Request",
                        "ja": "\u30af\u30ed\u30fc\u30ba\u4f9d\u983c"
                    },
                    "next_status": [
                        {
                            "next_status_code": "close",
                            "grant_role": "_member_"
                        }
                    ]
                },
                "ticket_id": "50038a31-6c80-4c1c-a4af-327a16f18cbc",
                "confirmed_at": "2015-09-24T16:14:58.000000",
                "id": "e2401c78-a9a4-4e1c-9bf4-84968d7207df",
                "additional_data": "{\"Message\": \"close request.\"}",
                "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
                "target_role": "none"
            }
        ],
        "ticket_template_id": "21",
        "deleted": False,
        "tenant_name": "project-a",
        "target_id": "",
        "updated_at": "2015-09-24T16:11:16.000000",
        "owner_name": "user-a",
        "owner_at": "2015-09-24T16:11:16.000000",
        "deleted_at": None,
        "ticket_detail": "{\"Message\": \"last status is close.\"}",
        "tenant_id": "348e455501c24b34b1e116c266f1764d",
        "created_at": "2015-09-24T16:11:16.000000",
        "id": "50038a31-6c80-4c1c-a4af-327a16f18cbc",
        "ticket_type": "request",
        "action_detail": "",
        "last_workflow": {
            "status": 1,
            "deleted_at": None,
            "confirmer_name": "suser-a",
            "deleted": False,
            "status_code": "close",
            "created_at": "2015-09-24T16:11:16.000000",
            "updated_at": "2015-09-24T16:16:19.000000",
            "status_detail": {
                "status_code": "close",
                "status_name": {
                    "Default": "Close",
                    "ja": "\u30af\u30ed\u30fc\u30ba"
                },
                "next_status": [{}]
            },
            "ticket_id": "50038a31-6c80-4c1c-a4af-327a16f18cbc",
            "confirmed_at": "2015-09-24T16:16:18.000000",
            "id": "c198f485-05bb-499b-9a0a-12f801d11a92",
            "additional_data": "{\"Message\": \"close.\"}",
            "confirmer_id": "6b02f9d12f8c4a3fadd1ec9181d77b1b",
            "target_role": "none"
        },
        "owner_id": "6b4e00ee920d4a97b6f9c466098db230"
    }
]


"""Request approval flags detail
REQEST_APPROVAL_FLAGS[0]:
    next_status_code:working last_status_code:inquiring
REQEST_APPROVAL_FLAGS[1]:
    next_status_code:close request last_status_code:inquiring
REQEST_APPROVAL_FLAGS[2]:
    next_status_code:close request last_status_code:working
REQEST_APPROVAL_FLAGS[3]:
    next_status_code:close last_status_code:close request
"""
REQEST_APPROVAL_FLAGS = \
    [[('working:'
       '772a52569-8d9a-4156-b5a9-357a09181320:'
       'inquiring:'
       '0a8dfe64-0e20-4add-b870-029d4f687d39'), u'Working'],
     [('close request:'
       '0e6ae7ee-e703-4916-8785-8b440638a709:'
       'inquiring:'
       '0a8dfe64-0e20-4add-b870-029d4f687d39'), u'Close Request'],
     [('close request:'
       '8dae74e0-f1e4-4703-a274-308d72217061:'
       'working:'
       '0a8dfe64-0e20-4add-b870-029d4f687d39'), u'Close Request'],
     [('close:'
       '33c824ca-7ec8-44de-ba35-364cb9a380df:'
       'close request:'
       '72a52569-8d9a-4156-b5a9-357a09181320'), u'Close']]


"""Contract ticket data detail
CONTRACT_DATA_LIST[0]:contracted
"""
CONTRACT_DATA_LIST = [
    {
        "application_date": "2015-09-28T20:14:57.000000",
        "application_id": "1f73f0a3-7b23-432d-bcf5-712c33f3c880",
        "application_kinds_name":
            "Gold VCPU 10, Silver VCPU 10, Bronze VCPU 10, "
            "RAM 20GB, Volume Storage 50GB",
        "application_name": "user-a",
        "cancel_application_id": None,
        "catalog_id": None,
        "catalog_name": None,
        "contract_id": "3ac86a31-a03e-4713-a909-a4422091cded",
        "created_at": "2015-09-28T22:06:47.000000",
        "deleted": False,
        "deleted_at": None,
        "expansions": {
            "expansion_key1": None,
            "expansion_key2": None,
            "expansion_key3": None,
            "expansion_key4": None,
            "expansion_key5": None
        },
        "expansions_text": {
            "expansion_text":
                "{\"contract_info\": "
                "{\"ticket_detail\": "
                "{\"Volume Storage 50 GB\": 5, "
                "\"RAM 20 GB\": 4, "
                "\"Silver VCPU x 10 CORE(S)\": 2, "
                "\"Bronze VCPU x 10 CORE(S)\": 3, "
                "\"Gold VCPU x 10 CORE(S)\": 1, "
                "\"Message\": \"registration apply check.\"}}, "
                "\"ticket_info\": "
                "{\"cancelling_template\": "
                "{\"id\": \"11\"}, "
                "\"change_template\": "
                "{\"id\": \"11\"}}}"
        },
        "lifetime_end": "9999-12-31T23:59:59.000000",
        "lifetime_start": "2015-09-29T07:06:47.000000",
        "num": None,
        "parent_application_kinds_name":
            "Gold VCPU 10, Silver VCPU 10, Bronze VCPU 10, "
            "RAM 20GB, Volume Storage 50GB",
        "parent_contract_id": "3ac86a31-a03e-4713-a909-a4422091cded",
        "parent_ticket_template_id": "10",
        "parent_ticket_template_name": "flat-rate",
        "project_id": "348e455501c24b34b1e116c266f1764d",
        "project_name": "project-a",
        "region_id": None,
        "ticket_template_id": "10",
        "ticket_template_name": "flat-rate",
        "updated_at": "2015-09-28T22:06:47.000000"
    }
]


"""Catalog price data detail
CATALOG_PRICE_DATA_LIST[0]
    catalog_id:catalog0-1111-2222-3333-000000000005
CATALOG_PRICE_DATA_LIST[1]
    catalog_id:catalog0-1111-2222-3333-000000000004
CATALOG_PRICE_DATA_LIST[2]
    catalog_id:catalog0-1111-2222-3333-000000000003
CATALOG_PRICE_DATA_LIST[3]
    catalog_id:catalog0-1111-2222-3333-000000000002
CATALOG_PRICE_DATA_LIST[4]
    catalog_id:catalog0-1111-2222-3333-000000000001
"""
CATALOG_PRICE_DATA_LIST = [
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000005",
        "created_at": "2015-01-01T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "expansions": {
            "expansion_key1": None,
            "expansion_key2": None,
            "expansion_key3": None,
            "expansion_key4": None,
            "expansion_key5": None
        },
        "expansions_text": {
            "expansion_text": None
        },
        "lifetime_end": "2015-12-31T00:00:00.000000",
        "lifetime_start": "2015-01-01T00:00:00.000000",
        "price": "172.41",
        "scope": "Default",
        "seq_no": "price01",
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000004",
        "created_at": "2015-01-01T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "expansions": {
            "expansion_key1": None,
            "expansion_key2": None,
            "expansion_key3": None,
            "expansion_key4": None,
            "expansion_key5": None
        },
        "expansions_text": {
            "expansion_text": None
        },
        "lifetime_end": "2015-12-31T00:00:00.000000",
        "lifetime_start": "2015-01-01T00:00:00.000000",
        "price": "129.31",
        "scope": "Default",
        "seq_no": "price02",
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000003",
        "created_at": "2015-01-01T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "expansions": {
            "expansion_key1": None,
            "expansion_key2": None,
            "expansion_key3": None,
            "expansion_key4": None,
            "expansion_key5": None
        },
        "expansions_text": {
            "expansion_text": None
        },
        "lifetime_end": "2015-12-31T00:00:00.000000",
        "lifetime_start": "2015-01-01T00:00:00.000000",
        "price": "86.21",
        "scope": "Default",
        "seq_no": "price03",
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000002",
        "created_at": "2015-01-01T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "expansions": {
            "expansion_key1": None,
            "expansion_key2": None,
            "expansion_key3": None,
            "expansion_key4": None,
            "expansion_key5": None
        },
        "expansions_text": {
            "expansion_text": None
        },
        "lifetime_end": "2015-12-31T00:00:00.000000",
        "lifetime_start": "2015-01-01T00:00:00.000000",
        "price": "258.62",
        "scope": "Default",
        "seq_no": "price04",
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000001",
        "created_at": "2015-01-01T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "expansions": {
            "expansion_key1": None,
            "expansion_key2": None,
            "expansion_key3": None,
            "expansion_key4": None,
            "expansion_key5": None
        },
        "expansions_text": {
            "expansion_text": None
        },
        "lifetime_end": "2015-12-31T00:00:00.000000",
        "lifetime_start": "2015-01-01T00:00:00.000000",
        "price": "64.66",
        "scope": "Default",
        "seq_no": "price05",
        "updated_at": None
    }
]
