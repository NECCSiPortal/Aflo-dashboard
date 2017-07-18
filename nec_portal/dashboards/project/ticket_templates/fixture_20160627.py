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
#

"""Tickettemplate data detail
ticket_template_version: 2016-06-27
TICKET_TEMPLATE_DATA_LIST[0]:
    ticket_type:New Contract(All types of parameters are set)
    id:10
TICKET_TEMPLATE_DATA_LIST[1]:
    ticket_type:Cancel Contract
    id:11
"""
TICKET_TEMPLATE_DATA_LIST = [
    {
        "ticket_template_version": "2016-06-27",
        "created_at": "2016-06-27T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "10",
        "roles": [
            "O__DC1__ServiceProvider",
            "O__DC1__ContractManager",
            "O__DC1__ServiceManager",
            "_member_",
            "T__DC1__ProjectMember",
            "admin",
            "T__DC1__ObjectStore",
        ],
        "template_contents": {
            "action": {
                "broker": [
                    {
                        "broker_method":
                            "integrity_check_for_purchase_contract",
                        "status": "pre-approval",
                        "timing": "before",
                        "validation":
                            "integrity_check_"
                            "for_purchase_contract_pre_approval"
                    },
                    {
                        "broker_method": "",
                        "status": "pre-approval",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "canceled",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "canceled",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "rejected",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "rejected",
                        "timing": "after"
                    },
                    {
                        "broker_method":
                            "integrity_check_for_purchase_contract",
                        "status": "final approval",
                        "timing": "before",
                        "validation":
                            "integrity_check_"
                            "for_purchase_contract_final_approval"
                    },
                    {
                        "broker_method":
                            "contract_data_registration_for_purchase_contract",
                        "status": "final approval",
                        "timing": "after"
                    }
                ],
                "broker_class":
                    "aflo.tickets.broker."
                    "sample_set_catalog_monthly.SampleSetCatalogBroker"
            },
            "application_kinds_name": {
                "Default": "VCPU 10, RAM 20GB, Volume Storage 50GB",
                "ja":
                    "VCPU 10, RAM 20GB, \u30dc\u30ea\u30e5"
                    "\u30fc\u30e0\u30b9\u30c8\u30ec\u30fc\u30b8 50GB"
            },
            "cancelling_template": {
                "id": "11"
            },
            "change_template": {
                "id": "11"
            },
            "create": {
                "custom": [
                    {
                        "price_list": "right"
                    }
                ],
                "parameters": [
                    {
                        "constraints": {
                            "range": {
                                "max": 9999,
                                "min": 1
                            },
                            "required": True
                        },
                        "default": "",
                        "key": "number_parameter",
                        "label": {
                            "default": "Number Parameter",
                            "ja": "Number Parameter(ja)"
                        },
                        "type": "number"
                    },
                    {
                        "constraints": {
                            "length": {
                                "max": 512,
                                "min": 2
                            }
                        },
                        "description": {
                            "default": "Please input if there is a message.",
                            "ja":
                                "\u30e1\u30c3\u30bb\u30fc\u30b8"
                                "\u304c\u3042\u308b\u5834\u5408"
                                "\u306f\u5165\u529b\u3057\u3066"
                                "\u304f\u3060\u3055\u3044\u3002"
                        },
                        "key": "string_parameter",
                        "label": {
                            "default": "String Parameter",
                            "ja": "String Parameter(ja)"
                        },
                        "multi_line": True,
                        "type": "string"
                    },
                    {
                        "key": "hidden_parameter",
                        "label": {
                            "default": "Hidden Parameter",
                            "ja": "Hidden Parameter(ja)"
                        },
                        "type": "hidden"
                    },
                    {
                        "default": "",
                        "key": "date_parameter",
                        "label": {
                            "default": "Date Parameter",
                            "ja": "Date Parameter(ja)"
                        },
                        "type": "date"
                    },
                    {
                        "default": "",
                        "key": "email_parameter",
                        "label": {
                            "default": "Email Parameter",
                            "ja": "Email Parameter(ja)"
                        },
                        "type": "email"
                    },
                    {
                        "default": "",
                        "key": "boolean_parameter",
                        "label": {
                            "default": "Boolean Parameter",
                            "ja": "Boolean Parameter(ja)"
                        },
                        "type": "boolean"
                    },
                    {
                        "default": "",
                        "key": "select_item_parameter",
                        "label": {
                            "default": "Select Item Parameter",
                            "ja": "Select Item Parameter(ja)"
                        },
                        "type": "string",
                        "constraints": {
                            "allowed_values": [
                                {
                                    "value": "0",
                                    "label": {
                                        "default": "Select Item A",
                                        "ja": "Select Item A(ja)"
                                    }
                                },
                                {
                                    "value": "1",
                                    "label": {
                                        "default": "Select Item B",
                                        "ja": "Select Item B(ja)"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "default": "",
                        "key": "regular_expression_parameter",
                        "label": {
                            "default": "Regular Expression Parameter",
                            "ja": "Regular Expression Parameter(ja)"
                        },
                        "type": "string",
                        "constraints": {
                            "allowed_pattern": "\d{2}-[a-z]{5}"
                        }
                    }
                ]
            },
            "first_status_code": "pre-approval",
            "price_notice": [
                "*Monthly fee",
                "*Tax excluded"
            ],
            "target_id": [
                "catalog0-1111-2222-3333-000000000003",
                "catalog0-1111-2222-3333-000000000002",
                "catalog0-1111-2222-3333-000000000001"
            ],
            "target_key": [
                "vcpu",
                "ram",
                "volume"
            ],
            "ticket_template_name": {
                "Default": "flat-rate",
                "ja": "\u5b9a\u984d\u8ab2\u91d1"
            },
            "ticket_type": "New Contract",
            "update": {
                "custom": [
                    {
                        "price_list": "right"
                    }
                ],
                "parameters": [
                    {
                        "constraints": {
                            "range": {
                                "max": 9999,
                                "min": 1
                            },
                            "required": True
                        },
                        "default": "",
                        "key": "number_parameter",
                        "label": {
                            "default": "Number Parameter",
                            "ja": "Number Parameter(ja)"
                        },
                        "type": "number"
                    },
                    {
                        "constraints": {
                            "length": {
                                "max": 512,
                                "min": 2
                            }
                        },
                        "description": {
                            "default": "Please input if there is a message.",
                            "ja":
                                "\u30e1\u30c3\u30bb\u30fc\u30b8"
                                "\u304c\u3042\u308b\u5834\u5408"
                                "\u306f\u5165\u529b\u3057\u3066"
                                "\u304f\u3060\u3055\u3044\u3002"
                        },
                        "key": "string_parameter",
                        "label": {
                            "default": "String Parameter",
                            "ja": "String Parameter(ja)"
                        },
                        "multi_line": True,
                        "type": "string"
                    },
                    {
                        "key": "hidden_parameter",
                        "label": {
                            "default": "Hidden Parameter",
                            "ja": "Hidden Parameter(ja)"
                        },
                        "type": "hidden"
                    },
                    {
                        "default": "",
                        "key": "date_parameter",
                        "label": {
                            "default": "Date Parameter",
                            "ja": "Date Parameter(ja)"
                        },
                        "type": "date"
                    },
                    {
                        "default": "",
                        "key": "email_parameter",
                        "label": {
                            "default": "Email Parameter",
                            "ja": "Email Parameter(ja)"
                        },
                        "type": "email"
                    },
                    {
                        "default": "",
                        "key": "boolean_parameter",
                        "label": {
                            "default": "Boolean Parameter",
                            "ja": "Boolean Parameter(ja)"
                        },
                        "type": "boolean"
                    },
                    {
                        "default": "",
                        "key": "select_item_parameter",
                        "label": {
                            "default": "Select Item Parameter",
                            "ja": "Select Item Parameter(ja)"
                        },
                        "type": "string",
                        "constraints": {
                            "allowed_values": [
                                {
                                    "value": "0",
                                    "label": {
                                        "default": "Select Item A",
                                        "ja": "Select Item A(ja)"
                                    }
                                },
                                {
                                    "value": "1",
                                    "label": {
                                        "default": "Select Item B",
                                        "ja": "Select Item B(ja)"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "default": "",
                        "key": "regular_expression_parameter",
                        "label": {
                            "default": "Regular Expression Parameter",
                            "ja": "Regular Expression Parameter(ja)"
                        },
                        "type": "string",
                        "constraints": {
                            "allowed_pattern": "\d{2}-[a-z]{5}"
                        }
                    }
                ]
            },
            "wf_pattern_code": "contract_workflow"
        },
        "ticket_type": "New Contract",
        "updated_at": None,
        "workflow_pattern": {
            "wf_pattern_version": "2016-06-27",
            "code": "contract_workflow",
            "created_at": "2016-06-27T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "10",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "T__DC1__ProjectMember",
                                "next_status_code": "pre-approval"
                            }
                        ],
                        "status_code": "none",
                        "status_name": {
                            "Default": "None",
                            "ja": "\u306a\u3057"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "admin",
                                "next_status_code": "final approval"
                            },
                            {
                                "grant_role": "admin",
                                "next_status_code": "rejected"
                            },
                            {
                                "grant_role": "T__DC1__ProjectMember",
                                "next_status_code": "canceled"
                            }
                        ],
                        "status_code": "pre-approval",
                        "status_name": {
                            "Default": "Pre-approval",
                            "ja": "\u672a\u627f\u8a8d"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "rejected",
                        "status_name": {
                            "Default": "Rejected",
                            "ja": "\u5426\u8a8d"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "canceled",
                        "status_name": {
                            "Default": "Canceled",
                            "ja": "\u30ad\u30e3\u30f3\u30bb\u30eb"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "final approval",
                        "status_name": {
                            "Default": "Final Approval",
                            "ja": "\u6700\u7d42\u627f\u8a8d"
                        }
                    }
                ],
                "wf_pattern_code": "contract_workflow",
                "wf_pattern_name": {
                    "Default": "Contract Workflow",
                    "ja": "\u5951\u7d04\u30ef\u30fc\u30af\u30d5\u30ed\u30fc"
                }
            }
        },
        "workflow_pattern_id": "10"
    },
    {
        "ticket_template_version": "2016-06-27",
        "created_at": "2016-06-27T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "11",
        "roles": [
            "O__DC1__ServiceProvider",
            "aflo_admin",
            "O__DC1__ContractManager",
            "O__DC1__ServiceManager",
            "_member_",
            "heat_stack_owner",
            "T__DC1__ProjectMember",
            "admin",
            "T__DC1__ObjectStore",
        ],
        "template_contents": {
            "action": {
                "broker": [
                    {
                        "broker_method": "",
                        "status": "pre-approval",
                        "timing": "before",
                        "validation": "integrity_check_for_cancellation"
                    },
                    {
                        "broker_method": "",
                        "status": "pre-approval",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "canceled",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "canceled",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "rejected",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "",
                        "status": "rejected",
                        "timing": "after"
                    },
                    {
                        "broker_method": "",
                        "status": "final approval",
                        "timing": "before",
                        "validation": "integrity_check_for_cancellation"
                    },
                    {
                        "broker_method":
                            "contract_data_registration_for_cancellation",
                        "status": "final approval",
                        "timing": "after"
                    }
                ],
                "broker_class":
                    "aflo.tickets.broker."
                    "sample_set_catalog_monthly.SampleSetCatalogBroker"
            },
            "application_kinds_name": {
                "Default": "VCPU 10, RAM 20GB, Volume Storage 50GB",
                "ja":
                    "VCPU 10, RAM 20GB, \u30dc\u30ea\u30e5"
                    "\u30fc\u30e0\u30b9\u30c8\u30ec\u30fc\u30b8 50GB"
            },
            "create": {
                "custom": [
                    {
                        "price_list": "right"
                    },
                    {
                        "cancel_contract": "left"
                    }
                ],
                "parameters": [
                    {
                        "constraints": {
                            "range": {
                                "max": 9999,
                                "min": 0
                            },
                            "required": True
                        },
                        "default": "",
                        "key": "vcpu",
                        "label": {
                            "default": "VCPU x 10 CORE(S) Number",
                            "ja": "VCPU x 10 CORE(S) \u5951\u7d04\u6570"
                        },
                        "type": "number"
                    },
                    {
                        "constraints": {
                            "range": {
                                "max": 9999,
                                "min": 0
                            },
                            "required": True
                        },
                        "default": "",
                        "key": "ram",
                        "label": {
                            "default": "RAM 20 GB Number",
                            "ja": "RAM 20 GB \u5951\u7d04\u6570"
                        },
                        "type": "number"
                    },
                    {
                        "constraints": {
                            "range": {
                                "max": 9999,
                                "min": 0
                            },
                            "required": True
                        },
                        "default": "",
                        "key": "volume",
                        "label": {
                            "default": "Volume 50 GB Number",
                            "ja":
                                "\u30dc\u30ea\u30e5\u30fc\u30e0"
                                "\u30b9\u30c8\u30ec\u30fc\u30b8 50 GB "
                                "\u5951\u7d04\u6570"
                        },
                        "type": "number"
                    },
                    {
                        "constraints": {
                            "length": {
                                "max": 512,
                                "min": 0
                            }
                        },
                        "description": {
                            "default": "Please input if there is a message.",
                            "ja": "\u30e1\u30c3\u30bb\u30fc\u30b8"
                            "\u304c\u3042\u308b\u5834\u5408\u306f"
                            "\u5165\u529b\u3057\u3066\u304f\u3060"
                            "\u3055\u3044\u3002"
                        },
                        "key": "message",
                        "label": {
                            "default": "Message",
                            "ja": "\u30e1\u30c3\u30bb\u30fc\u30b8"
                        },
                        "multi_line": True,
                        "type": "string"
                    }
                ]
            },
            "first_status_code": "pre-approval",
            "price_notice": [
                "*Monthly fee",
                "*Tax excluded"
            ],
            "target_id": [
                "catalog0-1111-2222-3333-000000000003",
                "catalog0-1111-2222-3333-000000000002",
                "catalog0-1111-2222-3333-000000000001"
            ],
            "target_key": [
                "vcpu",
                "ram",
                "volume"
            ],
            "ticket_template_name": {
                "Default": "flat-rate",
                "ja": "\u5b9a\u984d\u8ab2\u91d1"
            },
            "ticket_type": "Cancel Contract",
            "update": {
                "custom": [
                    {
                        "price_list": "right"
                    },
                    {
                        "project_info": "left"
                    }
                ],
                "parameters": [
                    {
                        "key": "message",
                        "label": {
                            "default": "Message",
                            "ja": "\u30e1\u30c3\u30bb\u30fc\u30b8"
                        },
                        "multi_line": True,
                        "type": "string"
                    }
                ]
            },
            "wf_pattern_code": "contract_workflow"
        },
        "ticket_type": "Cancel Contract",
        "updated_at": None,
        "workflow_pattern": {
            "wf_pattern_version": "2016-06-27",
            "code": "contract_workflow",
            "created_at": "2016-06-27T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "10",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "T__DC1__ProjectMember",
                                "next_status_code": "pre-approval"
                            }
                        ],
                        "status_code": "none",
                        "status_name": {
                            "Default": "None",
                            "ja": "\u306a\u3057"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "admin",
                                "next_status_code": "final approval"
                            },
                            {
                                "grant_role": "admin",
                                "next_status_code": "rejected"
                            },
                            {
                                "grant_role": "T__DC1__ProjectMember",
                                "next_status_code": "canceled"
                            }
                        ],
                        "status_code": "pre-approval",
                        "status_name": {
                            "Default": "Pre-approval",
                            "ja": "\u672a\u627f\u8a8d"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "rejected",
                        "status_name": {
                            "Default": "Rejected",
                            "ja": "\u5426\u8a8d"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "canceled",
                        "status_name": {
                            "Default": "Canceled",
                            "ja": "\u30ad\u30e3\u30f3\u30bb\u30eb"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "final approval",
                        "status_name": {
                            "Default": "Final Approval",
                            "ja": "\u6700\u7d42\u627f\u8a8d"
                        }
                    }
                ],
                "wf_pattern_code": "contract_workflow",
                "wf_pattern_name": {
                    "Default": "Contract Workflow",
                    "ja": "\u5951\u7d04\u30ef\u30fc\u30af\u30d5\u30ed\u30fc"
                }
            }
        },
        "workflow_pattern_id": "10"
    }
]


"""Contract ticket data detail
ticket_template_version: 2016-06-27
"""
CONTRACT_TICKET_DATA = {
    "action_detail": "",
    "created_at": "2016-06-27T00:35:56.000000",
    "deleted": False,
    "deleted_at": None,
    "id": "1491722c-e088-44e7-b13e-e0045107ca5b",
    "owner_at": "2016-06-27T00:35:56.000000",
    "owner_id": "267d442ae6d44a2992c8d0d3237df04a",
    "owner_name": "admin",
    "roles": [
        "O__DC1__ServiceProvider",
        "aflo_admin",
        "O__DC1__ContractManager",
        "O__DC1__ServiceManager",
        "_member_",
        "heat_stack_owner",
        "T__DC1__ProjectMember",
        "admin",
        "T__DC1__ObjectStore",
    ],
    "target_id": [
        "catalog0-1111-2222-3333-000000000003",
        "catalog0-1111-2222-3333-000000000002",
        "catalog0-1111-2222-3333-000000000001"
    ],
    "tenant_id": "f2e7deaf657d44f6bf754890b715d852",
    "tenant_name": "admin",
    "ticket_detail":
        "{\"volume\": 9999, "
        "\"vcpu\": 9999, "
        "\"message\": \"message.\", "
        "\"ram\": 9999}",
    "ticket_template_id": "10",
    "ticket_type": "New Contract",
    "updated_at": "2016-06-27T00:35:56.000000",
    "workflow": [
        {
            "additional_data": "",
            "confirmed_at": None,
            "confirmer_id": None,
            "confirmer_name": None,
            "created_at": "2016-06-27T00:35:56.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "65c4dd79-9c9f-4935-8080-f5bf5817f906",
            "status": 0,
            "status_code": "canceled",
            "status_detail": {
                "next_status": [{}],
                "status_code": "canceled",
                "status_name": {
                    "Default": "Canceled",
                    "ja": "\u30ad\u30e3\u30f3\u30bb\u30eb"
                }
            },
            "target_role": "none",
            "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
            "updated_at": "2016-06-27T00:35:56.000000"
        },
        {
            "additional_data": "",
            "confirmed_at": None,
            "confirmer_id": None,
            "confirmer_name": None,
            "created_at": "2016-06-27T00:35:56.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "b8bc188c-22c9-4e60-972c-fcf25e8f289f",
            "status": 0,
            "status_code": "rejected",
            "status_detail": {
                "next_status": [{}],
                "status_code": "rejected",
                "status_name": {
                    "Default": "Rejected",
                    "ja": "\u5426\u8a8d"
                }
            },
            "target_role": "none",
            "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
            "updated_at": "2016-06-27T00:35:56.000000"
        },
        {
            "additional_data": "",
            "confirmed_at": "2016-06-27T00:35:56.000000",
            "confirmer_id": "267d442ae6d44a2992c8d0d3237df04a",
            "confirmer_name": "admin",
            "created_at": "2016-06-27T00:35:56.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "d343d7bc-3b98-4a39-9a27-4678ed3cfcb2",
            "status": 2,
            "status_code": "pre-approval",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "admin",
                        "next_status_code": "final approval"
                    },
                    {
                        "grant_role": "admin",
                        "next_status_code": "rejected"
                    },
                    {
                        "grant_role": "T__DC1__ProjectMember",
                        "next_status_code": "canceled"
                    }
                ],
                "status_code": "pre-approval",
                "status_name": {
                    "Default": "Pre-approval",
                    "ja": "\u672a\u627f\u8a8d"
                }
            },
            "target_role": "none",
            "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
            "updated_at": "2016-06-27T00:36:14.000000"
        },
        {
            "additional_data": "{\"message\": \"message.\"}",
            "confirmed_at": "2016-06-27T00:36:14.000000",
            "confirmer_id": "267d442ae6d44a2992c8d0d3237df04a",
            "confirmer_name": "admin",
            "created_at": "2016-06-27T00:35:56.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "e4db1918-40d2-45e3-96a3-31fa848b2739",
            "status": 1,
            "status_code": "final approval",
            "status_detail": {
                "next_status": [{}],
                "status_code": "final approval",
                "status_name": {
                    "Default": "Final Approval",
                    "ja": "\u6700\u7d42\u627f\u8a8d"
                }
            },
            "target_role": "none",
            "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
            "updated_at": "2016-06-27T00:36:14.000000"
        }
    ]
}


