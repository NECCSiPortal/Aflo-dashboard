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

"""Catalog data detail
CATALOG_DATA_LIST[0]:catalog_id:100
CATALOG_DATA_LIST[1]:catalog_id:200
CATALOG_DATA_LIST[2]:catalog_id:300
CATALOG_DATA_LIST[3]:catalog_id:400
CATALOG_DATA_LIST[4]:catalog_id:500
"""
CATALOG_DATA_LIST = [
    {
        "catalog_id": "100",
        "catalog_name": "CPU 10 pieces S set",
        "lifetime_start": "2015-08-01T12:30:45.000000",
        "lifetime_end": "2016-08-01T12:30:45.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False,
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5"
        },
        "expansions_text": {
            "expansion_text": None
        }
    },
    {
        "catalog_id": "200",
        "catalog_name": "CPU 10 pieces M set",
        "lifetime_start": "2015-08-01T00:00:00.000000",
        "lifetime_end": "2016-08-30T23:59:59.000000",
        "created_at": "2015-08-30T23:59:59.000000",
        "deleted": False,
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5"
        },
        "expansions_text": {
            "expansion_text": None
        }
    },
    {
        "catalog_id": "300",
        "catalog_name": "CPU 10 pieces L set",
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "2016-08-31T23:59:59.000000",
        "created_at": "2015-08-29T23:59:59.000000",
        "deleted": False,
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5"
        },
        "expansions_text": {
            "expansion_text": None
        }
    },
    {
        "catalog_id": "400",
        "catalog_name": "Memory 10 GB S set",
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "2016-08-31T23:59:59.000000",
        "created_at": "2015-08-28T23:59:59.000000",
        "deleted": False,
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5"
        },
        "expansions_text": {
            "expansion_text": None
        }
    },
    {
        "catalog_id": "500",
        "catalog_name": "Memory 10 GB M set",
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "2016-08-31T23:59:59.000000",
        "created_at": "2015-08-27T23:59:59.000000",
        "deleted": False,
        "expansions": {
            "expansion_key1": "expansion1",
            "expansion_key2": "expansion2",
            "expansion_key3": "expansion3",
            "expansion_key4": "expansion4",
            "expansion_key5": "expansion5"
        },
        "expansions_text": {
            "expansion_text": None
        }
    }
]

PROJECT_ID = "5a53a6a5aab54293884b96e3cb1b1754"

"""Price data detail
PRICE_DATA_LIST[0]:catalog_id:100 Default
PRICE_DATA_LIST[1]:catalog_id:100 Project
PRICE_DATA_LIST[2]:catalog_id:200 Default
PRICE_DATA_LIST[3]:catalog_id:300 Project
PRICE_DATA_LIST[4]:catalog_id:400 Default
PRICE_DATA_LIST[5]:catalog_id:400 Project
"""
PRICE_DATA_LIST = [
    {
        "catalog_id": "100",
        "scope": "Default",
        "seq_no": "1",
        "price": 1000000,
        "lifetime_start": "2015-08-01T12:30:45.000000",
        "lifetime_end": "2016-08-01T12:30:45.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False
    },
    {
        "catalog_id": "100",
        "scope": PROJECT_ID,
        "seq_no": "2",
        "price": 2000000,
        "lifetime_start": "2015-08-01T12:30:45.000000",
        "lifetime_end": "2016-08-01T12:30:45.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False
    },
    {
        "catalog_id": "200",
        "scope": "Default",
        "seq_no": "3",
        "price": 3000000,
        "lifetime_start": "2015-08-01T00:00:00.000000",
        "lifetime_end": "2016-08-30T23:59:59.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False
    },
    {
        "catalog_id": "300",
        "scope": PROJECT_ID,
        "seq_no": "4",
        "price": 4000000,
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "2016-08-31T23:59:59.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False
    },
    {
        "catalog_id": "400",
        "scope": "Default",
        "seq_no": "5",
        "price": 5000000,
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "2016-08-31T23:59:59.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False
    },
    {
        "catalog_id": "400",
        "scope": PROJECT_ID,
        "seq_no": "6",
        "price": 6000000,
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "2016-08-31T23:59:59.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False
    },
    {
        "catalog_id": "500",
        "scope": "Default",
        "seq_no": "7",
        "price": 7000000,
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "2016-08-31T23:59:59.000000",
        "created_at": "2015-08-31T23:59:59.000000",
        "deleted": False
    }
]

