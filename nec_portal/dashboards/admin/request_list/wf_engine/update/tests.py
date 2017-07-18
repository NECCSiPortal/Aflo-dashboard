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

import copy

from mox3.mox import IsA

from django.core.urlresolvers import reverse
from django import http

from openstack_dashboard.test import helpers as test

from afloclient.v1.catalogs import Catalog
from afloclient.v1.price import Price
from afloclient.v1.tickets import Ticket
from afloclient.v1.tickettemplates import Tickettemplate

from nec_portal import api
from nec_portal.dashboards.project.ticket_templates import \
    fixture_20160627 as fixture
from nec_portal.dashboards.project.ticket_templates import panel  # noqa
from nec_portal.test import aflo_helpers as aflo_test


class WorkflowEngineTicketUpdateTest(aflo_test.BaseAdminViewTests):
    """Workflow engine ticket update test class"""

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_view(self):
        """Test 'Display the update screen' to successfully run"""

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']
        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        api.ticket.tickettemplates_get(
            IsA(http.HttpRequest),
            ticket_template_id).AndReturn(
                Tickettemplate(self, template_data, loaded=True))

        api.ticket.ticket_get_detailed(
            IsA(http.HttpRequest), ticket_detail_id).AndReturn(
                Ticket(self, ticket_detail_data, loaded=True))

        self._search_catalog_price_list(
            template_data['template_contents']['target_id'], True)

        self.mox.ReplayAll()

        url = reverse(
            'horizon:admin:request_list:wf_engine_update:index',
            args=[ticket_detail_id])

        res = self.client.get(url)

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, 'project/ticket_templates/wf_engine/update/update.html')

    def _get_ticket_template_data(self, index):
        return copy.deepcopy(fixture.TICKET_TEMPLATE_DATA_LIST[index])

    def _get_ticket_detail_data(self, index):
        return copy.deepcopy(fixture.TICKET_DATA_LIST[index])

    def _search_catalog_price_list(self, target_ids, price_exists_flag):
        count = 0
        for target_id in target_ids:
            catalog_data = Catalog(
                self, copy.deepcopy(fixture.CATALOG_DATA_LIST[count]),
                loaded=True)

            api.ticket.catalog_get_detailed(
                IsA(http.HttpRequest), target_id).AndReturn(catalog_data)

            if price_exists_flag:
                catalog_price_data = [Price(
                    self, copy.deepcopy(
                        fixture.CATALOG_PRICE_DATA_LIST[count]),
                    loaded=True)]
            else:
                catalog_price_data = []

            api.ticket.price_list_detailed2(
                IsA(http.HttpRequest), target_id).AndReturn(catalog_price_data)
            count = count + 1
