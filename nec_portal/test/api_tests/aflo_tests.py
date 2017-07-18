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

import afloclient
from afloclient.v1.tickets import Ticket
from afloclient.v1.tickettemplates import Tickettemplate

from django.conf import settings
from django.test.utils import override_settings

from nec_portal import api
from nec_portal.api import ticket  # noqa
from nec_portal.dashboards.project.ticket_list import \
    fixture as ticket_list_fixture
from nec_portal.dashboards.project.ticket_templates import \
    fixture as tickettemplate_fixture
from openstack_dashboard.test import helpers as test


class AfloApiTests(test.APITestCase):

    def setUp(self):
        super(AfloApiTests, self).setUp()

        # Store the original clients
        self._original_afloclient = api.ticket.afloclient

        # Replace the clients with our stubs.
        api.ticket.afloclient = lambda request: self.stub_afloclient()

    def tearDown(self):
        super(AfloApiTests, self).tearDown()

        api.ticket.afloclient = self._original_afloclient

    def stub_afloclient(self):
        if not hasattr(self, "afloclient"):
            self.mox.StubOutWithMock(afloclient, 'Client')
            self.afloclient = self.mox.CreateMock(afloclient.Client)
        return self.afloclient

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_ticket_list_detailed_no_pagination(self):
        """"Verify that all tickets
        are returned even with a small page size.
        """
        api_tickets = []
        for data in ticket_list_fixture.CONTRACT_TICKET_DATA_LIST:
            api_tickets.append(
                Ticket(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'created_at', }

        afloclient = self.stub_afloclient()
        afloclient.tickets = self.mox.CreateMockAnything()
        afloclient.tickets.list(kwargs) \
            .AndReturn(iter(api_tickets))
        self.mox.ReplayAll()

        tickets, has_more, has_prev = api.ticket.ticket_list_detailed(
            self.request)
        self.assertItemsEqual(tickets, api_tickets)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_ticket_list_detailed_sort_options(self):
        """"Verify that sort_dir and sort_key work"""
        api_tickets = []
        for data in ticket_list_fixture.CONTRACT_TICKET_DATA_LIST:
            api_tickets.append(
                Ticket(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        sort_dir = 'asc'
        sort_key = 'updated_at'

        kwargs = {'limit': limit,
                  'sort_dir': sort_dir,
                  'sort_key': sort_key, }

        afloclient = self.stub_afloclient()
        afloclient.tickets = self.mox.CreateMockAnything()
        afloclient.tickets.list(kwargs) \
            .AndReturn(iter(api_tickets))
        self.mox.ReplayAll()

        tickets, has_more, has_prev = api.ticket.ticket_list_detailed(
            self.request,
            sort_dir=sort_dir,
            sort_key=sort_key)
        self.assertItemsEqual(tickets, api_tickets)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_ticket_list_detailed_pagination_more_page_size(self):
        """"The total snapshot count is over page size, should return
        page_size tickets.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_tickets = []
        for data in ticket_list_fixture.CONTRACT_TICKET_DATA_LIST:
            api_tickets.append(
                Ticket(self, data, loaded=True))
        tickets_iter = iter(api_tickets)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'created_at', }

        afloclient = self.stub_afloclient()
        afloclient.tickets = self.mox.CreateMockAnything()
        # Pass back all tickets, ignoring filters
        afloclient.tickets.list(kwargs).AndReturn(tickets_iter)
        self.mox.ReplayAll()

        tickets, has_more, has_prev = api.ticket.ticket_list_detailed(
            self.request,
            marker=None,
            filters=None,
            paginate=True)
        expected_tickets = api_tickets[:page_size]
        self.assertItemsEqual(tickets, expected_tickets)
        self.assertTrue(has_more)
        self.assertFalse(has_prev)
        # Ensure that only the needed number of tickets are consumed
        # from the iterator (page_size + 1).
        self.assertEqual(len(list(tickets_iter)),
                         len(api_tickets) - len(expected_tickets) - 1)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_ticket_list_detailed_pagination_less_page_size(self):
        """"The total ticket count is less than page size,
        should return tickets more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_tickets = []
        for data in ticket_list_fixture.CONTRACT_TICKET_DATA_LIST:
            api_tickets.append(
                Ticket(self, data, loaded=True))
        tickets_iter = iter(api_tickets)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'created_at', }

        afloclient = self.stub_afloclient()
        afloclient.tickets = self.mox.CreateMockAnything()
        # Pass back all tickets, ignoring filters
        afloclient.tickets.list(kwargs).AndReturn(tickets_iter)
        self.mox.ReplayAll()

        tickets, has_more, has_prev = api.ticket.ticket_list_detailed(
            self.request,
            filters=None,
            paginate=True)
        expected_tickets = api_tickets[:page_size]
        self.assertItemsEqual(tickets, expected_tickets)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=6)
    def test_ticket_list_detailed_pagination_equal_page_size(self):
        """"The total ticket count equals page size, should return
        page_size tickets. more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_tickets = []
        for data in ticket_list_fixture.CONTRACT_TICKET_DATA_LIST:
            api_tickets.append(
                Ticket(self, data, loaded=True))
        tickets_iter = iter(api_tickets)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'created_at', }

        afloclient = self.stub_afloclient()
        afloclient.tickets = self.mox.CreateMockAnything()
        afloclient.tickets.list(kwargs).AndReturn(tickets_iter)
        self.mox.ReplayAll()

        tickets, has_more, has_prev = api.ticket.ticket_list_detailed(
            self.request,
            filters=None,
            paginate=True)
        expected_tickets = api_tickets[:page_size]
        self.assertItemsEqual(tickets, expected_tickets)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)
        self.assertEqual(len(expected_tickets), len(tickets))

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_ticket_list_detailed_pagination_marker(self):
        """"Tests getting a second page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = 'b0536e64-e20f-4280-88bf-deafaae8d3d0'

        api_tickets = []
        for data in ticket_list_fixture.CONTRACT_TICKET_DATA_LIST:
            api_tickets.append(
                Ticket(self, data, loaded=True))
        tickets_iter = iter(api_tickets[page_size:])

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'created_at', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.tickets = self.mox.CreateMockAnything()
        # Pass back all tickets, ignoring filters
        afloclient.tickets.list(kwargs) \
            .AndReturn(tickets_iter)
        self.mox.ReplayAll()

        tickets, has_more, has_prev = api.ticket.ticket_list_detailed(
            self.request,
            marker=marker,
            filters=None,
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_ticket_list_detailed_pagination_marker_prev(self):
        """"Tests getting previous page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = 'b0536e64-e20f-4280-88bf-deafaae8d3d0'

        api_tickets = []
        for data in ticket_list_fixture.CONTRACT_TICKET_DATA_LIST:
            api_tickets.append(
                Ticket(self, data, loaded=True))
        tickets_iter = iter(api_tickets[page_size:])

        kwargs = {'limit': limit,
                  'sort_dir': 'asc',
                  'sort_key': 'created_at', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.tickets = self.mox.CreateMockAnything()
        # Pass back all tickets, ignoring filters
        afloclient.tickets.list(kwargs) \
            .AndReturn(tickets_iter)
        self.mox.ReplayAll()

        tickets, has_more, has_prev = api.ticket.ticket_list_detailed(
            self.request,
            marker=marker,
            filters=None,
            sort_dir='asc',
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_tickettemplate_list_detailed_no_pagination(self):
        """"Verify that all tickettemplates
        are returned even with a small page size.
        """
        api_tickettemplates = []
        for data in tickettemplate_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            api_tickettemplates.append(
                Tickettemplate(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'enable_expansion_filters': False,
                  'sort_dir': ['desc'],
                  'sort_key': ['id'], }

        afloclient = self.stub_afloclient()
        afloclient.tickettemplates = self.mox.CreateMockAnything()
        afloclient.tickettemplates.list(kwargs) \
            .AndReturn(iter(api_tickettemplates))
        self.mox.ReplayAll()

        tickettemplates, has_more, has_prev = \
            api.ticket.tickettemplates_list_detailed(self.request)
        self.assertItemsEqual(tickettemplates, api_tickettemplates)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_tickettemplate_list_detailed_sort_options(self):
        """"Verify that sort_dir and sort_key work"""
        api_tickettemplates = []
        for data in tickettemplate_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            api_tickettemplates.append(
                Tickettemplate(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        sort_dir = ['asc']
        sort_key = ['updated_at']

        kwargs = {'limit': limit,
                  'enable_expansion_filters': False,
                  'sort_dir': sort_dir,
                  'sort_key': sort_key, }

        afloclient = self.stub_afloclient()
        afloclient.tickettemplates = self.mox.CreateMockAnything()
        afloclient.tickettemplates.list(kwargs) \
            .AndReturn(iter(api_tickettemplates))
        self.mox.ReplayAll()

        tickettemplates, has_more, has_prev = \
            api.ticket.tickettemplates_list_detailed(
                self.request,
                sort_dir=sort_dir,
                sort_key=sort_key)
        self.assertItemsEqual(tickettemplates, api_tickettemplates)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_tickettemplate_list_detailed_pagination_more_page_size(self):
        """"The total snapshot count is over page size, should return
        page_size tickettemplates.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_tickettemplates = []
        for data in tickettemplate_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            api_tickettemplates.append(
                Tickettemplate(self, data, loaded=True))
        tickettemplates_iter = iter(api_tickettemplates)

        kwargs = {'limit': limit,
                  'enable_expansion_filters': False,
                  'sort_dir': ['desc'],
                  'sort_key': ['id'], }

        afloclient = self.stub_afloclient()
        afloclient.tickettemplates = self.mox.CreateMockAnything()
        # Pass back all tickettemplates, ignoring filters
        afloclient.tickettemplates.list(kwargs) \
            .AndReturn(tickettemplates_iter)
        self.mox.ReplayAll()

        tickettemplates, has_more, has_prev = \
            api.ticket.tickettemplates_list_detailed(
                self.request,
                marker=None,
                filters=None,
                paginate=True)
        expected_tickettemplates = api_tickettemplates[:page_size]
        self.assertItemsEqual(tickettemplates, expected_tickettemplates)
        self.assertTrue(has_more)
        self.assertFalse(has_prev)
        # Ensure that only the needed number of tickettemplates are consumed
        # from the iterator (page_size + 1).
        self.assertEqual(
            len(list(tickettemplates_iter)),
            len(api_tickettemplates) - len(expected_tickettemplates) - 1)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_tickettemplate_list_detailed_pagination_less_page_size(self):
        """The total tickettemplate count is less than page size,
        should return tickettemplates more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_tickettemplates = []
        for data in tickettemplate_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            api_tickettemplates.append(
                Tickettemplate(self, data, loaded=True))
        tickettemplates_iter = iter(api_tickettemplates)

        kwargs = {'limit': limit,
                  'enable_expansion_filters': False,
                  'sort_dir': ['desc'],
                  'sort_key': ['id'], }

        afloclient = self.stub_afloclient()
        afloclient.tickettemplates = self.mox.CreateMockAnything()
        # Pass back all tickettemplates, ignoring filters
        afloclient.tickettemplates.list(kwargs) \
            .AndReturn(tickettemplates_iter)
        self.mox.ReplayAll()

        tickettemplates, has_more, has_prev = \
            api.ticket.tickettemplates_list_detailed(
                self.request,
                filters=None,
                paginate=True)
        expected_tickettemplates = api_tickettemplates[:page_size]
        self.assertItemsEqual(tickettemplates, expected_tickettemplates)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=6)
    def test_tickettemplate_list_detailed_pagination_equal_page_size(self):
        """"The total tickettemplate count equals page size, should return
        page_size tickettemplates. more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_tickettemplates = []
        for data in tickettemplate_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            api_tickettemplates.append(
                Tickettemplate(self, data, loaded=True))
        tickettemplates_iter = iter(api_tickettemplates)

        kwargs = {'limit': limit,
                  'enable_expansion_filters': False,
                  'sort_dir': ['desc'],
                  'sort_key': ['id'], }

        afloclient = self.stub_afloclient()
        afloclient.tickettemplates = self.mox.CreateMockAnything()
        afloclient.tickettemplates.list(kwargs) \
            .AndReturn(tickettemplates_iter)
        self.mox.ReplayAll()

        tickettemplates, has_more, has_prev = \
            api.ticket.tickettemplates_list_detailed(
                self.request,
                filters=None,
                paginate=True)
        expected_tickettemplates = api_tickettemplates[:page_size]
        self.assertItemsEqual(tickettemplates, expected_tickettemplates)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)
        self.assertEqual(len(expected_tickettemplates), len(tickettemplates))

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_tickettemplate_list_detailed_pagination_marker(self):
        """"Tests getting a second page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = '2'

        api_tickettemplates = []
        for data in tickettemplate_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            api_tickettemplates.append(
                Tickettemplate(self, data, loaded=True))
        tickettemplates_iter = iter(api_tickettemplates[page_size:])

        kwargs = {'limit': limit,
                  'enable_expansion_filters': False,
                  'sort_dir': ['desc'],
                  'sort_key': ['id'], }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.tickettemplates = self.mox.CreateMockAnything()
        # Pass back all tickettemplates, ignoring filters
        afloclient.tickettemplates.list(kwargs) \
            .AndReturn(tickettemplates_iter)
        self.mox.ReplayAll()

        tickettemplates, has_more, has_prev = \
            api.ticket.tickettemplates_list_detailed(
                self.request,
                marker=marker,
                filters=None,
                paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_tickettemplate_list_detailed_pagination_marker_prev(self):
        """Tests getting previous page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = '2'

        api_tickettemplates = []
        for data in tickettemplate_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST:
            api_tickettemplates.append(
                Tickettemplate(self, data, loaded=True))
        tickettemplates_iter = iter(api_tickettemplates[page_size:])

        kwargs = {'limit': limit,
                  'enable_expansion_filters': False,
                  'sort_dir': 'asc',
                  'sort_key': ['id'], }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.tickettemplates = self.mox.CreateMockAnything()
        # Pass back all tickettemplates, ignoring filters
        afloclient.tickettemplates.list(kwargs) \
            .AndReturn(tickettemplates_iter)
        self.mox.ReplayAll()

        tickettemplates, has_more, has_prev = \
            api.ticket.tickettemplates_list_detailed(
                self.request,
                marker=marker,
                filters=None,
                sort_dir='asc',
                paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)
