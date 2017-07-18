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

from mox3.mox import IsA  # noqa

from django.conf import settings
from django.core.urlresolvers import reverse
from django import http
from django.test.utils import override_settings

from openstack_dashboard.test import helpers as test
from openstack_dashboard.test.test_data import \
    exceptions as test_exceptions

from horizon import exceptions

import afloclient.exc as aflo_exceptions
from afloclient.v1.tickettemplates import Tickettemplate

from nec_portal import api
from nec_portal.dashboards.project.ticket_templates.application_kinds \
    import tables as tables
from nec_portal.dashboards.project.ticket_templates \
    import fixture
from nec_portal.test import aflo_helpers as aflo_test


class TicketTemplatesContractTest(aflo_test.BaseAdminViewTests):
    """Ticket contract template list view test class"""
    aflo_exception = test_exceptions.create_stubbed_exception(
        aflo_exceptions.ClientException)

    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_index(self):
        """Test contract 'index' Test if the retrieved result is of 1"""

        # Create a tickettemplate of return data.
        ticket_template_data = \
            [Tickettemplate(self,
                            fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST[0],
                            loaded=True)]

        # Search for tickettemplates.
        api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([ticket_template_data,
                                                      False,
                                                      False])
        self.mox.ReplayAll()

        res = self.client.get(
            reverse("horizon:project:ticket_templates:index"))

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_index_no_data(self):
        """Test contract 'index' if the retrieved result is of 0"""

        # Search for tickettemplates.
        api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([[], False, False])
        self.mox.ReplayAll()

        res = self.client.post(
            reverse("horizon:project:ticket_templates:index"))

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',),
                        exceptions: ('handle',)})
    def test_ticket_index_exception(self):
        """Test contract 'index' if the server raise exception"""

        # Search for tickettemplates.
        api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndRaise(self.aflo_exception)
        exceptions.handle(IsA(http.HttpRequest),
                          "Unable to retrieve services information.")

        self.mox.ReplayAll()

        res = self.client.post(
            reverse("horizon:project:ticket_templates:index"))

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)


class TicketTemplatesContractPaginationTest(aflo_test.BaseAdminViewTests):
    """Ticket contract template list view pagination test class"""

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_get_pagination(self):
        """Test 'Move next page'
        1 page have 2 row of ticket template.
        """

        # Create tickettemplate data list.
        tickettemplate_data_list = []
        for data in fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            tickettemplate_data_list.append(
                Tickettemplate(self, data, loaded=True))

        # Get 5 row from fixture data.
        tickettemplates = tickettemplate_data_list[:5]

        # Create number 1 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([tickettemplates[:2],
                                                      True,
                                                      True])
        rtn_tickettemplate_1 = rtn_tickettemplate[0]

        # Create number 2 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=tickettemplates[1].id,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([tickettemplates[2:4],
                                                      True,
                                                      True])
        rtn_tickettemplate_2 = rtn_tickettemplate[0]

        # Create number 3 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=tickettemplates[3].id,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([tickettemplates[4:],
                                                      True,
                                                      True])
        rtn_tickettemplate_3 = rtn_tickettemplate[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:project:ticket_templates:index")

        # Show number 1 page.(items 1-2)
        self.client.get(index_url)
        self.assertEqual(len(rtn_tickettemplate_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 2-4)
        tickettemplate_table = tables.TicketTemplatesListContractTable
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[1].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_2),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 3 page.(items 5)
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[3].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_3), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_get_prev_pagination(self):
        """Test contract 'Move previous page'
        1 page have 2 row of ticket.
        """

        # Create tickettemplate data list.
        tickettemplate_data_list = []
        for data in fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            tickettemplate_data_list.append(
                Tickettemplate(self, data, loaded=True))

        # Get 3 row from fixture data.
        tickettemplates = tickettemplate_data_list[:3]

        # Create number 1 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([tickettemplates[:2],
                                                      True,
                                                      False])
        rtn_tickettemplate_1 = rtn_tickettemplate[0]

        # Create number 2 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=tickettemplates[1].id,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([tickettemplates[2:],
                                                      True,
                                                      True])
        rtn_tickettemplate_2 = rtn_tickettemplate[0]

        # Create back page(number1) data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="New Contract",
            marker=tickettemplates[2].id,
            paginate=True,
            filters=None,
            sort_dir=['desc'],
            enable_expansion_filters=True).AndReturn([tickettemplates[:2],
                                                      True,
                                                      True])
        rtn_tickettemplate_3 = rtn_tickettemplate[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:project:ticket_templates:index")

        # Show number 1 page.(items 1-2)
        self.client.get(index_url)
        self.assertEqual(len(rtn_tickettemplate_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 3)
        tickettemplate_table = tables.TicketTemplatesListContractTable
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[1].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_2), 1)

        # Move to back page(number1) data.
        tickettemplate_table = tables.TicketTemplatesListContractTable
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[2].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_3),
                         settings.API_RESULT_PAGE_SIZE)


