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
from mock import MagicMock
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
from afloclient.v1.tickets import Ticket
from afloclient.v1.tickettemplates import Tickettemplate

from nec_portal import api
from nec_portal.dashboards.project.ticket_list import fixture
from nec_portal.dashboards.project.ticket_list import tables
from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils
from nec_portal.dashboards.project.ticket_list import views
from nec_portal.test import aflo_helpers as aflo_test


class TicketListViewTest(aflo_test.BaseAdminViewTests):
    """Ticket list view test class"""
    aflo_exception = test_exceptions.create_stubbed_exception(
        aflo_exceptions.ClientException)

    @test.create_stubs({api.ticket: ('ticket_list_detailed',
                                     'tickettemplates_get',)})
    @test.create_stubs({views.IndexView: ('_get_project_id',)})
    def test_ticket_list_index(self):
        """Test 'index' if the retrieved result is of 1"""
        # Create a filter condition.
        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filters = {'tenant_id': project_id}

        # Create a ticket of return data.(awaiting approval)
        ticket_data = \
            [Ticket(self, fixture.CONTRACT_TICKET_DATA_LIST[0], loaded=True)]

        # Search for tickets.
        api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc').AndReturn(
                [ticket_data, False, False])
        _get_ticket_templates(self, ticket_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse("horizon:project:ticket_list:index"))

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/ticket_list/index.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('ticket_list_detailed',)})
    @test.create_stubs({views.IndexView: ('_get_project_id',)})
    def test_tickets_list_no_data(self):
        """Test 'index' if the retrieved result is of 0"""
        # Create a filter condition.
        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filters = {'tenant_id': project_id}

        # Search for tickets.
        api.ticket. \
            ticket_list_detailed(
                IsA(http.HttpRequest),
                marker=None,
                paginate=True,
                filters=filters,
                sort_dir='desc').AndReturn(
                    [[], False, False])
        self.mox.ReplayAll()
        res = self.client.get(reverse("horizon:project:ticket_list:index"))

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/ticket_list/index.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('ticket_list_detailed',
                                     'tickettemplates_get',)})
    @test.create_stubs({views.IndexView: ('_get_project_id',)})
    def test_ticket_list_multi_role_data(self):
        """Test 'index' if the retrieved result is multi role data"""
        # Create a filter condition.
        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filters = {'tenant_id': project_id}

        ticket_data = copy.deepcopy(fixture.CONTRACT_TICKET_DATA_LIST[0])

        for workflow in ticket_data['workflow']:
            for next_status in workflow['status_detail']['next_status']:
                if 'grant_role' in next_status:
                    next_status['grant_role'] = [
                        next_status['grant_role'],
                        'test'
                    ]

        # Create a ticket of return data.(awaiting approval)
        ticket_data = [Ticket(self, ticket_data, loaded=True)]

        # Search for tickets.
        api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc').AndReturn([ticket_data, False, False])
        _get_ticket_templates(self, ticket_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse("horizon:project:ticket_list:index"))

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/ticket_list/index.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('ticket_list_detailed',),
                        exceptions: ('handle',)})
    def test_tickets_list_exception(self):
        """Test 'index' if the server raise exception"""
        # Create a filter condition.
        filters = {}

        # Search for tickets.
        api.ticket. \
            ticket_list_detailed(
                IsA(http.HttpRequest),
                marker=None,
                paginate=True,
                filters=filters,
                sort_dir='desc').AndRaise(self.aflo_exception)
        exceptions.handle(IsA(http.HttpRequest),
                          "Unable to retrieve requests information.")

        self.mox.ReplayAll()
        res = self.client.get(reverse("horizon:project:ticket_list:index"))

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/ticket_list/index.html')
        self.assertEqual(res.status_code, 200)


