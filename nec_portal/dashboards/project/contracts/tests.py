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

from mox3.mox import IsA
import six

from django.conf import settings
from django.core.urlresolvers import reverse
from django import http
from django.test.utils import override_settings

from openstack_dashboard.test import helpers as test

from nec_portal import api
from nec_portal.dashboards.project.contracts import fixture
from nec_portal.dashboards.project.contracts import panel  # noqa
from nec_portal.dashboards.project.contracts import tables
from nec_portal.dashboards.project.contracts import views
from nec_portal.dashboards.project.ticket_list import fixture \
    as ticket_fixture
from nec_portal.test import aflo_helpers as aflo_test

INDEX_URL = reverse("horizon:project:contracts:index")

CONTRACT_DETAIL_URL = reverse('horizon:project:contracts:detail',
                              kwargs={"id": fixture.CONTRACT_ID})


class ContractsViewTest(aflo_test.TestCase):
    """Contracts view test class"""

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles',),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=None)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles',),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_no_link(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(
        REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS_NO_SET_ROLE)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_no_set_role(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_not_has_role(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(['aaaa'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_filter_application_type(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """

        ticket_template_name = "ticket_template_name"
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337",
             "ticket_template_name": ticket_template_name})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        contract_data_list = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertEqual(contract_data_list[0][0].ticket_template_name,
                         ticket_template_name)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_filter_contract_id(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """

        parent_contract_id = "7a867af0702c435981cfb970998b4000"
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337",
             "parent_contract_id": parent_contract_id})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        contract_data_list = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertEqual(contract_data_list[0][0].parent_contract_id,
                         parent_contract_id)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_filter_application_name(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """

        application_name = "application_name"
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337",
             "application_name": application_name})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        contract_data_list = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertEqual(contract_data_list[0][0].application_name,
                         application_name)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_filter_application_date(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """

        application_date = "2015-08-08T17:51:53.000001"
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337",
             "application_date_from": "2015-08-08T00:00:00.000000",
             "application_date_to": "2015-08-08T23:59:59.999999"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        contract_data_list = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertEqual(contract_data_list[0][0].application_date,
                         application_date)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_filter_contract_start_date(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """

        lifetime_start = "2015-08-08T17:51:53.000001"
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337",
             "lifetime_start_from": "2015-08-08T00:00:00.000000",
             "lifetime_start_to": "2015-08-08T23:59:59.999999"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        contract_data_list = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertEqual(contract_data_list[0][0].lifetime_start,
                         lifetime_start)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_filter_contract_end_date(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """

        lifetime_end = "2999-12-31T23:59:59.999999"
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337",
             "lifetime_end_from": "2999-12-31T00:00:00.000000",
             "lifetime_end_to": "2999-12-31T23:59:59.999999"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        contract_data_list = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertEqual(contract_data_list[0][0].lifetime_end,
                         lifetime_end)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_filter_contract_date(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 1.
        """

        lifetime = "2016-12-31T23:59:59.999999"
        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337",
             "date_in_lifetime": "2016-12-31"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Create a contracts of return data.(awaiting approval)
        contract_data = [Contract(self,
                                  fixture.CONTRACT_DATA_LIST[0],
                                  loaded=True)]

        # Search for contracts.
        contract_data_list = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contract_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertLessEqual(contract_data_list[0][0].lifetime_start,
                             lifetime)
        self.assertGreaterEqual(contract_data_list[0][0].lifetime_end,
                                lifetime)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(REGION_CONTRACTS_LINKS=fixture.REGION_CONTRACTS_LINKS)
    @test.create_stubs({views.IndexView: ('get_filters', '_get_user_roles'),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_list_no_data(self):
        """Do a test of 'List Search of contracts'
        Test if the retrieved result is of 0.
        """

        # Create a filter condition.
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": "7a867af0702c435981cfb970998b2337"})

        # Create a link settings.
        views.IndexView._get_user_roles().AndReturn(
            ['T__DC1__ProjectMember'])

        # Search for contracts.
        api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None, paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([[], False, False])

        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({views.IndexView: ('get_filters',),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_get_pagination(self):
        """Do a test of 'List Search of contracts'
        Next page of paging.
        """

        # Create a filter condition.
        project_id = "7a867af0702c435981cfb970998b2337"
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": project_id})

        # Create contract data list.
        contract_data_list = []
        for data in fixture.CONTRACT_DATA_LIST:
            contract_data_list.append(Contract(self,
                                               data,
                                               loaded=True))
        contracts = contract_data_list[:5]

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None, paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contracts, True, True])
        rtn_contract_1 = rtn_contract[0]

        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": project_id})

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None, paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contracts[:2], True, True])
        rtn_contract_2 = rtn_contract[0]

        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": project_id})

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=contracts[2].contract_id,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contracts[2:4], True, True])
        rtn_contract_3 = rtn_contract[0]

        filters = views.IndexView.get_filters(). AndReturn(
            {"project_id": project_id})

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=contracts[4].contract_id,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contracts[4:], True, True])
        rtn_contract_4 = rtn_contract[0]

        self.mox.ReplayAll()
        res = self.client.get(INDEX_URL)

        # Get all.
        self.assertEqual(len(rtn_contract_1),
                         len(contracts))
        self.assertTemplateUsed(res, 'project/contracts/index.html')

        res = self.client.get(INDEX_URL)
        # Get first page with 2 items.
        self.assertEqual(len(rtn_contract_2),
                         settings.API_RESULT_PAGE_SIZE)

        params = "=".join([tables.ContractTable._meta.pagination_param,
                           contracts[2].contract_id])
        url = "?".join([INDEX_URL, params])
        res = self.client.get(url)
        # Get second page.(items 2-4)
        self.assertEqual(len(rtn_contract_3),
                         settings.API_RESULT_PAGE_SIZE)

        params = "=".join([tables.ContractTable._meta.pagination_param,
                           contracts[4].contract_id])
        url = "?".join([INDEX_URL, params])
        res = self.client.get(url)
        # Get third page.(item 5)
        self.assertEqual(len(rtn_contract_4), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({views.IndexView: ('get_filters',),
                        api.ticket: ('contract_list_detailed',)})
    def test_contracts_get_prev_pagination(self):
        """Do a test of 'List Search of contracts'
        Prev page of paging.
        """

        # Create a filter condition.
        project_id = "7a867af0702c435981cfb970998b2337"
        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": project_id})

        # Create contract data list.
        contract_data_list = []
        for data in fixture.CONTRACT_DATA_LIST:
            contract_data_list.append(Contract(self, data, loaded=True))
        contracts = contract_data_list[:3]

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contracts, True, False])
        rtn_contract_1 = rtn_contract[0]

        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": project_id})

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=None, paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contracts[:2], True, True])
        rtn_contract_2 = rtn_contract[0]

        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": project_id})

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=contracts[2].contract_id,
            paginate=True,
            filters=filters,
            sort_dir='desc,desc').AndReturn([contracts[2:], True, True])
        rtn_contract_3 = rtn_contract[0]

        filters = views.IndexView.get_filters().AndReturn(
            {"project_id": project_id})

        rtn_contract = api.ticket.contract_list_detailed(
            IsA(http.HttpRequest),
            marker=contracts[2].contract_id,
            paginate=True,
            filters=filters,
            sort_dir='asc,asc').AndReturn([contracts[:2], True, True])
        rtn_contract_4 = rtn_contract[0]

        self.mox.ReplayAll()
        res = self.client.get(INDEX_URL)

        # get all.
        self.assertEqual(len(rtn_contract_1),
                         len(contracts))
        self.assertTemplateUsed(res, 'project/contracts/index.html')

        res = self.client.get(INDEX_URL)
        # get first page with 2 items.
        self.assertEqual(len(rtn_contract_2),
                         settings.API_RESULT_PAGE_SIZE)

        params = "=".join([tables.ContractTable._meta.pagination_param,
                           contracts[2].contract_id])
        url = "?".join([INDEX_URL, params])
        res = self.client.get(url)
        # get second page.(item 3)
        self.assertEqual(len(rtn_contract_3), 1)

        params = "=".join([tables.ContractTable._meta.prev_pagination_param,
                           contracts[2].contract_id])
        url = "?".join([INDEX_URL, params])
        res = self.client.get(url)
        # prev back to get first page with 2 items.
        self.assertEqual(len(rtn_contract_4),
                         settings.API_RESULT_PAGE_SIZE)


class ContractsTest(aflo_test.TestCase):

    @test.create_stubs({api.ticket: ('contract_get_detailed',
                                     'tickettemplates_get',)})
    def test_contract_detail_view(self):
        """Test 'View a contract detail'"""
        # Create a contract of return data.
        contract_data = \
            Contract(self,
                     fixture.CONTRACT_GET_DATA[0],
                     loaded=True)
        ticket_data = Tickettemplate(
            self,
            ticket_fixture.CONTRACT_TICKET_TEMPLATE_DATA_LIST[0],
            loaded=True)

        api.ticket.contract_get_detailed(IsA(http.HttpRequest),
                                         contract_data.contract_id) \
            .AndReturn(contract_data)
        api.ticket.tickettemplates_get(IsA(http.HttpRequest),
                                       contract_data.ticket_template_id) \
            .AndReturn(ticket_data)
        self.mox.ReplayAll()

        res = self.client.get(CONTRACT_DETAIL_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/contracts/detail.html')
        self.assertEqual(res.status_code, 200)


class Contract(object):
    """Contract resource."""

    def __init__(self, manager, info, loaded=False):
        """Populate and bind to a manager.

        :param manager: BaseManager object
        :param info: dictionary representing resource attributes
        :param loaded: prevent lazy-loading if set to True
        """
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._loaded = loaded

    def __repr__(self):
        """String of contract object."""
        return "<Contract %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass


class Tickettemplate(object):
    """Represents a ticket template."""

    def __init__(self, manager, info, loaded=False):
        """Populate and bind to a manager.

        :param manager: BaseManager object
        :param info: dictionary representing resource attributes
        :param loaded: prevent lazy-loading if set to True
        """
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._loaded = loaded

    def __repr__(self):
        """String of Object."""
        return "<Tickettemplate %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass
