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

from mock import MagicMock
from mox3.mox import IsA  # noqa

from django.conf import settings
from django.core.urlresolvers import reverse
from django import http
from django.test.utils import override_settings

from openstack_dashboard.api import keystone
from openstack_dashboard.test import helpers as test
from openstack_dashboard.test.test_data import \
    exceptions as test_exceptions

from horizon import exceptions

from keystoneclient.v2_0.tenants import Tenant

import afloclient.exc as aflo_exceptions
from afloclient.v1.tickets import Ticket
from afloclient.v1.tickettemplates import Tickettemplate

from nec_portal import api
from nec_portal.dashboards.admin.request_list import fixture
from nec_portal.dashboards.admin.request_list import tables
from nec_portal.dashboards.admin.request_list import views
from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils
from nec_portal.test import aflo_helpers as aflo_test

TICKET_TYPE = 'Work'


class RequestListViewTest(aflo_test.BaseAdminViewTests):
    """Request list view test class"""
    aflo_exception = test_exceptions.create_stubbed_exception(
        aflo_exceptions.ClientException)

    @test.create_stubs({api.ticket: ('ticket_list_detailed',
                                     'tickettemplates_get',)})
    def test_request_list_index(self):
        """Test 'index' if the retrieved result is of 1"""
        # Create a filter condition.
        filters = {}

        # Create a ticket of return data.(awaiting approval)
        ticket_data = \
            [Ticket(self, fixture.REQUEST_TICKET_DATA_LIST[0], loaded=True)]

        # Search for tickets.
        api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc',
            ticket_type=TICKET_TYPE).AndReturn([ticket_data, False, False])
        _get_ticket_templates(self, ticket_data)

        self.mox.ReplayAll()
        res = self.client.get(reverse("horizon:admin:request_list:index"))

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/request_list/index.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({api.ticket: ('ticket_list_detailed',)})
    def test_tickets_list_no_data(self):
        """Test 'index' if the retrieved result is of 0"""
        # Create a filter condition.
        filters = {}

        # Search for tickets.
        api.ticket. \
            ticket_list_detailed(IsA(http.HttpRequest),
                                 marker=None,
                                 paginate=True,
                                 filters=filters,
                                 sort_dir='desc',
                                 ticket_type=TICKET_TYPE).AndReturn(
                                     [[], False, False])
        self.mox.ReplayAll()
        res = self.client.get(reverse("horizon:admin:request_list:index"))

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/request_list/index.html')
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
                sort_dir='desc',
                ticket_type=TICKET_TYPE).AndRaise(self.aflo_exception)
        exceptions.handle(IsA(http.HttpRequest),
                          "Unable to retrieve requests information.")

        self.mox.ReplayAll()
        res = self.client.get(reverse("horizon:admin:request_list:index"))

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/request_list/index.html')
        self.assertEqual(res.status_code, 200)