"""Contract data detail
ticket_template_version: 2016-06-27
"""
CONTRACT_DATA = {
    "application_date": "2016-06-27T00:35:56.000000",
    "application_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
    "application_kinds_name": "VCPU 10, RAM 20GB, Volume Storage 50GB",
    "application_name": "admin",
    "cancel_application_id": None,
    "catalog_id": None,
    "catalog_name": None,
    "contract_id": "242200e7-757d-45a9-80db-cfc620d1c8a7",
    "created_at": "2016-06-27T00:36:14.000000",
    "deleted": False,
    "deleted_at": None,
    "expansions": {
        "expansion_key1": "contract-flat-rate",
        "expansion_key2": None,
        "expansion_key3": None,
        "expansion_key4": None,
        "expansion_key5": None
    },
    "expansions_text": {
        "expansion_text":
            "{\"contract_info\": "
            "{\"ticket_detail\": "
            "{\"volume\": 9999, "
            "\"vcpu\": 9999, "
            "\"message\": \"message.\", "
            "\"ram\": 9999}},"
            "\"ticket_info\": "
            "{\"cancelling_template\": {\"id\": \"11\"},"
            "\"change_template\": {\"id\": \"11\"}}}"
    },
    "lifetime_end": "9999-12-31T23:59:59.000000",
    "lifetime_start": "2016-06-27T00:36:14.000000",
    "num": None,
    "parent_application_kinds_name": "VCPU 10, RAM 20GB, Volume Storage 50GB",
    "parent_contract_id": "242200e7-757d-45a9-80db-cfc620d1c8a7",
    "parent_ticket_template_id": "10",
    "parent_ticket_template_name": "flat-rate",
    "project_id": "f2e7deaf657d44f6bf754890b715d852",
    "project_name": "admin",
    "region_id": None,
    "ticket_template_id": "10",
    "ticket_template_name": "flat-rate",
    "updated_at": "2016-06-27T00:36:14.000000"
}


