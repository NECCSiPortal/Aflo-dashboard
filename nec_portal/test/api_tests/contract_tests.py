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

import six

import afloclient

from django.conf import settings
from django.test.utils import override_settings

from nec_portal import api
from nec_portal.api import ticket  # noqa
from nec_portal.dashboards.project.contracts import \
    fixture as contracts_fixture
from openstack_dashboard.test import helpers as test

CURRENCY_FORMAT = getattr(settings, 'CURRENCY_FORMAT', '{0:,.2f}')


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
    def test_contract_list_detailed_no_pagination(self):
        """"Verify that all contracts
        are returned even with a small page size.
        """
        api_contracts = []
        for data in contracts_fixture.CONTRACT_DATA_LIST[:5]:
            api_contracts.append(
                Contract(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc,desc',
                  'sort_key': 'lifetime_start,contract_id', }

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        afloclient.contracts.list(kwargs) \
            .AndReturn(iter(api_contracts))
        self.mox.ReplayAll()

        contracts, has_more, has_prev = api.ticket.contract_list_detailed(
            self.request)
        self.assertItemsEqual(contracts, api_contracts)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_contract_list_detailed_filters(self):
        """"Verify that sort_dir and sort_key work"""
        api_contracts = []
        for data in contracts_fixture.CONTRACT_DATA_LIST[:2]:
            api_contracts.append(
                Contract(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        sort_dir = 'desc,desc'
        sort_key = 'lifetime_start,contract_id'
        filters = {'project_id': '7a867af0702c435981cfb970998b2337',
                   'application_name': 'application_name'}

        kwargs = {'limit': limit,
                  'sort_dir': sort_dir,
                  'sort_key': sort_key}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        afloclient.contracts.list(kwargs) \
            .AndReturn(iter(api_contracts))
        self.mox.ReplayAll()

        contracts, has_more, has_prev = api.ticket.contract_list_detailed(
            self.request,
            sort_dir=sort_dir,
            marker=None,
            filters=filters)
        self.assertItemsEqual(contracts, api_contracts)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_contract_list_detailed_pagination_more_page_size(self):
        """"The total snapshot count is over page size, should return
        page_size contracts.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_contracts = []
        for data in contracts_fixture.CONTRACT_DATA_LIST[:5]:
            api_contracts.append(
                Contract(self, data, loaded=True))
        contracts_iter = iter(api_contracts)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc,desc',
                  'sort_key': 'lifetime_start,contract_id', }

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        # Pass back all contracts, ignoring filters
        afloclient.contracts.list(kwargs).AndReturn(contracts_iter)
        self.mox.ReplayAll()

        contracts, has_more, has_prev = api.ticket.contract_list_detailed(
            self.request,
            marker=None,
            filters=None,
            paginate=True)
        expected_contracts = api_contracts[:page_size]
        self.assertItemsEqual(contracts, expected_contracts)
        self.assertTrue(has_more)
        self.assertFalse(has_prev)
        # Ensure that only the needed number of contracts are consumed
        # from the iterator (page_size + 1).
        self.assertEqual(len(list(contracts_iter)),
                         len(api_contracts) - len(expected_contracts) - 1)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_contract_list_detailed_pagination_less_page_size(self):
        """"The total contract count is less than page size,
        should return contracts more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_contracts = []
        for data in contracts_fixture.CONTRACT_DATA_LIST[:5]:
            api_contracts.append(
                Contract(self, data, loaded=True))
        contracts_iter = iter(api_contracts)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc,desc',
                  'sort_key': 'lifetime_start,contract_id', }

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        # Pass back all contracts, ignoring filters
        afloclient.contracts.list(kwargs).AndReturn(contracts_iter)
        self.mox.ReplayAll()

        contracts, has_more, has_prev = api.ticket.contract_list_detailed(
            self.request,
            filters=None,
            paginate=True)
        expected_contracts = api_contracts[:page_size]
        self.assertItemsEqual(contracts, expected_contracts)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=5)
    def test_contract_list_detailed_pagination_equal_page_size(self):
        """"The total contract count equals page size, should return
        page_size contracts. more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_contracts = []
        for data in contracts_fixture.CONTRACT_DATA_LIST[:5]:
            api_contracts.append(
                Contract(self, data, loaded=True))
        contracts_iter = iter(api_contracts)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc,desc',
                  'sort_key': 'lifetime_start,contract_id', }

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        afloclient.contracts.list(kwargs).AndReturn(contracts_iter)
        self.mox.ReplayAll()

        contracts, has_more, has_prev = api.ticket.contract_list_detailed(
            self.request,
            filters=None,
            paginate=True)
        expected_contracts = api_contracts[:page_size]
        self.assertItemsEqual(contracts, expected_contracts)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)
        self.assertEqual(len(expected_contracts), len(contracts))

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_contract_list_detailed_pagination_marker(self):
        """"Tests getting a second page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = '02262dc1-9906-41bc-822d-426a5ba3f764'

        api_contracts = []
        for data in contracts_fixture.CONTRACT_DATA_LIST[:5]:
            api_contracts.append(
                Contract(self, data, loaded=True))
        contracts_iter = iter(api_contracts[page_size:])

        kwargs = {'limit': limit,
                  'sort_dir': 'desc,desc',
                  'sort_key': 'lifetime_start,contract_id', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        # Pass back all contracts, ignoring filters
        afloclient.contracts.list(kwargs) \
            .AndReturn(contracts_iter)
        self.mox.ReplayAll()

        contracts, has_more, has_prev = api.ticket.contract_list_detailed(
            self.request,
            marker=marker,
            filters=None,
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_contract_list_detailed_pagination_marker_prev(self):
        """"Tests getting previous page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = '02262dc1-9906-41bc-822d-426a5ba3f764'

        api_contracts = []
        for data in contracts_fixture.CONTRACT_DATA_LIST[:5]:
            api_contracts.append(
                Contract(self, data, loaded=True))
        contracts_iter = iter(api_contracts[page_size:])

        kwargs = {'limit': limit,
                  'sort_dir': 'asc,asc',
                  'sort_key': 'lifetime_start,contract_id', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        # Pass back all contracts, ignoring filters
        afloclient.contracts.list(kwargs) \
            .AndReturn(contracts_iter)
        self.mox.ReplayAll()

        contracts, has_more, has_prev = api.ticket.contract_list_detailed(
            self.request,
            marker=marker,
            filters=None,
            sort_dir='asc,asc',
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_contract_list_detailed_exception(self):
        """"Verify that all contracts
        are returned even with a small page size.
        """
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc,desc',
                  'sort_key': 'lifetime_start,contract_id', }

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        afloclient.contracts.list(kwargs) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.contract_list_detailed,
                          self.request)

    def test_contract_get_detailed(self):
        """Verify that the specified contract data
        can be acquired.
        """
        api_contract = Contract(self,
                                contracts_fixture.CONTRACT_DATA_LIST[0],
                                loaded=True)

        contract_id = '02262dc1-9906-41bc-822d-426a5ba3f763'

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        afloclient.contracts.get(contract_id) \
            .AndReturn(api_contract)
        self.mox.ReplayAll()

        contract_data = api.ticket.contract_get_detailed(
            self.request,
            contract_id=contract_id)
        self.assertEqual(contract_data, api_contract)

    def test_contract_get_detailed_exception(self):
        """Verify that the specified contract data
        can be acquired.
        """
        contract_id = '02262dc1-9906-41bc-822d-426a5ba3f763'

        afloclient = self.stub_afloclient()
        afloclient.contracts = self.mox.CreateMockAnything()
        afloclient.contracts.get(contract_id) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.contract_get_detailed,
                          self.request,
                          contract_id)


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
