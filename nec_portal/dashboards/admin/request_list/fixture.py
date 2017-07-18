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

"""Request tickettemplate data detail
REQUEST_TICKET_TEMPLATE_DATA_LIST[0]:request_user_entry
    inner data of special string : "'<>\%
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
                "ja": "\"'<>\%\u30e6\u30fc\u30b6\u30fc\u767b\u9332\u7533\u8acb"
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
            "form_key": "request_user_entry"
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
            "form_key": "request_contact"
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

"""Ticket template data detail
TICKET_TEMPLATE_DATA_LIST[0]:id:1 one approver
TICKET_TEMPLATE_DATA_LIST[1]:id:2 three approver
"""
sample_broker = "aflo.tickets.broker.sample_broker.SampleBroker"
TICKET_TEMPLATE_DATA_LIST = [
    {
        "created_at": "2015-07-07T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "1",
        "template_contents": {
            "action": {
                "broker": [
                    {
                        "broker_method": "",
                        "status": "approval",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "sendmail",
                        "status": "approval",
                        "timing": "after",
                        "validation": ""
                    }
                ],
                "broker_class": sample_broker
            },
            "first_status_code": "approval",
            "param": {
                "param": [
                    {
                        "max_length": "",
                        "max_val": "999",
                        "min_length": "",
                        "min_val": "1",
                        "name": {
                            "Default": "num",
                            "ja": "\u500b\u6570"
                        },
                        "required": "True",
                        "type": "integer"
                    },
                    {
                        "max_length": "128",
                        "max_val": "",
                        "min_length": "0",
                        "min_val": "",
                        "name": {
                            "Default": "description",
                            "ja": "\u5099\u8003"
                        },
                        "required": "False",
                        "type": "string"
                    }
                ]
            },
            "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            "ticket_template_name": {
                "Default": "flat-rate",
                "ja": "Quota\u8cb7\u3044"
            },
            "ticket_type": "goods",
            "wf_pattern_code": "one_approver"
        },
        "updated_at": None,
        "workflow_pattern_id": "1"
    },
    {
        "created_at": "2015-07-07T00:00:00.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "2",
        "template_contents": {
            "action": {
                "broker": [
                    {
                        "broker_method": "",
                        "status": "awaiting approval",
                        "timing": "before",
                        "validation": ""
                    },
                    {
                        "broker_method": "sendmail",
                        "status": "awaiting approval",
                        "timing": "after",
                        "validation": ""
                    },
                    {
                        "broker_method": "sendmail",
                        "status": "withdrawn",
                        "timing": "after",
                        "validation": ""
                    },
                    {
                        "broker_method": "sendmail",
                        "status": "reject",
                        "timing": "after",
                        "validation": ""
                    },
                    {
                        "broker_method": "sendmail",
                        "status": "check",
                        "timing": "after",
                        "validation": ""
                    },
                    {
                        "broker_method": "sendmail",
                        "status": "approval",
                        "timing": "after",
                        "validation": ""
                    }
                ],
                "broker_class": sample_broker
            },
            "first_status_code": "awaiting approval",
            "param": {
                "param": [
                    {
                        "max_length": "",
                        "max_val": "999",
                        "min_length": "",
                        "min_val": "1",
                        "name": {
                            "Default": "num",
                            "ja": "\u500b\u6570"
                        },
                        "required": "True",
                        "type": "integer"
                    },
                    {
                        "max_length": "128",
                        "max_val": "",
                        "min_length": "0",
                        "min_val": "",
                        "name": {
                            "Default": "description",
                            "ja": "\u5099\u8003"
                        },
                        "required": "False",
                        "type": "string"
                    }
                ]
            },
            "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
            "ticket_template_name": {
                "Default": "pay-for-use",
                "ja": "\u5f93\u91cf\u8ab2\u91d1"
            },
            "ticket_type": "goods",
            "wf_pattern_code": "three_approver"
        },
        "updated_at": None,
        "workflow_pattern_id": "2"
    }
]

"""Ticket data detail
TICKET_DATA_LIST[0]:one approver   last_status_code:approval
TICKET_DATA_LIST[1]:one approver   last_status_code:approval
TICKET_DATA_LIST[2]:one approver   last_status_code:approval
TICKET_DATA_LIST[3]:one approver   last_status_code:approval
TICKET_DATA_LIST[4]:three approver last_status_code:awaiting approval
TICKET_DATA_LIST[5]:three approver last_status_code:check
"""
TICKET_DATA_LIST = [
    {
        "action_detail": "",
        "created_at": "2015-07-29T20:53:36.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "f93f8b63-6847-4c98-86d9-6a538c9702e6",
        "last_workflow": {
            "additional_data": "",
            "confirmed_at": "2015-07-29T20:53:35.000000",
            "confirmer_id": "b0e2f399de544ba6b33fe11be9cca3be",
            "confirmer_name": "user-a",
            "created_at": "2015-07-29T20:53:36.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "42bf7e18-df86-434f-be85-c827ef83d1da",
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
            "ticket_id": "f93f8b63-6847-4c98-86d9-6a538c9702e6",
            "updated_at": "2015-07-29T20:53:36.000000"
        },
        "owner_at": "2015-07-29T20:53:35.000000",
        "owner_id": "b0e2f399de544ba6b33fe11be9cca3be",
        "owner_name": "user-a",
        "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        "tenant_id": "7a867af0702c435981cfb970998b2337",
        "tenant_name": "project-a",
        "ticket_detail": {
            "description": "approved.",
            "nop": 500
        },
        "ticket_template_id": "1",
        "ticket_type": "goods",
        "updated_at": "2015-07-29T20:53:36.000000"
    },
    {
        "action_detail": "",
        "created_at": "2015-07-29T20:53:28.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "b0536e64-e20f-4280-88bf-deafaae8d3d0",
        "last_workflow": {
            "additional_data": "",
            "confirmed_at": "2015-07-29T20:53:27.000000",
            "confirmer_id": "b0e2f399de544ba6b33fe11be9cca3be",
            "confirmer_name": "user-a",
            "created_at": "2015-07-29T20:53:29.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "6cce8316-30c4-42e2-8bf8-5cfeb0f56e75",
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
            "ticket_id": "b0536e64-e20f-4280-88bf-deafaae8d3d0",
            "updated_at": "2015-07-29T20:53:29.000000"
        },
        "owner_at": "2015-07-29T20:53:27.000000",
        "owner_id": "b0e2f399de544ba6b33fe11be9cca3be",
        "owner_name": "user-a",
        "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        "tenant_id": "7a867af0702c435981cfb970998b2337",
        "tenant_name": "project-a",
        "ticket_detail": {
            "description": "approved.",
            "nop": 400
        },
        "ticket_template_id": "1",
        "ticket_type": "goods",
        "updated_at": "2015-07-29T20:53:28.000000"
    },
    {
        "action_detail": "",
        "created_at": "2015-07-29T20:53:20.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "4dc9c279-53ed-47fc-a210-12f2dcea5c50",
        "last_workflow": {
            "additional_data": "",
            "confirmed_at": "2015-07-29T20:53:18.000000",
            "confirmer_id": "b0e2f399de544ba6b33fe11be9cca3be",
            "confirmer_name": "user-a",
            "created_at": "2015-07-29T20:53:21.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "19521d6d-e777-40c0-b253-ee6fb1ad9461",
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
            "ticket_id": "4dc9c279-53ed-47fc-a210-12f2dcea5c50",
            "updated_at": "2015-07-29T20:53:21.000000"
        },
        "owner_at": "2015-07-29T20:53:18.000000",
        "owner_id": "b0e2f399de544ba6b33fe11be9cca3be",
        "owner_name": "user-a",
        "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        "tenant_id": "7a867af0702c435981cfb970998b2337",
        "tenant_name": "project-a",
        "ticket_detail": {
            "description": "approved.",
            "nop": 300
        },
        "ticket_template_id": "1",
        "ticket_type": "goods",
        "updated_at": "2015-07-29T20:53:20.000000"
    },
    {
        "action_detail": "",
        "created_at": "2015-07-29T20:53:18.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "d53a4e9c-f61f-4c21-b278-25c6d2d6e420",
        "last_workflow": {
            "additional_data": "",
            "confirmed_at": "2015-07-29T20:53:11.000000",
            "confirmer_id": "b0e2f399de544ba6b33fe11be9cca3be",
            "confirmer_name": "user-a",
            "created_at": "2015-07-29T20:53:18.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "c2e4a826-0c5a-4287-8a26-9a59199f6ed4",
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
            "ticket_id": "d53a4e9c-f61f-4c21-b278-25c6d2d6e420",
            "updated_at": "2015-07-29T20:53:18.000000"
        },
        "owner_at": "2015-07-29T20:53:11.000000",
        "owner_id": "b0e2f399de544ba6b33fe11be9cca3be",
        "owner_name": "user-a",
        "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        "tenant_id": "7a867af0702c435981cfb970998b2337",
        "tenant_name": "project-a",
        "ticket_detail": {
            "description": "approved.",
            "nop": 200
        },
        "ticket_template_id": "1",
        "ticket_type": "goods",
        "updated_at": "2015-07-29T20:53:18.000000"
    },
    {
        "action_detail": "",
        "created_at": "2015-07-29T20:52:49.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "99364350-a452-4eff-9b7b-fb207f6b01f8",
        "last_workflow": {
            "additional_data": "",
            "confirmed_at": "2015-07-29T20:52:44.000000",
            "confirmer_id": "b0e2f399de544ba6b33fe11be9cca3be",
            "confirmer_name": "user-a",
            "created_at": "2015-07-29T20:52:49.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "51e3f8b5-2a22-4374-bef2-9ff5143c54cf",
            "status": 1,
            "status_code": "awaiting approval",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "project_manager_a",
                        "next_status_code": "check"
                    },
                    {
                        "grant_role": "project_manager_a",
                        "next_status_code": "reject"
                    },
                    {
                        "grant_role": "_member_",
                        "next_status_code": "withdrawn"
                    }
                ],
                "status_code": "awaiting approval",
                "status_name": {
                    "Default": "Awaiting approval",
                    "ja": "\u7533\u8acb\u4e2d"
                }
            },
            "target_role": "none",
            "ticket_id": "99364350-a452-4eff-9b7b-fb207f6b01f8",
            "updated_at": "2015-07-29T20:52:49.000000"
        },
        "owner_at": "2015-07-29T20:52:44.000000",
        "owner_id": "b0e2f399de544ba6b33fe11be9cca3be",
        "owner_name": "user-a",
        "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
        "tenant_id": "7a867af0702c435981cfb970998b2337",
        "tenant_name": "project-a",
        "ticket_detail": {
            "description": "awaiting approval.",
            "nop": 100
        },
        "ticket_template_id": "2",
        "ticket_type": "goods",
        "updated_at": "2015-07-29T20:52:49.000000"
    },
    {
        "action_detail": "",
        "created_at": "2015-07-29T21:39:05.000000",
        "deleted": False,
        "deleted_at": None,
        "id": "02262dc1-9906-41bc-822d-426a5ba3f767",
        "last_workflow": {
            "additional_data": {
                "description": "inspectioned."
            },
            "confirmed_at": "2015-07-29T21:40:21.000000",
            "confirmer_id": "e9db2c3e046d4adbb326a1df4defba8e",
            "confirmer_name": "muser-a",
            "created_at": "2015-07-29T21:39:05.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "72a52569-8d9a-4156-b5a9-357a09181320",
            "status": 1,
            "status_code": "check",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "project_manager_b",
                        "next_status_code": "approval"
                    },
                    {
                        "grant_role": "project_manager_b",
                        "next_status_code": "reject"
                    }
                ],
                "status_code": "check",
                "status_name": {
                    "Default": "Check",
                    "ja": "\u67fb\u95b2"
                }
            },
            "target_role": "none",
            "ticket_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
            "updated_at": "2015-07-29T21:40:22.000000"
        },
        "owner_at": "2015-07-29T21:39:03.000000",
        "owner_id": "b0e2f399de544ba6b33fe11be9cca3be",
        "owner_name": "user-a",
        "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
        "tenant_id": "7a867af0702c435981cfb970998b2337",
        "tenant_name": "project-a",
        "ticket_detail": {
            "description": "approved.",
            "nop": 700
        },
        "ticket_template_id": "2",
        "ticket_type": "goods",
        "updated_at": "2015-07-29T21:39:05.000000"
    }
]

"""Ticket get data detail
TICKET_GET_DATA:three approver last_status_code:awaiting approval
"""
TICKET_GET_DATA = {
    "action_detail": "",
    "created_at": "2015-07-29T21:39:05.000000",
    "deleted": False,
    "deleted_at": None,
    "id": "02262dc1-9906-41bc-822d-426a5ba3f767",
    "owner_at": "2015-07-29T21:39:03.000000",
    "owner_id": "b0e2f399de544ba6b33fe11be9cca3be",
    "owner_name": "user-a",
    "roles": [
        "_member_"
    ],
    "target_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
    "tenant_id": "7a867af0702c435981cfb970998b2337",
    "tenant_name": "project-a",
    "ticket_detail": '{"description": "approved.","nop": 700}',
    "ticket_template_id": "2",
    "ticket_type": "goods",
    "updated_at": "2015-07-29T21:39:05.000000",
    "workflow": [
        {
            "additional_data": "",
            "confirmed_at": "2015-07-29T21:39:03.000000",
            "confirmer_id": "b0e2f399de544ba6b33fe11be9cca3be",
            "confirmer_name": "user-a",
            "created_at": "2015-07-29T21:39:05.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "0a8dfe64-0e20-4add-b870-029d4f687d39",
            "status": 2,
            "status_code": "awaiting approval",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "project_manager_a",
                        "next_status_code": "check"
                    },
                    {
                        "grant_role": "project_manager_a",
                        "next_status_code": "reject"
                    },
                    {
                        "grant_role": "_member_",
                        "next_status_code": "withdrawn"
                    }
                ],
                "status_code": "awaiting approval",
                "status_name": {
                    "Default": "Awaiting approval",
                    "ja": "\u7533\u8acb\u4e2d"
                }
            },
            "target_role": "none",
            "ticket_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
            "updated_at": "2015-07-29T21:40:22.000000"
        },
        {
            "additional_data": "",
            "confirmed_at": None,
            "confirmer_id": None,
            "confirmer_name": None,
            "created_at": "2015-07-29T21:39:05.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "0e6ae7ee-e703-4916-8785-8b440638a709",
            "status": 0,
            "status_code": "reject",
            "status_detail": {
                "next_status": [
                    {}
                ],
                "status_code": "reject",
                "status_name": {
                    "Default": "Reject",
                    "ja": "\u5426\u8a8d"
                }
            },
            "target_role": "none",
            "ticket_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
            "updated_at": "2015-07-29T21:39:05.000000"
        },
        {
            "additional_data": "",
            "confirmed_at": None,
            "confirmer_id": None,
            "confirmer_name": None,
            "created_at": "2015-07-29T21:39:05.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "33c824ca-7ec8-44de-ba35-364cb9a380df",
            "status": 0,
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
            "ticket_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
            "updated_at": "2015-07-29T21:39:05.000000"
        },
        {
            "additional_data": '{"description": "inspectioned."}',
            "confirmed_at": "2015-07-29T21:40:21.000000",
            "confirmer_id": "e9db2c3e046d4adbb326a1df4defba8e",
            "confirmer_name": "muser-a",
            "created_at": "2015-07-29T21:39:05.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "72a52569-8d9a-4156-b5a9-357a09181320",
            "status": 1,
            "status_code": "check",
            "status_detail": {
                "next_status": [
                    {
                        "grant_role": "project_manager_b",
                        "next_status_code": "approval"
                    },
                    {
                        "grant_role": "project_manager_b",
                        "next_status_code": "reject"
                    }
                ],
                "status_code": "check",
                "status_name": {
                    "Default": "Check",
                    "ja": "\u67fb\u95b2"
                }
            },
            "target_role": "none",
            "ticket_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
            "updated_at": "2015-07-29T21:40:22.000000"
        },
        {
            "additional_data": "",
            "confirmed_at": None,
            "confirmer_id": None,
            "confirmer_name": None,
            "created_at": "2015-07-29T21:39:05.000000",
            "deleted": False,
            "deleted_at": None,
            "id": "8dae74e0-f1e4-4703-a274-308d72217061",
            "status": 0,
            "status_code": "withdrawn",
            "status_detail": {
                "next_status": [
                    {}
                ],
                "status_code": "withdrawn",
                "status_name": {
                    "Default": "Withdrawn",
                    "ja": "\u53d6\u308a\u4e0b\u3052"
                }
            },
            "target_role": "none",
            "ticket_id": "02262dc1-9906-41bc-822d-426a5ba3f767",
            "updated_at": "2015-07-29T21:39:05.000000"
        }
    ]
}

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


"""Ticket id"""
TICKET_ID = "02262dc1-9906-41bc-822d-426a5ba3f767"


"""Project get data detail
PROJECT_GET_DATA:project a
"""
PROJECT_GET_DATA = {
    "enabled": True,
    "description": "project a",
    "name": "project-a",
    "id": "7a867af0702c435981cfb970998b2337"
}
