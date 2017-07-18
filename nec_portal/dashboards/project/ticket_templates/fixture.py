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
CONTRACT_TICKET_TEMPLATE_DATA_LIST[0]:New Contract
    inner data of special string : "'<>\%
    id:10
CONTRACT_TICKET_TEMPLATE_DATA_LIST[1]:Cancel Contract
    id:11
CONTRACT_TICKET_TEMPLATE_DATA_LIST[2]:TEST-DATA
    id:90
CONTRACT_TICKET_TEMPLATE_DATA_LIST[3]:TEST-DATA
    id:91
CONTRACT_TICKET_TEMPLATE_DATA_LIST[4]:TEST-DATA
    id:92
"""
CONTRACT_TICKET_TEMPLATE_DATA_LIST = [
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow_pattern": {
            "code": "contract_workflow",
            "created_at": "2015-09-08T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "10",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "awaiting approval"
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
                    {
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
                    {
                        "next_status": [{}],
                        "status_code": "reject",
                        "status_name": {
                            "Default": "Reject",
                            "ja": "\u5426\u8a8d"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "withdrawn",
                        "status_name": {
                            "Default": "Withdrawn",
                            "ja": "\u53d6\u308a\u4e0b\u3052"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "approval",
                        "status_name": {
                            "Default": "Approval",
                            "ja": "\u627f\u8a8d"
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
            "param": [
                {
                    "max_length": "",
                    "max_val": "9999",
                    "min_length": "",
                    "min_val": "0",
                    "name": {
                        "Default": "Gold VCPU x 10 CORE(S)",
                        "ja": "\u677e VCPU x 10 CORE(S)"
                    },
                    "required": "True",
                    "type": "number"
                },
                {
                    "max_length": "",
                    "max_val": "9999",
                    "min_length": "",
                    "min_val": "0",
                    "name": {
                        "Default": "Silver VCPU x 10 CORE(S)",
                        "ja": "\u7af9 VCPU x 10 CORE(S)"
                    },
                    "required": "True",
                    "type": "number"
                },
                {
                    "max_length": "",
                    "max_val": "9999",
                    "min_length": "",
                    "min_val": "0",
                    "name": {
                        "Default": "Bronze VCPU x 10 CORE(S)",
                        "ja": "\u6885 VCPU x 10 CORE(S)"
                    },
                    "required": "True",
                    "type": "number"
                },
                {
                    "max_length": "",
                    "max_val": "9999",
                    "min_length": "",
                    "min_val": "0",
                    "name": {
                        "Default": "RAM 20 GB",
                        "ja": "RAM 20 GB"
                    },
                    "required": "True",
                    "type": "number"
                },
                {
                    "max_length": "",
                    "max_val": "9999",
                    "min_length": "",
                    "min_val": "0",
                    "name": {
                        "Default": "Volume Storage 50 GB",
                        "ja":
                            "\u30dc\u30ea\u30e5\u30fc"
                            "\u30e0\u30b9\u30c8\u30ec\u30fc\u30b8 50 GB"
                    },
                    "required": "True",
                    "type": "number"
                },
                {
                    "max_length": "512",
                    "max_val": "",
                    "min_length": "0",
                    "min_val": "",
                    "name": {
                        "Default": "Message",
                        "ja": "\u30e1\u30c3\u30bb\u30fc\u30b8"
                    },
                    "required": "False",
                    "type": "string"
                }
            ],
            "target_id": [
                "catalog0-1111-2222-3333-000000000005",
                "catalog0-1111-2222-3333-000000000004",
                "catalog0-1111-2222-3333-000000000003",
                "catalog0-1111-2222-3333-000000000002",
                "catalog0-1111-2222-3333-000000000001"
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
        "workflow_pattern": {
            "code": "contract_workflow",
            "created_at": "2015-09-08T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "10",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "awaiting approval"
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
                    {
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
                    {
                        "next_status": [{}],
                        "status_code": "reject",
                        "status_name": {
                            "Default": "Reject",
                            "ja": "\u5426\u8a8d"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "withdrawn",
                        "status_name": {
                            "Default": "Withdrawn",
                            "ja": "\u53d6\u308a\u4e0b\u3052"
                        }
                    },
                    {
                        "next_status": [{}],
                        "status_code": "approval",
                        "status_name": {
                            "Default": "Approval",
                            "ja": "\u627f\u8a8d"
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
            "param": [
                {
                    "max_length": "512",
                    "max_val": "",
                    "min_length": "0",
                    "min_val": "",
                    "name": {
                        "Default": "Message",
                        "ja": "\u30e1\u30c3\u30bb\u30fc\u30b8"
                    },
                    "required": "False",
                    "type": "string"
                }
            ],
            "target_id": [
                "catalog0-1111-2222-3333-000000000005",
                "catalog0-1111-2222-3333-000000000004",
                "catalog0-1111-2222-3333-000000000003",
                "catalog0-1111-2222-3333-000000000002",
                "catalog0-1111-2222-3333-000000000001"
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
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "created_at": "2015-09-08T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "90",
        "template_contents": {
            "action": {
                "broker": [],
                "broker_class": ""
            },
            "application_kinds_name": {
                "Default": "TEST-DATA",
                "ja": "TEST-DATA(ja)"
            },
            "first_status_code": "awaiting approval",
            "param": [],
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
        "id": "91",
        "template_contents": {
            "action": {
                "broker": [],
                "broker_class": ""
            },
            "application_kinds_name": {
                "Default": "TEST-DATA",
                "ja": "TEST-DATA(ja)"
            },
            "first_status_code": "awaiting approval",
            "param": [],
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
        "id": "92",
        "template_contents": {
            "action": {
                "broker": [],
                "broker_class": ""
            },
            "application_kinds_name": {
                "Default": "TEST-DATA",
                "ja": "TEST-DATA(ja)"
            },
            "first_status_code": "awaiting approval",
            "param": [],
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
    }
]


"""Contract tickettemplate data detail
REQUEST_TICKET_TEMPLATE_DATA_LIST[0]:Add User
    id:20
