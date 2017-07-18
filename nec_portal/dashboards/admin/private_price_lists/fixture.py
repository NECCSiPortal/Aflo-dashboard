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

TENANT_DATA_LIST = [
    {
        "id": "696111a61ec94c3188a90c017de1ebb9",
        "name": "services",
        "description": "Tenant for the openstack services"
    },
    {
        "id": "a0d58ee41a364026a1031aca2548fd03",
        "name": "demo",
        "description": "Tenant for the openstack demo"
    },
    {
        "id": "bdb8f50f82da4370813e6ea797b1fb87",
        "name": "admin",
        "description": "Tenant for the openstack admin"
    },
    {
        "id": "a0d58ee41a364026a1031ac797b1fb87",
        "name": "demo2",
        "description": "Tenant for the openstack demo2"
    },
    {
        "id": "bdb8f50f82da4370813e6ea72548fd03",
        "name": "admin2",
        "description": "Tenant for the openstack admin2"
    }
]


"""Catalog id"""
CATALOG_ID = "100"
PROJECT_ID = "696111a61ec94c3188a90c017de1ebb9"

"""Catalog data detail
CATALOG_PRICE_LIST[0]:catalog_id:100
CATALOG_PRICE_LIST[1]:catalog_id:200
CATALOG_PRICE_LIST[2]:catalog_id:300
CATALOG_PRICE_LIST[3]:catalog_id:400
CATALOG_PRICE_LIST[4]:catalog_id:500
"""
CATALOG_PRICE_LIST = [
    {
        "catalog_id": "100",
        "catalog_name": "CPU 10 pieces S set",
        "public_seq_no": "1",
        "public_price": 1000000,
        "private_seq_no": "101",
        "private_price": 1000001,
        "project_id": "696111a61ec94c3188a90c017de1ebb9"
    },
    {
        "catalog_id": "200",
        "catalog_name": "CPU 10 pieces S set",
        "public_seq_no": "2",
        "public_price": 2000000,
        "private_seq_no": "102",
        "private_price": 1000002,
        "project_id": "696111a61ec94c3188a90c017de1ebb9"
    },
    {
        "catalog_id": "300",
        "catalog_name": "CPU 10 pieces S set",
        "public_seq_no": "3",
        "public_price": 3000000,
        "private_seq_no": "103",
        "private_price": 1000003,
        "project_id": "696111a61ec94c3188a90c017de1ebb9"
    },
    {
        "catalog_id": "400",
        "catalog_name": "CPU 10 pieces S set",
        "public_seq_no": "4",
        "public_price": 4000000,
        "private_seq_no": "104",
        "private_price": 1000004,
        "project_id": "696111a61ec94c3188a90c017de1ebb9"
    },
    {
        "catalog_id": "500",
        "catalog_name": "CPU 10 pieces S set",
        "public_seq_no": "5",
        "public_price": 5000000,
        "private_seq_no": "105",
        "private_price": 1000005,
        "project_id": "696111a61ec94c3188a90c017de1ebb9"
    }
]