"""Catalog price data detail
ticket_template_version: 2016-06-27
CATALOG_PRICE_DATA_LIST[0]
    catalog_id:catalog0-1111-2222-3333-000000000003
CATALOG_PRICE_DATA_LIST[1]
    catalog_id:catalog0-1111-2222-3333-000000000002
CATALOG_PRICE_DATA_LIST[2]
    catalog_id:catalog0-1111-2222-3333-000000000001
"""
CATALOG_PRICE_DATA_LIST = [
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000003",
        "created_at": "2016-06-27T00:00:00.000000",
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
        "lifetime_end": "9999-12-31T00:00:00.000000",
        "lifetime_start": "2016-06-27T00:00:00.000000",
        "price": "172.41",
        "scope": "Default",
        "seq_no": "price01",
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000002",
        "created_at": "2016-06-27T00:00:00.000000",
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
        "lifetime_end": "9999-12-31T00:00:00.000000",
        "lifetime_start": "2016-06-27T00:00:00.000000",
        "price": "258.62",
        "scope": "Default",
        "seq_no": "price04",
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000001",
        "created_at": "2016-06-27T00:00:00.000000",
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
        "lifetime_end": "9999-12-31T00:00:00.000000",
        "lifetime_start": "2016-06-27T00:00:00.000000",
        "price": "64.66",
        "scope": "Default",
        "seq_no": "price05",
        "updated_at": None
    }
]