"""Catalog scope data detail
CATALOG_SCOPE_DATA_LIST[0]:catalog_id:100 Default
CATALOG_SCOPE_DATA_LIST[1]:catalog_id:100 Project
CATALOG_SCOPE_DATA_LIST[2]:catalog_id:200 Default
CATALOG_SCOPE_DATA_LIST[3]:catalog_id:300 Project
CATALOG_SCOPE_DATA_LIST[4]:catalog_id:400 Default
CATALOG_SCOPE_DATA_LIST[5]:catalog_id:400 Project
"""
CATALOG_SCOPE_DATA_LIST = [
    {
        "id": "scope_id0-111-222-333-001",
        "catalog_id": "100",
        "scope": "Default",
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "9999-12-31T23:59:59.999999"
    },
    {
        "id": "scope_id0-111-222-333-002",
        "catalog_id": "100",
        "scope": PROJECT_ID,
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "9999-12-31T23:59:59.999999"
    },
    {
        "id": "scope_id0-111-222-333-003",
        "catalog_id": "200",
        "scope": "Default",
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "9999-12-31T23:59:59.999999"
    },
    {
        "id": "scope_id0-111-222-333-004",
        "catalog_id": "300",
        "scope": PROJECT_ID,
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "9999-12-31T23:59:59.999999"
    },
    {
        "id": "scope_id0-111-222-333-005",
        "catalog_id": "400",
        "scope": "Default",
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "9999-12-31T23:59:59.999999"
    },
    {
        "id": "scope_id0-111-222-333-006",
        "catalog_id": "400",
        "scope": PROJECT_ID,
        "lifetime_start": "2015-08-31T00:00:00.000000",
        "lifetime_end": "9999-12-31T23:59:59.999999"
    },
]

"""Vaild catalog data detail
VALID_DATA_LIST[0]:catalog_id:100 Default
VALID_DATA_LIST[1]:catalog_id:100 Project
VALID_DATA_LIST[2]:catalog_id:200 Default
VALID_DATA_LIST[3]:catalog_id:300 Project
VALID_DATA_LIST[4]:catalog_id:400 Default
VALID_DATA_LIST[5]:catalog_id:400 Project
"""
VALID_DATA_LIST = [
    {
        "catalog_id": "100",
        "scope": "Default",
        "catalog_name": "CPU 10 pieces S set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "1",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2015-08-01T12:30:45.000000",
        "price_seq_no": "1",
        "price": 1000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2015-08-01T12:30:45.000000",
    },
    {
        "catalog_id": "100",
        "scope": PROJECT_ID,
        "catalog_name": "CPU 10 pieces S set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "2",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2015-08-01T12:30:45.000000",
        "price_seq_no": "2",
        "price": 2000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2015-08-01T12:30:45.000000",
    },
    {
        "catalog_id": "200",
        "scope": "Default",
        "catalog_name": "CPU 10 pieces M set",
        "catalog_lifetime_start": "2015-08-01T00:00:00.000000",
        "catalog_lifetime_end": "2016-08-30T23:59:59.000000",
        "catalog_scope_id": "3",
        "catalog_scope_lifetime_start": "2015-08-01T00:00:00.000000",
        "catalog_scope_lifetime_end": "2016-08-30T23:59:59.000000",
        "price_seq_no": "3",
        "price": 3000000,
        "price_lifetime_start": "2015-08-01T00:00:00.000000",
        "price_lifetime_end": "2016-08-30T23:59:59.000000",
    },
    {
        "catalog_id": "300",
        "scope": PROJECT_ID,
        "catalog_name": "CPU 10 pieces L set",
        "catalog_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_lifetime_end": "2016-08-31T23:59:59.000000",
        "catalog_scope_id": "4",
        "catalog_scope_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_scope_lifetime_end": "2016-08-31T23:59:59.000000",
        "price_seq_no": "4",
        "price": 4000000,
        "price_lifetime_start": "2015-08-31T00:00:00.000000",
        "price_lifetime_end": "2016-08-31T23:59:59.000000",
    },
    {
        "catalog_id": "400",
        "scope": "Default",
        "catalog_name": "Memory 10 GB S set",
        "catalog_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_lifetime_end": "2016-08-31T23:59:59.000000",
        "catalog_scope_id": "5",
        "catalog_scope_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_scope_lifetime_end": "2016-08-31T23:59:59.000000",
        "price_seq_no": "5",
        "price": 5000000,
        "price_lifetime_start": "2015-08-31T00:00:00.000000",
        "price_lifetime_end": "2016-08-31T23:59:59.000000",
    },
    {
        "catalog_id": "400",
        "scope": PROJECT_ID,
        "catalog_name": "Memory 10 GB S set",
        "catalog_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_lifetime_end": "2016-08-31T23:59:59.000000",
        "catalog_scope_id": "6",
        "catalog_scope_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_scope_lifetime_end": "2016-08-31T23:59:59.000000",
        "price_seq_no": "6",
        "price": 6000000,
        "price_lifetime_start": "2015-08-31T00:00:00.000000",
        "price_lifetime_end": "2016-08-31T23:59:59.000000",
    },
    {
        "catalog_id": "500",
        "scope": "Default",
        "catalog_name": "Memory 10 GB M set",
        "catalog_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_lifetime_end": "2016-08-31T23:59:59.000000",
        "catalog_scope_id": "7",
        "catalog_scope_lifetime_start": "2015-08-31T00:00:00.000000",
        "catalog_scope_lifetime_end": "2016-08-31T23:59:59.000000",
        "price_seq_no": "7",
        "price": 7000000,
        "price_lifetime_start": "2015-08-31T00:00:00.000000",
        "price_lifetime_end": "2016-08-31T23:59:59.000000",
    }
]