class RequestListViewPaginationTest(aflo_test.BaseAdminViewTests):
    """Request list view pagination test class"""

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('ticket_list_detailed',
                                     'tickettemplates_get',)})
    def test_tickets_list_get_pagination(self):
        """Test 'Move next page'
        1 page have 2 row of ticket.
        """
        # Create a filter condition.
        filters = {}

        # Create ticket data list.
        ticket_data_list = []
        for data in fixture.REQUEST_TICKET_DATA_LIST:
            ticket_data_list.append(
                Ticket(self, data, loaded=True))

        # Get 5 row from fixture data
        tickets = ticket_data_list[:5]

        # Create number 1 page data.
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc',
            ticket_type=TICKET_TYPE).AndReturn([tickets[:2], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_1 = rtn_ticket[0]

        # Create number 2 page data.
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[1].id,
            paginate=True,
            filters=filters,
            sort_dir='desc',
            ticket_type=TICKET_TYPE).AndReturn([tickets[2:4], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_2 = rtn_ticket[0]

        # Create number 3 page data.
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[3].id,
            paginate=True,
            filters=filters,
            sort_dir='desc',
            ticket_type=TICKET_TYPE).AndReturn([tickets[4:], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_3 = rtn_ticket[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:admin:request_list:index")

        # Show number 1 page.(items 1-2)
        self.client.get(index_url)
        self.assertEqual(len(rtn_ticket_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 2-4)
        params = "=".join([tables.RequestTable._meta.pagination_param,
                           tickets[1].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_2),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 3 page.(items 5)
        params = "=".join([tables.RequestTable._meta.pagination_param,
                           tickets[3].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_3), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('ticket_list_detailed',
                                     'tickettemplates_get',)})
    def test_tickets_list_get_prev_pagination(self):
        """Test 'Move previous page'
        1 page have 2 row of ticket.
        """
        # Create a filter condition.
        filters = {}

        # Create ticket data list.
        ticket_data_list = []
        for data in fixture.REQUEST_TICKET_DATA_LIST:
            ticket_data_list.append(
                Ticket(self, data, loaded=True))

        # Get 5 row from fixture data.
        tickets = ticket_data_list[:3]

        # Create number 1 page data.
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc',
            ticket_type=TICKET_TYPE).AndReturn([tickets[:2], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_1 = rtn_ticket[0]

        # Create number 2 page data.
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[1].id,
            paginate=True,
            filters=filters,
            sort_dir='desc',
            ticket_type=TICKET_TYPE).AndReturn([tickets[2:], True, True])
        _get_ticket_templates(self, rtn_ticket[0])
        rtn_ticket_2 = rtn_ticket[0]

        # Create back page(number1) data.
        rtn_ticket = api.ticket.ticket_list_detailed(
            IsA(http.HttpRequest),
            marker=tickets[2].id,
            paginate=True,
            filters=filters,
            sort_dir='asc',
            ticket_type=TICKET_TYPE).AndReturn([tickets[:2], True, True])
        _get_ticket_templates(self, [tickets[1]])
        _get_ticket_templates(self, [tickets[0]])
        rtn_ticket_3 = rtn_ticket[0]

        self.mox.ReplayAll()
        index_url = reverse("horizon:admin:request_list:index")

        # Show number 1 page.(items 1-2)
        self.client.get(index_url)
        self.assertEqual(len(rtn_ticket_1),
                         settings.API_RESULT_PAGE_SIZE)

        # Move to number 2 page.(items 3)
        params = "=".join([tables.RequestTable._meta.pagination_param,
                           tickets[1].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_2), 1)

        # Move to back page(number1) data.
        params = "=".join([tables.RequestTable._meta.prev_pagination_param,
                           tickets[2].id])
        url = "?".join([index_url, params])
        self.client.get(url)
        self.assertEqual(len(rtn_ticket_3),
                         settings.API_RESULT_PAGE_SIZE)


class RequestListViewFilterTest(aflo_test.BaseAdminViewTests):
    """Request list view filter test class"""

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',)})
    @test.create_stubs({keystone: ('tenant_list',)})
    def test_request_list_get_filter_project(self):
        """Test 'get_filter[Project] of index'"""
        view = views.IndexView()
        view.request = None

        filter_option = {
            "filter_field": "tenant_id",
            "filter_string": "project-a",
            "result": {"tenant_id":
                       "7a867af0702c435981cfb970998b2337"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        # Create a project name.
        project_data = [Tenant(self, fixture.PROJECT_GET_DATA, loaded=True)]
        keystone.tenant_list(None). \
            AndReturn([project_data, False])

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)

    @test.create_stubs({views.IndexView: ('_get_filter_field',
                                          '_get_filter_string',)})
    def test_request_list_get_filter_category(self):
        """Test 'get_filter[Category] of index'"""
        view = views.IndexView()
        view.request = MagicMock()
        view.request.encoding = 'utf-8'

        filter_option = {
            "filter_field": "ticket_type",
            "filter_string": "Work",
            "result": {"ticket_type": "Work"}
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_category_multi_byte(self):
        """Test 'get_filter[Category] of index'"""
        view = views.IndexView()
        view.request = MagicMock()
        view.request.encoding = 'utf-8'

        filter_option = {
            "filter_field": "ticket_type",
            "filter_string": views.TICKET_TYPE['Work'],
            "result": {"ticket_type": 'Work'}
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_type(self):
        """Test 'get_filter[Type] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "ticket_template_name",
            "filter_string": "ticket_template_name_string",
            "result": {"ticket_template_name":
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_id(self):
        """Test 'get_filter[ID] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "ticket_id",
            "filter_string": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
            "result": {"ticket_id":
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_request_form(self):
        """Test 'get_filter[Request Form] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "application_kinds_name",
            "filter_string": "application_kinds_name_value",
            "result": {"application_kinds_name":
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
                                          '_get_timezone',)})
    def test_request_list_get_filter_issue_date(self):
        """Test 'get_filter[Issue Date] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "owner_at",
            "filter_string": "2015-07-29",
            "result": {"owner_at_from":
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
                                          '_get_timezone',)})
    def test_request_list_get_filter_issue_date_utc(self):
        """Test 'get_filter[Issue Date(UTC)] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "owner_at",
            "filter_string": "2015-07-29",
            "result": {"owner_at_from":
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_irregular_issue_date(self):
        """Test 'get_filter[Issue Date(irregular)] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "owner_at",
            "filter_string": "aaaaa",
            "result": {}
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_issuer(self):
        """Test 'get_filter[Issuer] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "owner_name",
            "filter_string": "owner_name_value",
            "result": {"owner_name":
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
                                          '_get_timezone',)})
    def test_request_list_get_filter_last_update(self):
        """Test 'get_filter[Last Update] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "last_confirmed_at",
            "filter_string": "2015-07-29",
            "result": {"last_confirmed_at_from":
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
                                          '_get_timezone',)})
    def test_request_list_get_filter_last_update_utc(self):
        """Test 'get_filter[Last Update(UTC)] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "last_confirmed_at",
            "filter_string": "2015-07-29",
            "result": {"last_confirmed_at_from":
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_irregular_last_update(self):
        """Test 'get_filter[Last Update(irregular)] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "last_confirmed_at",
            "filter_string": "aaaaa",
            "result": {}
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
                                          '_get_filter_string',)})
    def test_request_list_get_filter_updated_by(self):
        """Test 'get_filter[Updated By] of index'"""
        view = views.IndexView()

        filter_option = {
            "filter_field": "last_confirmer_name",
            "filter_string": "last_confirmer_name_value",
            "result": {"last_confirmer_name":
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
                                          '_get_filter_string',)})
    @test.create_stubs({api.ticket: ('ticket_list_detailed',)})
    @test.create_stubs({ticket_utils: ('get_language_name',)})
    def test_request_list_get_filter_status(self):
        """Test 'get_filter[Status] of index'"""
        view = views.IndexView()
        view.request = None

        filter_option = {
            "filter_field": "last_status_code",
            "filter_string": "Inquiring",
            "result": {"last_status_code":
                       "inquiring"}
        }

        # Create a filter condition.
        views.IndexView._get_filter_field(). \
            AndReturn(filter_option["filter_field"])
        views.IndexView._get_filter_string(). \
            AndReturn(filter_option["filter_string"])
        filters_result = filter_option['result']

        # Create a ticket of return data.(awaiting approval)
        ticket_data = \
            [Ticket(self, fixture.REQUEST_TICKET_DATA_LIST[0], loaded=True)]

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
            language_name).AndReturn('Inquiring')

        self.mox.ReplayAll()
        self.assertEqual(view.get_filters(), filters_result)


def _get_ticket_templates(self, ticket_data_list):

    user = fixture.REQUEST_TICKET_TEMPLATE_DATA_LIST[0]
    inquiry = fixture.REQUEST_TICKET_TEMPLATE_DATA_LIST[1]

    # Search for tickettemplate.
    for ticket in ticket_data_list:
        if ticket.ticket_template_id == user.get('id'):
            ticket_template_data = \
                Tickettemplate(self, user, loaded=True)

            api.ticket.tickettemplates_get(
                IsA(http.HttpRequest),
                ticket.ticket_template_id).AndReturn(ticket_template_data)

        elif ticket.ticket_template_id == inquiry.get('id'):
            ticket_template_data = \
                Tickettemplate(self, inquiry, loaded=True)

            api.ticket.tickettemplates_get(
                IsA(http.HttpRequest),
                ticket.ticket_template_id).AndReturn(ticket_template_data)