"""Catalog data detail
ticket_template_version: 2016-06-27
CATALOG_DATA_LIST[0]
    catalog_id:catalog0-1111-2222-3333-000000000003
CATALOG_DATA_LIST[1]
    catalog_id:catalog0-1111-2222-3333-000000000002
CATALOG_DATA_LIST[2]
    catalog_id:catalog0-1111-2222-3333-000000000001
"""
CATALOG_DATA_LIST = [
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000003",
        "catalog_name": "Catalog C",
        "created_at": "2016-06-27T00:00:00.000000",
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
        "lifetime_end": "9999-12-31T23:59:59.000000",
        "lifetime_start": "2016-06-27T00:00:00.000000",
        "region_id": None,
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000002",
        "catalog_name": "Catalog B",
        "created_at": "2016-06-27T00:00:00.000000",
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
        "lifetime_end": "9999-12-31T23:59:59.000000",
        "lifetime_start": "2016-06-27T00:00:00.000000",
        "region_id": None,
        "updated_at": None
    },
    {
        "catalog_id": "catalog0-1111-2222-3333-000000000001",
        "catalog_name": "Catalog A",
        "created_at": "2016-06-27T00:00:00.000000",
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
        "lifetime_end": "9999-12-31T23:59:59.000000",
        "lifetime_start": "2016-06-27T00:00:00.000000",
        "region_id": None,
        "updated_at": None
    }
]