"""Valid public catalog data detail
VALID_PUBLIC_DATA_LIST[0]:catalog_id:100 Default
VALID_PUBLIC_DATA_LIST[1]:catalog_id:200 Default
VALID_PUBLIC_DATA_LIST[2]:catalog_id:400 Default
"""
VALID_PUBLIC_DATA_LIST = [
    {
        "catalog_id": "100",
        "scope": "Default",
        "catalog_name": "CPU 10 pieces S set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "scope_id0-111-222-333-001",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2016-08-01T12:30:45.000000",
        "price_seq_no": "1",
        "price": 1000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2016-08-01T12:30:45.000000"
    },
    {
        "catalog_id": "200",
        "scope": "Default",
        "catalog_name": "CPU 10 pieces M set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "scope_id0-111-222-333-003",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2016-08-01T12:30:45.000000",
        "price_seq_no": "3",
        "price": 3000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2016-08-01T12:30:45.000000"
    },
    {
        "catalog_id": "400",
        "scope": "Default",
        "catalog_name": "Memory 10 GB S set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "scope_id0-111-222-333-005",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2016-08-01T12:30:45.000000",
        "price_seq_no": "5",
        "price": 5000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2016-08-01T12:30:45.000000"
    }
]

"""Valid private catalog data detail
VALID_PRIVATE_DATA_LIST[0]:catalog_id:100 Project
VALID_PRIVATE_DATA_LIST[1]:catalog_id:300 Project
VALID_PRIVATE_DATA_LIST[2]:catalog_id:400 Project
"""
VALID_PRIVATE_DATA_LIST = [
    {
        "catalog_id": "100",
        "scope": PROJECT_ID,
        "catalog_name": "CPU 10 pieces S set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "scope_id0-111-222-333-002",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2016-08-01T12:30:45.000000",
        "price_seq_no": "2",
        "price": 2000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2016-08-01T12:30:45.000000"
    },
    {
        "catalog_id": "300",
        "scope": PROJECT_ID,
        "catalog_name": "CPU 10 pieces L set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "scope_id0-111-222-333-004",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2016-08-01T12:30:45.000000",
        "price_seq_no": "4",
        "price": 4000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2016-08-01T12:30:45.000000"
    },
    {
        "catalog_id": "400",
        "scope": PROJECT_ID,
        "catalog_name": "Memory 10 GB S set",
        "catalog_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_lifetime_end": "2016-08-01T12:30:45.000000",
        "catalog_scope_id": "scope_id0-111-222-333-006",
        "catalog_scope_lifetime_start": "2015-08-01T12:30:45.000000",
        "catalog_scope_lifetime_end": "2016-08-01T12:30:45.000000",
        "price_seq_no": "6",
        "price": 6000000,
        "price_lifetime_start": "2015-08-01T12:30:45.000000",
        "price_lifetime_end": "2016-08-01T12:30:45.000000"
    }
]

"""Catalog id"""
CATALOG_ID = "100"
