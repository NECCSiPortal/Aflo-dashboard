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

import copy

from mox3.mox import IsA  # noqa

from django.core.urlresolvers import reverse
from django import http

from openstack_dashboard.test import helpers as test

from afloclient.v1.tickets import Ticket
from afloclient.v1.tickettemplates import Tickettemplate

from nec_portal import api
from nec_portal.dashboards.project.ticket_list import panel  # noqa
from nec_portal.dashboards.project.ticket_templates \
    import fixture_20160627 as fixture
from nec_portal.dashboards.project.ticket_templates import panel  # noqa
from nec_portal.test import aflo_helpers as aflo_test


class WorkflowEngineTicketDetailTest(aflo_test.BaseAdminViewTests):
    """Workflow engine ticket detail view test class"""

    @test.create_stubs({api.ticket: ('ticket_get_detailed',
                                     'tickettemplates_get',)})
    def test_view_filled_data(self):
        """Test 'Ticket detail view display' to successfully run
        In the filled data
        """

        ticket_detail_data = self._get_ticket_detail_data(0)

        template_data = self._get_ticket_template_data(0)

        self._ticket_create_successfully_action(
            ticket_detail_data, template_data)

    def _get_ticket_detail_data(self, index):
        return copy.deepcopy(fixture.TICKET_DATA_LIST[index])

    def _get_ticket_template_data(self, index):
        return copy.deepcopy(fixture.TICKET_TEMPLATE_DATA_LIST[index])

    def _ticket_create_successfully_action(self, ticket_detail_data,
                                           template_data):

        ticket_detail_id = ticket_detail_data['id']

        api.ticket.ticket_get_detailed(
            IsA(http.HttpRequest), ticket_detail_id).AndReturn(
                Ticket(self, ticket_detail_data, loaded=True))

        template_id = template_data['id']

        api.ticket.tickettemplates_get(
            IsA(http.HttpRequest), template_id).AndReturn(
                Tickettemplate(self, template_data, loaded=True))

        self.mox.ReplayAll()

        url = reverse(
            'horizon:project:ticket_list:wf_engine_detail:index',
            args=[ticket_detail_id])

        res = self.client.get(url)

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, 'project/ticket_templates/wf_engine/detail/detail.html')