REQUEST_TICKET_TEMPLATE_DATA_LIST[1]:Inquiry
    id:21
REQUEST_TICKET_TEMPLATE_DATA_LIST[2]:TEST-DATA
    id:90
REQUEST_TICKET_TEMPLATE_DATA_LIST[3]:TEST-DATA
    id:91
REQUEST_TICKET_TEMPLATE_DATA_LIST[4]:TEST-DATA
    id:92
"""
REQUEST_TICKET_TEMPLATE_DATA_LIST = [
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow_pattern": {
            "code": "request_workflow",
            "created_at": "2015-09-08T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "20",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "inquiring"
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
                                "grant_role": "wf_request_support",
                                "next_status_code": "working"
                            },
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "inquiring",
                        "status_name": {
                            "Default": "Inquiring",
                            "ja": "\u4f9d\u983c\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "working",
                        "status_name": {
                            "Default": "Working",
                            "ja": "\u4f5c\u696d\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "closed"
                            }
                        ],
                        "status_code": "done",
                        "status_name": {
                            "Default": "Done",
                            "ja": "\u4f5c\u696d\u7d42\u4e86"
                        }
                    },
                    {
                        "next_status": [
                            {}
                        ],
                        "status_code": "closed",
                        "status_name": {
                            "Default": "Closed",
                            "ja": "\u30af\u30ed\u30fc\u30ba"
                        }
                    }
                ],
                "wf_pattern_code": "request_workflow",
                "wf_pattern_name": {
                    "Default": "Request Workflow",
                    "ja":
                        "\u4f5c\u696d\u4f9d\u983c"
                        "\u30ef\u30fc\u30af\u30d5\u30ed\u30fc"
                }
            }
        },
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
            "param": [
                {
                    "min_length": "1",
                    "name": {
                        "Default": "User Name",
                        "ja": "\u30e6\u30fc\u30b6\u30fc\u540d"
                    },
                    "required": "True",
                    "min_val": "",
                    "max_val": "",
                    "max_length": "255",
                    "type": "string"
                },
                {
                    "min_length": "",
                    "name": {
                        "Default": "Email",
                        "ja": "\u30e1\u30fc\u30eb"
                    },
                    "required": "False",
                    "min_val": "",
                    "max_val": "",
                    "max_length": "",
                    "type": "e-mail"
                },
                {
                    "min_length": "",
                    "name": {
                        "Default": "Role",
                        "ja": "\u6a29\u9650"
                    },
                    "required": "False",
                    "min_val": "",
                    "max_val": "",
                    "max_length": "",
                    "type": "string"
                },
                {
                    "min_length": "0",
                    "name": {
                        "Default": "Message",
                        "ja": "\u30e1\u30c3\u30bb\u30fc\u30b8"
                    },
                    "required": "False",
                    "min_val": "",
                    "max_val": "",
                    "max_length": "512",
                    "type": "string"
                }
            ],
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
                        "validation": "message_check",
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
                        "validation": "message_check",
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
                        "validation": "message_check",
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
        "workflow_pattern": {
            "code": "request_workflow",
            "created_at": "2015-09-08T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "20",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "inquiring"
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
                                "grant_role": "wf_request_support",
                                "next_status_code": "working"
                            },
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "inquiring",
                        "status_name": {
                            "Default": "Inquiring",
                            "ja": "\u4f9d\u983c\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "working",
                        "status_name": {
                            "Default": "Working",
                            "ja": "\u4f5c\u696d\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "closed"
                            }
                        ],
                        "status_code": "done",
                        "status_name": {
                            "Default": "Done",
                            "ja": "\u4f5c\u696d\u7d42\u4e86"
                        }
                    },
                    {
                        "next_status": [
                            {}
                        ],
                        "status_code": "closed",
                        "status_name": {
                            "Default": "Closed",
                            "ja": "\u30af\u30ed\u30fc\u30ba"
                        }
                    }
                ],
                "wf_pattern_code": "request_workflow",
                "wf_pattern_name": {
                    "Default": "Request Workflow",
                    "ja":
                        "\u4f5c\u696d\u4f9d\u983c"
                        "\u30ef\u30fc\u30af\u30d5\u30ed\u30fc"
                }
            }
        },
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
            "param": [
                {
                    "min_length": "1",
                    "name": {
                        "Default": "Message",
                        "ja": "\u30e1\u30c3\u30bb\u30fc\u30b8"
                    },
                    "required": "True",
                    "min_val": "",
                    "max_val": "",
                    "max_length": "512",
                    "type": "string"
                }
            ],
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
                        "validation": "message_check",
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
                        "validation": "message_check",
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
                        "validation": "message_check",
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
    },
    {
        "roles": [
            "_member_",
            "wf_apply"
        ],
        "workflow_pattern": {
            "code": "request_workflow",
            "created_at": "2015-09-08T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "20",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "inquiring"
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
                                "grant_role": "wf_request_support",
                                "next_status_code": "working"
                            },
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "inquiring",
                        "status_name": {
                            "Default": "Inquiring",
                            "ja": "\u4f9d\u983c\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "working",
                        "status_name": {
                            "Default": "Working",
                            "ja": "\u4f5c\u696d\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "closed"
                            }
                        ],
                        "status_code": "done",
                        "status_name": {
                            "Default": "Done",
                            "ja": "\u4f5c\u696d\u7d42\u4e86"
                        }
                    },
                    {
                        "next_status": [
                            {}
                        ],
                        "status_code": "closed",
                        "status_name": {
                            "Default": "Closed",
                            "ja": "\u30af\u30ed\u30fc\u30ba"
                        }
                    }
                ],
                "wf_pattern_code": "request_workflow",
                "wf_pattern_name": {
                    "Default": "Request Workflow",
                    "ja":
                        "\u4f5c\u696d\u4f9d\u983c"
                        "\u30ef\u30fc\u30af\u30d5\u30ed\u30fc"
                }
            }
        },
        "created_at": "2015-09-08T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "90",
        "template_contents": {
            "action": {
                "broker": [],
                "broker_class": ""
            },
            "application_kinds_name": {
                "Default": "TEST-DATA",
                "ja": "TEST-DATA(ja)"
            },
            "first_status_code": "awaiting approval",
            "param": [],
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
        "workflow_pattern": {
            "code": "request_workflow",
            "created_at": "2015-09-08T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "20",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "inquiring"
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
                                "grant_role": "wf_request_support",
                                "next_status_code": "working"
                            },
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "inquiring",
                        "status_name": {
                            "Default": "Inquiring",
                            "ja": "\u4f9d\u983c\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "working",
                        "status_name": {
                            "Default": "Working",
                            "ja": "\u4f5c\u696d\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "closed"
                            }
                        ],
                        "status_code": "done",
                        "status_name": {
                            "Default": "Done",
                            "ja": "\u4f5c\u696d\u7d42\u4e86"
                        }
                    },
                    {
                        "next_status": [
                            {}
                        ],
                        "status_code": "closed",
                        "status_name": {
                            "Default": "Closed",
                            "ja": "\u30af\u30ed\u30fc\u30ba"
                        }
                    }
                ],
                "wf_pattern_code": "request_workflow",
                "wf_pattern_name": {
                    "Default": "Request Workflow",
                    "ja":
                        "\u4f5c\u696d\u4f9d\u983c"
                        "\u30ef\u30fc\u30af\u30d5\u30ed\u30fc"
                }
            }
        },
        "created_at": "2015-09-08T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "91",
        "template_contents": {
            "action": {
                "broker": [],
                "broker_class": ""
            },
            "application_kinds_name": {
                "Default": "TEST-DATA",
                "ja": "TEST-DATA(ja)"
            },
            "first_status_code": "awaiting approval",
            "param": [],
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
        "workflow_pattern": {
            "code": "request_workflow",
            "created_at": "2015-09-08T00:00:00.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "20",
            "updated_at": None,
            "wf_pattern_contents": {
                "status_list": [
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "inquiring"
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
                                "grant_role": "wf_request_support",
                                "next_status_code": "working"
                            },
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "inquiring",
                        "status_name": {
                            "Default": "Inquiring",
                            "ja": "\u4f9d\u983c\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "wf_request_support",
                                "next_status_code": "done"
                            }
                        ],
                        "status_code": "working",
                        "status_name": {
                            "Default": "Working",
                            "ja": "\u4f5c\u696d\u4e2d"
                        }
                    },
                    {
                        "next_status": [
                            {
                                "grant_role": "_member_",
                                "next_status_code": "closed"
                            }
                        ],
                        "status_code": "done",
                        "status_name": {
                            "Default": "Done",
                            "ja": "\u4f5c\u696d\u7d42\u4e86"
                        }
                    },
                    {
                        "next_status": [
                            {}
                        ],
                        "status_code": "closed",
                        "status_name": {
                            "Default": "Closed",
                            "ja": "\u30af\u30ed\u30fc\u30ba"
                        }
                    }
                ],
                "wf_pattern_code": "request_workflow",
                "wf_pattern_name": {
                    "Default": "Request Workflow",
                    "ja":
                        "\u4f5c\u696d\u4f9d\u983c"
                        "\u30ef\u30fc\u30af\u30d5\u30ed\u30fc"
                }
            }
        },
        "created_at": "2015-09-08T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "92",
        "template_contents": {
            "action": {
                "broker": [],
                "broker_class": ""
            },
            "application_kinds_name": {
                "Default": "TEST-DATA",
                "ja": "TEST-DATA(ja)"
            },
            "first_status_code": "awaiting approval",
            "param": [],
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
    }
]


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