class TicketTemplatesWorkTest(aflo_test.BaseAdminViewTests):
    """Ticket work template list view test class"""
    aflo_exception = test_exceptions.create_stubbed_exception(
        aflo_exceptions.ClientException)

    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_index(self):
        """Test work 'index' Test if the retrieved result is of 1"""

        # Create a tickettemplate of return data.
        ticket_template_data = \
            [Tickettemplate(self,
                            fixture.REQUEST_TICKET_TEMPLATE_DATA_LIST[0],
                            loaded=True)]

        # Search for tickettemplates.
        api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([ticket_template_data, False, False])
        self.mox.ReplayAll()

        res = self.client.get(
            reverse("horizon:project:ticket_templates:index") +
            '?tab=ticket_templates_group_tabs__request_tab')

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_index_no_data(self):
        """Test work 'index' if the retrieved result is of 0"""

        # Search for tickettemplates.
        api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([[], False, False])
        self.mox.ReplayAll()

        res = self.client.post(
            reverse("horizon:project:ticket_templates:index") +
            '?tab=ticket_templates_group_tabs__request_tab')

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',),
                        exceptions: ('handle',)})
    def test_ticket_index_exception(self):
        """Test work 'index' if the server raise exception"""

        # Search for tickettemplates.
        api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndRaise(self.aflo_exception)
        exceptions.handle(IsA(http.HttpRequest),
                          "Unable to retrieve services information.")

        self.mox.ReplayAll()

        res = self.client.get(
            reverse("horizon:project:ticket_templates:index") +
            '?tab=ticket_templates_group_tabs__request_tab')

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)


class TicketTemplatesWorkPaginationTest(aflo_test.BaseAdminViewTests):
    """Ticket work template list view pagination test class"""

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_get_pagination(self):
        """Test work 'Move next page'
        1 page have 2 row of ticket template.
        """

        # Create tickettemplate data list.
        tickettemplate_data_list = []
        for data in fixture.REQUEST_TICKET_TEMPLATE_DATA_LIST:
            tickettemplate_data_list.append(
                Tickettemplate(self, data, loaded=True))

        # Get 5 row from fixture data.
        tickettemplates = tickettemplate_data_list[:5]

        # Create number 1 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([tickettemplates[:2], True, True])
        rtn_tickettemplate_1 = rtn_tickettemplate[0]

        # Create number 2 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=tickettemplates[1].id,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([tickettemplates[2:4], True, True])
        rtn_tickettemplate_2 = rtn_tickettemplate[0]

        # Create number 3 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=tickettemplates[3].id,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([tickettemplates[4:], True, True])
        rtn_tickettemplate_3 = rtn_tickettemplate[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:project:ticket_templates:index")
        index_url_selected_tab = 'tab=ticket_templates_group_tabs__request_tab'

        # Show number 1 page.(items 1-2)
        url = "?".join([index_url, index_url_selected_tab])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 2-4)
        tickettemplate_table = tables.TicketTemplatesListRequestTable
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[1].id])
        url = "?".join([index_url, index_url_selected_tab + "&" + params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_2),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 3 page.(items 5)
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[3].id])
        url = "?".join([index_url, index_url_selected_tab + "&" + params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_3), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('tickettemplates_list_detailed',)})
    def test_ticket_get_prev_pagination(self):
        """Test work 'Move previous page'
        1 page have 2 row of ticket.
        """

        # Create tickettemplate data list.
        tickettemplate_data_list = []
        for data in fixture.REQUEST_TICKET_TEMPLATE_DATA_LIST:
            tickettemplate_data_list.append(
                Tickettemplate(self, data, loaded=True))

        # Get 3 row from fixture data.
        tickettemplates = tickettemplate_data_list[:3]

        # Create number 1 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=None,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([tickettemplates[:2], True, False])
        rtn_tickettemplate_1 = rtn_tickettemplate[0]

        # Create number 2 page data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=tickettemplates[1].id,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([tickettemplates[2:], True, True])
        rtn_tickettemplate_2 = rtn_tickettemplate[0]

        # Create back page(number1) data.
        rtn_tickettemplate = api.ticket.tickettemplates_list_detailed(
            IsA(http.HttpRequest),
            ticket_type="Work",
            marker=tickettemplates[2].id,
            paginate=True,
            filters=None,
            sort_dir=['desc']).AndReturn([tickettemplates[:2], True, True])
        rtn_tickettemplate_3 = rtn_tickettemplate[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:project:ticket_templates:index")
        index_url_selected_tab = 'tab=ticket_templates_group_tabs__request_tab'

        # Show number 1 page.(items 1-2)
        url = "?".join([index_url, index_url_selected_tab])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 3)
        tickettemplate_table = tables.TicketTemplatesListRequestTable
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[1].id])
        url = "?".join([index_url, index_url_selected_tab + "&" + params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_2), 1)

        # Move to back page(number1) data.
        tickettemplate_table = tables.TicketTemplatesListRequestTable
        params = "=".join([tickettemplate_table._meta.pagination_param,
                           tickettemplates[2].id])
        url = "?".join([index_url, index_url_selected_tab + "&" + params])
        self.client.get(url)
        self.assertEqual(len(rtn_tickettemplate_3),
                         settings.API_RESULT_PAGE_SIZE)