"""Ticket data detail
ticket_template_version: 2016-06-27
TICKET_DATA_LIST[0]: create input parameter for pre-approval
TICKET_DATA_LIST[1]: create and update input parameter for final approval
"""
TICKET_DATA_LIST = [
    {
        "action_detail": "",
        "created_at": "2016-06-27T00:35:56.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "1491722c-e088-44e7-b13e-e0045107ca5b",
        "owner_at": "2016-06-27T00:35:56.000000",
        "owner_id": "267d442ae6d44a2992c8d0d3237df04a",
        "owner_name": "admin",
        "roles": [
            "O__DC1__ServiceProvider",
            "aflo_admin",
            "O__DC1__ContractManager",
            "O__DC1__ServiceManager",
            "_member_",
            "heat_stack_owner",
            "T__DC1__ProjectMember",
            "admin",
            "T__DC1__ObjectStore",
        ],
        "target_id": [
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "f2e7deaf657d44f6bf754890b715d852",
        "tenant_name": "admin",
        "ticket_detail":
            "{\"number_parameter\": 9999, "
            "\"string_parameter\": \"message.\", "
            "\"hidden_parameter\": \"message.\", "
            "\"date_parameter\": \"2016-06-27T00:00:00.000000\", "
            "\"email_parameter\": \"xxxxx@xxxxx.xxxxx\", "
            "\"boolean_parameter\": true, "
            "\"select_item_parameter\": \"0\", "
            "\"regular_expression_parameter\": \"99-xxxxx\", "
            "\"message\": \"pre-approval.\"}",
        "ticket_template_id": "10",
        "ticket_type": "New Contract",
        "updated_at": "2016-06-27T00:35:56.000000",
        "workflow": [
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "65c4dd79-9c9f-4935-8080-f5bf5817f906",
                "status": 0,
                "status_code": "canceled",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "canceled",
                    "status_name": {
                        "Default": "Canceled",
                        "ja": "\u30ad\u30e3\u30f3\u30bb\u30eb"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:35:56.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "b8bc188c-22c9-4e60-972c-fcf25e8f289f",
                "status": 0,
                "status_code": "rejected",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "rejected",
                    "status_name": {
                        "Default": "Rejected",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:35:56.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": "2016-06-27T00:35:56.000000",
                "confirmer_id": "267d442ae6d44a2992c8d0d3237df04a",
                "confirmer_name": "admin",
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "d343d7bc-3b98-4a39-9a27-4678ed3cfcb2",
                "status": 1,
                "status_code": "pre-approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "admin",
                            "next_status_code": "final approval"
                        },
                        {
                            "grant_role": "admin",
                            "next_status_code": "rejected"
                        },
                        {
                            "grant_role": "T__DC1__ProjectMember",
                            "next_status_code": "canceled"
                        }
                    ],
                    "status_code": "pre-approval",
                    "status_name": {
                        "Default": "Pre-approval",
                        "ja": "\u672a\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:36:14.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "e4db1918-40d2-45e3-96a3-31fa848b2739",
                "status": 0,
                "status_code": "final approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "final approval",
                    "status_name": {
                        "Default": "Final Approval",
                        "ja": "\u6700\u7d42\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:36:14.000000"
            }
        ]
    },
    {
        "action_detail": "",
        "created_at": "2016-06-27T00:35:56.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "1491722c-e088-44e7-b13e-e0045107ca5b",
        "owner_at": "2016-06-27T00:35:56.000000",
        "owner_id": "267d442ae6d44a2992c8d0d3237df04a",
        "owner_name": "admin",
        "roles": [
            "O__DC1__ServiceProvider",
            "aflo_admin",
            "O__DC1__ContractManager",
            "O__DC1__ServiceManager",
            "_member_",
            "heat_stack_owner",
            "T__DC1__ProjectMember",
            "admin",
            "T__DC1__ObjectStore",
        ],
        "target_id": [
            "catalog0-1111-2222-3333-000000000003",
            "catalog0-1111-2222-3333-000000000002",
            "catalog0-1111-2222-3333-000000000001"
        ],
        "tenant_id": "f2e7deaf657d44f6bf754890b715d852",
        "tenant_name": "admin",
        "ticket_detail":
            "{\"number_parameter\": 9999, "
            "\"string_parameter\": \"message.\", "
            "\"hidden_parameter\": \"message.\", "
            "\"date_parameter\": \"2016-06-27T00:00:00.000000\", "
            "\"email_parameter\": \"xxxxx@xxxxx.xxxxx\", "
            "\"boolean_parameter\": true, "
            "\"select_item_parameter\": \"0\", "
            "\"regular_expression_parameter\": \"99-xxxxx\", "
            "\"message\": \"pre-approval.\"}",
        "ticket_template_id": "10",
        "ticket_type": "New Contract",
        "updated_at": "2016-06-27T00:35:56.000000",
        "workflow": [
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "65c4dd79-9c9f-4935-8080-f5bf5817f906",
                "status": 0,
                "status_code": "canceled",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "canceled",
                    "status_name": {
                        "Default": "Canceled",
                        "ja": "\u30ad\u30e3\u30f3\u30bb\u30eb"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:35:56.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": None,
                "confirmer_id": None,
                "confirmer_name": None,
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "b8bc188c-22c9-4e60-972c-fcf25e8f289f",
                "status": 0,
                "status_code": "rejected",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "rejected",
                    "status_name": {
                        "Default": "Rejected",
                        "ja": "\u5426\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:35:56.000000"
            },
            {
                "additional_data": "",
                "confirmed_at": "2016-06-27T00:35:56.000000",
                "confirmer_id": "267d442ae6d44a2992c8d0d3237df04a",
                "confirmer_name": "admin",
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "d343d7bc-3b98-4a39-9a27-4678ed3cfcb2",
                "status": 2,
                "status_code": "pre-approval",
                "status_detail": {
                    "next_status": [
                        {
                            "grant_role": "admin",
                            "next_status_code": "final approval"
                        },
                        {
                            "grant_role": "admin",
                            "next_status_code": "rejected"
                        },
                        {
                            "grant_role": "T__DC1__ProjectMember",
                            "next_status_code": "canceled"
                        }
                    ],
                    "status_code": "pre-approval",
                    "status_name": {
                        "Default": "Pre-approval",
                        "ja": "\u672a\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:36:14.000000"
            },
            {
                "additional_data":
                    "{\"number_parameter\": 9999, "
                    "\"string_parameter\": \"message.\", "
                    "\"hidden_parameter\": \"message.\", "
                    "\"date_parameter\": \"2016-06-27T00:00:00.000000\", "
                    "\"email_parameter\": \"xxxxx@xxxxx.xxxxx\", "
                    "\"boolean_parameter\": true, "
                    "\"select_item_parameter\": \"0\", "
                    "\"regular_expression_parameter\": \"99-xxxxx\", "
                    "\"message\": \"final approval.\"}",
                "confirmed_at": "2016-06-27T00:36:14.000000",
                "confirmer_id": "267d442ae6d44a2992c8d0d3237df04a",
                "confirmer_name": "admin",
                "created_at": "2016-06-27T00:35:56.000000",
                "deleted": False,
                "deleted_at": None,
                "id": "e4db1918-40d2-45e3-96a3-31fa848b2739",
                "status": 1,
                "status_code": "final approval",
                "status_detail": {
                    "next_status": [{}],
                    "status_code": "final approval",
                    "status_name": {
                        "Default": "Final Approval",
                        "ja": "\u6700\u7d42\u627f\u8a8d"
                    }
                },
                "target_role": "none",
                "ticket_id": "1491722c-e088-44e7-b13e-e0045107ca5b",
                "updated_at": "2016-06-27T00:36:14.000000"
            }
        ]
    }
]


"""Approval flags detail
APPROVAL_FLAGS[0]:
    next_status_code:final approval last_status_code:pre-approval
APPROVAL_FLAGS[1]:
    next_status_code:rejected last_status_code:pre-approval
APPROVAL_FLAGS[2]:
    next_status_code:canceled last_status_code:pre-approval
"""
APPROVAL_FLAGS = \
    [[('final approval:'
       'e4db1918-40d2-45e3-96a3-31fa848b2739:'
       'pre-approval:'
       'd343d7bc-3b98-4a39-9a27-4678ed3cfcb2'), u'Final approval'],
     [('rejected:'
       'b8bc188c-22c9-4e60-972c-fcf25e8f289f:'
       'pre-approval:'
       'd343d7bc-3b98-4a39-9a27-4678ed3cfcb2'), u'Rejected'],
     [('canceled:'
       '65c4dd79-9c9f-4935-8080-f5bf5817f906:'
       'pre-approval:'
       'd343d7bc-3b98-4a39-9a27-4678ed3cfcb2'), u'Canceled']]