class TicketListViewPaginationTest(aflo_test.BaseAdminViewTests):
    """Ticket list view pagination test class"""

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('ticket_list_detailed',
                                     'tickettemplates_get',)})
    @test.create_stubs({views.IndexView: ('_get_project_id',)})
    def test_tickets_list_get_pagination(self):
        """Test 'Move next page'
        1 page have 2 row of ticket.
        """
        # Create a filter condition.
        filters = {'tenant_id': fixture.PROJECT_GET_DATA.get('id')}

        # Create ticket data list.
        ticket_data_list = []
        for data in fixture.CONTRACT_TICKET_DATA_LIST:
            ticket_data_list.append(
                Ticket(self, data, loaded=True))

        # Get 5 row from fixture data
        tickets = ticket_data_list[:5]

        # Create number 1 page data.
        views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc').AndReturn(
                [tickets[:2], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_1 = rtn_ticket[0]

        # Create number 2 page data.
        views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[1].id,
            paginate=True,
            filters=filters,
            sort_dir='desc').AndReturn(
                [tickets[2:4], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_2 = rtn_ticket[0]

        # Create number 3 page data.
        views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[3].id,
            paginate=True,
            filters=filters,
            sort_dir='desc').AndReturn(
                [tickets[4:], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_3 = rtn_ticket[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:project:ticket_list:index")

        # Show number 1 page.(items 1-2)
        self.client.get(index_url)
        self.assertEqual(len(rtn_ticket_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 2-4)
        params = "=".join([tables.TicketTable._meta.pagination_param,
                           tickets[1].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_2),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 3 page.(items 5)
        params = "=".join([tables.TicketTable._meta.pagination_param,
                           tickets[3].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_3), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('ticket_list_detailed',
                                     'tickettemplates_get',)})
    @test.create_stubs({views.IndexView: ('_get_project_id',)})
    def test_tickets_list_get_prev_pagination(self):
        """Test 'Move previous page'
        1 page have 2 row of ticket.
        """
        # Create a filter condition.
        filters = {'tenant_id': fixture.PROJECT_GET_DATA.get('id')}

        # Create ticket data list.
        ticket_data_list = []
        for data in fixture.CONTRACT_TICKET_DATA_LIST:
            ticket_data_list.append(
                Ticket(self, data, loaded=True))

        # Get 5 row from fixture data.
        tickets = ticket_data_list[:3]

        # Create number 1 page data.
        views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc').AndReturn(
                [tickets[:2], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_1 = rtn_ticket[0]

        # Create number 2 page data.
        views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[1].id,
            paginate=True,
            filters=filters,
            sort_dir='desc').AndReturn(
                [tickets[2:], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_2 = rtn_ticket[0]

        # Create back page(number1) data.
        views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[2].id,
            paginate=True,
            filters=filters,
            sort_dir='asc').AndReturn(
                [tickets[:2], True, True])
        _get_ticket_templates(self, [tickets[1]])
        _get_ticket_templates(self, [tickets[0]])
        rtn_ticket_3 = rtn_ticket[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:project:ticket_list:index")

        # Show number 1 page.(items 1-2)
        self.client.get(index_url)
        self.assertEqual(len(rtn_ticket_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 3)
        params = "=".join([tables.TicketTable._meta.pagination_param,
                           tickets[1].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_2), 1)

        # Move to back page(number1) data.
        params = "=".join([tables.TicketTable._meta.prev_pagination_param,
                           tickets[2].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_3),
                         settings.API_RESULT_PAGE_SIZE)


class TicketListViewFilterTest(aflo_test.BaseAdminViewTests):
    """Ticket list view filter test class"""

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_category(self):
        """Test 'get_filter[Category] of index'"""
        view = views.IndexView()
        view.request = MagicMock()
        view.request.encoding = 'utf-8'

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "ticket_type",
            "filter_string": "contract",
            "result": {'tenant_id': project_id,
                       "ticket_type": "contract"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_category_multi_byte(self):
        """Test 'get_filter[Category] of index'"""
        view = views.IndexView()
        view.request = MagicMock()
        view.request.encoding = 'utf-8'

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "ticket_type",
            "filter_string": views.TICKET_TYPE['New Contract'],
            "result": {'tenant_id': project_id,
                       "ticket_type": 'New Contract'}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_type(self):
        """Test 'get_filter[Type] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "ticket_template_name",
            "filter_string": "ticket_template_name_string",
            "result": {'tenant_id': project_id,
                       "ticket_template_name":
                       "ticket_template_name_string"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_id(self):
        """Test 'get_filter[ID] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "ticket_id",
            "filter_string": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
            "result": {'tenant_id': project_id,
                       "ticket_id":
                            "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_request_form(self):
        """Test 'get_filter[Request Form] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "application_kinds_name",
            "filter_string": "application_kinds_name_value",
            "result": {'tenant_id': project_id,
                       "application_kinds_name":
                            "application_kinds_name_value"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_timezone',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_issue_date(self):
        """Test 'get_filter[Issue Date] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "owner_at",
            "filter_string": "2015-07-29",
            "result": {'tenant_id': project_id,
                       "owner_at_from":
                            "2015-07-28T15:00:00.000000",
                       "owner_at_to":
                            "2015-07-29T14:59:59.999999"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        views.IndexView._get_timezone(). \
            AndReturn('Asia/Tokyo')

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_timezone',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_issue_date_utc(self):
        """Test 'get_filter[Issue Date(UTC)] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "owner_at",
            "filter_string": "2015-07-29",
            "result": {'tenant_id': project_id,
                       "owner_at_from":
                            "2015-07-29T00:00:00.000000",
                       "owner_at_to":
                            "2015-07-29T23:59:59.999999"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        views.IndexView._get_timezone(). \
            AndReturn('UTC')

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_irregular_issue_date(self):
        """Test 'get_filter[Issue Date(irregular)] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "owner_at",
            "filter_string": "aaaaa",
            "result": {'tenant_id': project_id}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_issuer(self):
        """Test 'get_filter[Issuer] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "owner_name",
            "filter_string": "owner_name_value",
            "result": {'tenant_id': project_id,
                       "owner_name":
                            "owner_name_value"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_timezone',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_last_update(self):
        """Test 'get_filter[Last Update] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "last_confirmed_at",
            "filter_string": "2015-07-29",
            "result": {'tenant_id': project_id,
                       "last_confirmed_at_from":
                            "2015-07-28T15:00:00.000000",
                       "last_confirmed_at_to":
                            "2015-07-29T14:59:59.999999"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        views.IndexView._get_timezone(). \
            AndReturn('Asia/Tokyo')

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_timezone',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_last_update_utc(self):
        """Test 'get_filter[Last Update(UTC)] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "last_confirmed_at",
            "filter_string": "2015-07-29",
            "result": {'tenant_id': project_id,
                       "last_confirmed_at_from":
                            "2015-07-29T00:00:00.000000",
                       "last_confirmed_at_to":
                            "2015-07-29T23:59:59.999999"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        views.IndexView._get_timezone(). \
            AndReturn('UTC')

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_irregular_last_update(self):
        """Test 'get_filter[Last Update(irregular)] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "last_confirmed_at",
            "filter_string": "aaaaa",
            "result": {'tenant_id': project_id}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    def test_ticket_list_get_filter_updated_by(self):
        """Test 'get_filter[Updated By] of index'"""
        view = views.IndexView()

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "last_confirmer_name",
            "filter_string": "last_confirmer_name_value",
            "result": {'tenant_id': project_id,
                       "last_confirmer_name":
                            "last_confirmer_name_value"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',
                                          '_get_project_id',)})
    @test.create_stubs({api.ticket: ('ticket_list_detailed',)})
    @test.create_stubs({ticket_utils: ('get_language_name',)})
    def test_ticket_list_get_filter_status(self):
        """Test 'get_filter[Status] of index'"""
        view = views.IndexView()
        view.request = None

        project_id = views.IndexView._get_project_id().AndReturn(
            fixture.PROJECT_GET_DATA.get('id'))
        filter_option = {
            "filter_field": "last_status_code",
            "filter_string": "Awaiting Approval",
            "result": {'tenant_id': project_id,
                       "last_status_code":
                            "awaiting approval"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        # Create a ticket of return data.(awaiting approval)
        ticket_data = \
            [Ticket(self, fixture.CONTRACT_TICKET_DATA_LIST[0], loaded=True)]

        # Search for tickets.
        api.ticket.ticket_list_detailed(
            None,
            marker=None).AndReturn([ticket_data, False, False])

        # Get Status name.
        language_name = ticket_data[0].last_workflow. \
            get("status_detail"). \
            get("status_name")
        ticket_utils.get_language_name(
            None,
            language_name).AndReturn('Awaiting Approval')

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)


def _get_ticket_templates(self, ticket_data_list):

    quota_registration = fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST[0]
    quota_cancel = fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST[1]

    # Search for tickettemplate.
    for ticket in ticket_data_list:
        if ticket.ticket_template_id == quota_registration.get('id'):
            ticket_template_data = \
                Tickettemplate(self, quota_registration, loaded=True)

            api.ticket.tickettemplates_get(
                IsA(http.HttpRequest),
                ticket.ticket_template_id).AndReturn(ticket_template_data)

        elif ticket.ticket_template_id == quota_cancel.get('id'):
            ticket_template_data = \
                Tickettemplate(self, quota_cancel, loaded=True)

            api.ticket.tickettemplates_get(
                IsA(http.HttpRequest),
                ticket.ticket_template_id).AndReturn(ticket_template_data)
