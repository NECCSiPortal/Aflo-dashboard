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

import datetime
import decimal
from decimal import Decimal
import six

import afloclient

from django.conf import settings
from django.test.utils import override_settings
from django.utils.html import escape

import horizon

from nec_portal import api
from nec_portal.dashboards.project.private_price_lists import \
    fixture as catalogs_fixture
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
    def test_catalog_list_detailed_no_pagination(self):
        """"Verify that all catalogs
        are returned even with a small page size.
        """
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST:
            api_catalogs.append(
                Catalog(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id', }

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_list_detailed(
            self.request)
        self.assertItemsEqual(catalogs, api_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_list_detailed_filters(self):
        """"Verify that sort_dir and sort_key work"""
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST[:2]:
            api_catalogs.append(
                Catalog(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        sort_dir = 'desc'
        sort_key = 'catalog_id'
        filters = {'lifetime': '2016-01-01T12:00:00.000000',
                   'catalog_name': 'CPU'}

        kwargs = {'limit': limit,
                  'sort_dir': sort_dir,
                  'sort_key': sort_key}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_list_detailed(
            self.request,
            filters=filters)
        self.assertItemsEqual(catalogs, api_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_list_detailed_pagination_more_page_size(self):
        """"The total snapshot count is over page size, should return
        page_size catalogs.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST[:5]:
            api_catalogs.append(
                Catalog(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id', }

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        # Pass back all catalogs, ignoring filters
        afloclient.catalogs.list(kwargs).AndReturn(catalogs_iter)
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_list_detailed(
            self.request,
            marker=None,
            filters=None,
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertTrue(has_more)
        self.assertFalse(has_prev)
        # Ensure that only the needed number of catalogs are consumed
        # from the iterator (page_size + 1).
        self.assertEqual(len(list(catalogs_iter)),
                         len(api_catalogs) - len(expected_catalogs) - 1)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_catalog_list_detailed_pagination_less_page_size(self):
        """"The total catalog count is less than page size,
        should return catalogs more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST:
            api_catalogs.append(
                Catalog(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id', }

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        # Pass back all catalogs, ignoring filters
        afloclient.catalogs.list(kwargs).AndReturn(catalogs_iter)
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_list_detailed(
            self.request,
            filters=None,
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=6)
    def test_catalog_list_detailed_pagination_equal_page_size(self):
        """"The total catalog count equals page size, should return
        page_size catalogs. more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST:
            api_catalogs.append(
                Catalog(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id', }

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs).AndReturn(catalogs_iter)
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_list_detailed(
            self.request,
            filters=None,
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)
        self.assertEqual(len(expected_catalogs), len(catalogs))

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_list_detailed_pagination_marker(self):
        """"Tests getting a second page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = '200'

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST:
            api_catalogs.append(
                Catalog(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs[page_size:])

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        # Pass back all catalogs, ignoring filters
        afloclient.catalogs.list(kwargs) \
            .AndReturn(catalogs_iter)
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_list_detailed(
            self.request,
            marker=marker,
            filters=None,
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_list_detailed_pagination_marker_prev(self):
        """"Tests getting previous page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = '400'

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST:
            api_catalogs.append(
                Catalog(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs[page_size:])

        kwargs = {'limit': limit,
                  'sort_dir': 'asc',
                  'sort_key': 'catalog_id', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        # Pass back all catalogs, ignoring filters
        afloclient.catalogs.list(kwargs) \
            .AndReturn(catalogs_iter)
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_list_detailed(
            self.request,
            marker=marker,
            filters=None,
            sort_dir='asc',
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    def test_catalog_list_detailed_exception(self):
        """Verify that the specified catalog data
        can be acquired.
        """
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id', }

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.catalog_list_detailed,
                          self.request)

    def test_catalog_get_detailed(self):
        """Verify that the specified catalog data
        can be acquired.
        """
        api_catalog = Catalog(self,
                              catalogs_fixture.CATALOG_DATA_LIST[0],
                              loaded=True)

        catalog_id = '100'

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.get(catalog_id) \
            .AndReturn(api_catalog)
        self.mox.ReplayAll()

        contract_data = api.ticket.catalog_get_detailed(
            self.request,
            catalog_id='100')
        self.assertEqual(contract_data, api_catalog)

    def test_catalog_get_detailed_exception(self):
        """Verify that the specified catalog data
        can be acquired.
        """
        catalog_id = '100'

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.get(catalog_id) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.catalog_get_detailed,
                          self.request,
                          catalog_id)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_price_list_detailed_no_pagination(self):
        """"Verify that all prices
        are returned even with a small page size.
        """
        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start', }

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn(iter(api_prices))
        self.mox.ReplayAll()

        prices, has_prev, has_more = api.ticket.price_list_detailed(
            self.request,
            catalog_id)
        self.assertItemsEqual(prices, api_prices)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_price_list_detailed_filters(self):
        """"Verify that sort_dir and sort_key work"""
        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        filters = {'lifetime': '2016-01-01T12:00:00.000000'}

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start'}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn(iter(api_prices))
        self.mox.ReplayAll()

        prices, has_prev, has_more = api.ticket.price_list_detailed(
            self.request,
            catalog_id,
            filters=filters)
        self.assertItemsEqual(prices, api_prices)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_price_list_detailed_pagination_more_page_size(self):
        """"The total snapshot count is over page size, should return
        page_size prices.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))
        prices_iter = iter(api_prices)

        catalog_id = '100'
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start', }

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        # Pass back all prices, ignoring filters
        afloclient.price.list(catalog_id, kwargs).AndReturn(prices_iter)
        self.mox.ReplayAll()

        prices, has_prev, has_more = api.ticket.price_list_detailed(
            self.request,
            catalog_id,
            marker=None,
            filters=None,
            paginate=True)
        expected_prices = api_prices[:page_size]
        self.assertItemsEqual(prices, expected_prices)
        self.assertTrue(has_more)
        self.assertFalse(has_prev)
        # Ensure that only the needed number of prices are consumed
        # from the iterator (page_size + 1).
        self.assertEqual(len(list(prices_iter)),
                         len(api_prices) - len(expected_prices) - 1)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_price_list_detailed_pagination_less_page_size(self):
        """"The total price count is less than page size,
        should return prices more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))
        prices_iter = iter(api_prices)

        catalog_id = '100'
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start', }

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        # Pass back all prices, ignoring filters
        afloclient.price.list(catalog_id, kwargs).AndReturn(prices_iter)
        self.mox.ReplayAll()

        prices, has_prev, has_more = api.ticket.price_list_detailed(
            self.request,
            catalog_id,
            filters=None,
            paginate=True)
        expected_prices = api_prices[:page_size]
        self.assertItemsEqual(prices, expected_prices)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=7)
    def test_price_list_detailed_pagination_equal_page_size(self):
        """"The total price count equals page size, should return
        page_size prices. more, prev should return False.
        """
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))
        prices_iter = iter(api_prices)

        catalog_id = '100'
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start', }

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs).AndReturn(prices_iter)
        self.mox.ReplayAll()

        prices, has_prev, has_more = api.ticket.price_list_detailed(
            self.request,
            catalog_id,
            filters=None,
            paginate=True)
        expected_prices = api_prices[:page_size]
        self.assertItemsEqual(prices, expected_prices)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)
        self.assertEqual(len(expected_prices), len(prices))

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_price_list_detailed_pagination_marker(self):
        """"Tests getting a second page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = 'b0536e64-e20f-4280-88bf-deafaae8d3d0'

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))
        prices_iter = iter(api_prices[page_size:])

        catalog_id = '100'
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        # Pass back all prices, ignoring filters
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn(prices_iter)
        self.mox.ReplayAll()

        prices, has_prev, has_more = api.ticket.price_list_detailed(
            self.request,
            catalog_id,
            marker=marker,
            filters=None,
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_price_list_detailed_pagination_marker_prev(self):
        """"Tests getting previous page with a marker"""
        page_size = settings.API_RESULT_PAGE_SIZE
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = 'b0536e64-e20f-4280-88bf-deafaae8d3d0'

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))
        prices_iter = iter(api_prices[page_size:])

        catalog_id = '100'
        kwargs = {'limit': limit,
                  'sort_dir': 'asc',
                  'sort_key': 'lifetime_start', }

        if marker:
            kwargs['marker'] = marker

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        # Pass back all prices, ignoring filters
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn(prices_iter)
        self.mox.ReplayAll()

        prices, has_prev, has_more = api.ticket.price_list_detailed(
            self.request,
            catalog_id,
            marker=marker,
            filters=None,
            sort_dir='asc',
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    def test_price_list_detailed_exception(self):
        """Verify that the specified catalog data
        can be acquired.
        """
        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start', }

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.price_list_detailed,
                          self.request,
                          catalog_id)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_price_get_with_project_id_get_data(self):
        """Verify that the specified catalog data
        can be acquired.
        """
        api_price = Price(self,
                          catalogs_fixture.PRICE_DATA_LIST[0],
                          loaded=True)

        # Get price for catalog.
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        catalog_id = '100'
        project_id = '5a53a6a5aab54293884b96e3cb1b1754'
        filters = {'scope': project_id}
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'lifetime': lifetime}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn(iter([api_price]))
        self.mox.ReplayAll()

        contract_data = api.ticket.price_get_with_project_id(
            self.request,
            project_id=project_id,
            catalog_id=catalog_id,
            scope='Default',
            seq_no='1')
        self.assertEqual(contract_data, api_price)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_price_get_with_project_id_no_data(self):
        """Verify that the specified price data
        where can't get data.
        """
        api_price = Price(self,
                          catalogs_fixture.PRICE_DATA_LIST[0],
                          loaded=True)

        # Get price for catalog.
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        catalog_id = '100'
        project_id = '5a53a6a5aab54293884b96e3cb1b1754'
        filters = {'scope': project_id}
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'lifetime': lifetime}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn([])
        afloclient.price.get(catalog_id, 'Default', '1') \
            .AndReturn(api_price)
        self.mox.ReplayAll()

        contract_data = api.ticket.price_get_with_project_id(
            self.request,
            project_id=project_id,
            catalog_id=catalog_id,
            scope='Default',
            seq_no='1')
        self.assertEqual(contract_data, api_price)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_price_get_with_project_id_exception(self):
        """Verify that the specified catalog data
        can be acquired.
        """
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        catalog_id = '100'
        project_id = '5a53a6a5aab54293884b96e3cb1b1754'
        filters = {'scope': project_id}
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'lifetime': lifetime}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn([])
        afloclient.price.get(catalog_id, 'Default', '1') \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.price_get_with_project_id,
                          self.request,
                          project_id=project_id,
                          catalog_id=catalog_id,
                          scope='Default',
                          seq_no='1')

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_price_update_or_create_get_data(self):
        """Tests to update the specified data
        where scope is default.
        """
        api_price = Price(self,
                          catalogs_fixture.PRICE_DATA_LIST[1],
                          loaded=True)

        # Get price for catalog.
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        catalog_id = '100'
        scope = '5a53a6a5aab54293884b96e3cb1b1754'
        filters = {'scope': scope,
                   'lifetime': '2015-08-01T12:30:45.000000'}
        field = {"price": "100",
                 'lifetime_start': lifetime,
                 'lifetime_end': '9999-12-31T23:59:59.999999'}
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start'}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn(iter([api_price]))
        afloclient.price.update(
            catalog_id,
            scope,
            "2",
            {'lifetime_end': "2015-08-01T12:30:44.000000"}) \
            .AndReturn(api_price)
        afloclient.price.create(catalog_id, scope, field) \
            .AndReturn(api_price)
        self.mox.ReplayAll()

        contract_data = api.ticket.price_update_or_create(
            self.request,
            catalog_id=catalog_id,
            scope=scope,
            fields={"price": "100"})
        self.assertEqual(contract_data, api_price)

    def test_price_update_or_create_get_no_data(self):
        """Tests to create the specified data
        where scope is default.
        """
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        catalog_id = '100'
        scope = '5a53a6a5aab54293884b96e3cb1b1754'
        filters = {'scope': scope,
                   'lifetime': '2015-08-01T23:59:59.000000'}
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start'}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn([])
        self.mox.ReplayAll()

        contract_data = api.ticket.price_update_or_create(
            self.request,
            catalog_id=catalog_id,
            scope=scope,
            fields={"price": "100"},
            now='2015-08-01T23:59:59.000000',
            del_flg=True)
        self.assertEqual(contract_data, {})

    def test_price_update_or_create_exception_create(self):
        """Tests to create the specified data
        where scope is default.
        """
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        catalog_id = '100'
        scope = '5a53a6a5aab54293884b96e3cb1b1754'
        filters = {'scope': scope,
                   'lifetime': '2015-08-01T23:59:59.000000'}
        field = {"price": "100"}
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start'}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn([])
        afloclient.price.create(catalog_id, scope, field) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.price_update_or_create,
                          self.request,
                          catalog_id=catalog_id,
                          scope=scope,
                          fields=field,
                          now='2015-08-01T23:59:59.000000')

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_price_update_or_create_exception_update(self):
        """Tests to update the specified data
        where scope is default.
        """
        api_price = Price(self,
                          catalogs_fixture.PRICE_DATA_LIST[1],
                          loaded=True)

        api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        catalog_id = '100'
        scope = '5a53a6a5aab54293884b96e3cb1b1754'
        filters = {'scope': scope,
                   'lifetime': '2015-08-01T12:30:45.000000'}
        field = {'lifetime_end': '2015-08-01T12:30:44.000000'}
        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start'}
        kwargs.update(filters)

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, kwargs) \
            .AndReturn(iter([api_price]))
        afloclient.price.update(catalog_id, scope, "2", field) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.price_update_or_create,
                          self.request,
                          catalog_id=catalog_id,
                          scope=scope,
                          fields={'price': 100})

    def catalog_contents_get_detailed(self):
        """Verify that the specified catalog contents data
        can be acquired.
        """
        api_catalog_contents = Catalog(
            self,
            catalogs_fixture.CATALOG_DATA_LIST[0],
            loaded=True)

        catalog_id = '100'

        afloclient = self.stub_afloclient()
        afloclient.catalog_contents = self.mox.CreateMockAnything()
        afloclient.catalog_contents.get(catalog_id) \
            .AndReturn(api_catalog_contents)
        self.mox.ReplayAll()

        catalog_contents_data = api.ticket.catalog_get_detailed(
            self.request,
            catalog_id='100')
        self.assertEqual(catalog_contents_data, api_catalog_contents)

    def test_catalog_contents_get_detailed_exception(self):
        """Verify that the specified catalog contents data
        can be acquired.
        """
        catalog_id = '100'

        afloclient = self.stub_afloclient()
        afloclient.catalog_contents = self.mox.CreateMockAnything()
        afloclient.catalog_contents.get(catalog_id) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.catalog_contents_get_detailed,
                          self.afloclient,
                          catalog_id)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('get_datetime_utcnow',)})
    def test_price_list_detailed2(self):
        """"Verify that all catalog prices
        can be acquired.
        """
        catalog_id = '100'
        date_now = _get_datetime_utcnow()
        lifetime = {'lifetime': date_now}

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST:
            api_prices.append(
                Price(self, data, loaded=True))

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, lifetime) \
            .AndReturn(iter(api_prices))

        api.ticket.get_datetime_utcnow().AndReturn(date_now)

        self.mox.ReplayAll()

        price_data = api.ticket.price_list_detailed2(
            self.request,
            catalog_id='100')
        self.assertItemsEqual(price_data, api_prices)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({api.ticket: ('get_datetime_utcnow',)})
    def test_price_list_detailed2_exception(self):
        """"Verify that all catalog prices
        can be acquired.
        """
        catalog_id = '100'
        date_now = _get_datetime_utcnow()
        lifetime = {'lifetime': date_now}

        afloclient = self.stub_afloclient()
        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list(catalog_id, lifetime) \
            .AndRaise(OSError)

        api.ticket.get_datetime_utcnow().AndReturn(date_now)

        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.price_list_detailed2,
                          self.request,
                          catalog_id)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_price_list(self):
        """"Verify that all catalog prices
        are returned default price or project price.
        """
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST[:5]:
            api_catalogs.append(
                Catalog(self, data, loaded=True))

        # Get price for catalog.
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        details = []

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        project_id = '5a53a6a5aab54293884b96e3cb1b1754'

        kwargs_cata = {'limit': limit,
                       'sort_dir': 'desc',
                       'sort_key': 'catalog_id', }
        kwargs_pri = {'limit': limit,
                      'sort_dir': 'desc',
                      'sort_key': 'lifetime_start',
                      'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs_cata) \
            .AndReturn(iter(api_catalogs))

        afloclient.price = self.mox.CreateMockAnything()

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST[:2]:
            api_prices.append(
                Price(self, data, loaded=True))
        afloclient.price.list(api_catalogs[0].catalog_id, kwargs_pri) \
            .AndReturn(iter(api_prices))
        detail = ProjectCatalog(api_catalogs[0].catalog_id,
                                api_prices[1].scope,
                                api_prices[1].seq_no,
                                api_catalogs[0].catalog_name,
                                api_prices[1].price,
                                project_id)
        details.append(detail)

        api_prices = [Price(self,
                            catalogs_fixture.PRICE_DATA_LIST[2],
                            loaded=True)]
        afloclient.price.list(api_catalogs[1].catalog_id, kwargs_pri) \
            .AndReturn(iter(api_prices))
        detail = ProjectCatalog(api_catalogs[1].catalog_id,
                                api_prices[0].scope,
                                api_prices[0].seq_no,
                                api_catalogs[1].catalog_name,
                                api_prices[0].price,
                                project_id)
        details.append(detail)

        api_prices = [Price(self,
                            catalogs_fixture.PRICE_DATA_LIST[3],
                            loaded=True)]
        afloclient.price.list(api_catalogs[2].catalog_id, kwargs_pri) \
            .AndReturn(iter(api_prices))
        detail = ProjectCatalog(api_catalogs[2].catalog_id,
                                api_prices[0].scope,
                                api_prices[0].seq_no,
                                api_catalogs[2].catalog_name,
                                api_prices[0].price,
                                project_id)
        details.append(detail)

        api_prices = []
        for data in catalogs_fixture.PRICE_DATA_LIST[4:6]:
            api_prices.append(
                Price(self, data, loaded=True))
        afloclient.price.list(api_catalogs[3].catalog_id, kwargs_pri) \
            .AndReturn(iter(api_prices))
        detail = ProjectCatalog(api_catalogs[3].catalog_id,
                                api_prices[1].scope,
                                api_prices[1].seq_no,
                                api_catalogs[3].catalog_name,
                                api_prices[1].price,
                                project_id)
        details.append(detail)

        api_prices = [Price(self,
                            catalogs_fixture.PRICE_DATA_LIST[6],
                            loaded=True)]
        afloclient.price.list(api_catalogs[4].catalog_id, kwargs_pri) \
            .AndReturn(iter(api_prices))
        detail = ProjectCatalog(api_catalogs[4].catalog_id,
                                api_prices[0].scope,
                                api_prices[0].seq_no,
                                api_catalogs[4].catalog_name,
                                api_prices[0].price,
                                project_id)
        details.append(detail)

        self.mox.ReplayAll()

        catalog_price, has_prev, has_more = api.ticket.catalog_price_list(
            self.request,
            catalogs_fixture.PROJECT_ID,
            sort_dir='desc',
            sort_key='catalog_id')
        self.assertEqual(catalog_price[0].catalog_id, details[0].catalog_id)
        self.assertEqual(catalog_price[0].price, details[0].price)
        self.assertEqual(catalog_price[1].catalog_id, details[1].catalog_id)
        self.assertEqual(catalog_price[1].price, details[1].price)
        self.assertEqual(catalog_price[2].catalog_id, details[2].catalog_id)
        self.assertEqual(catalog_price[2].price, details[2].price)
        self.assertEqual(catalog_price[3].catalog_id, details[3].catalog_id)
        self.assertEqual(catalog_price[3].price, details[3].price)
        self.assertEqual(catalog_price[4].catalog_id, details[4].catalog_id)
        self.assertEqual(catalog_price[4].price, details[4].price)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_price_list_no_catalog(self):
        """"Verify that all catalog prices
        if catalog data is none.
        """
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs_cata = {'limit': limit,
                       'sort_dir': 'desc',
                       'sort_key': 'catalog_id', }

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs_cata) \
            .AndReturn([])

        self.mox.ReplayAll()

        catalog_price, has_prev, has_more = api.ticket.catalog_price_list(
            self.request,
            catalogs_fixture.PROJECT_ID,
            sort_dir='desc',
            sort_key='catalog_id')
        self.assertEqual(catalog_price, [])
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_price_list_no_price_data(self):
        """"Verify that all catalog prices
        if price data is none.
        """
        api_catalogs = []
        api_catalogs.append(
            Catalog(self, catalogs_fixture.CATALOG_DATA_LIST[0], loaded=True))

        # Get price for catalog.
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        kwargs_cata = {'limit': limit,
                       'sort_dir': 'desc',
                       'sort_key': 'catalog_id', }
        kwargs_pri = {'limit': limit,
                      'sort_dir': 'desc',
                      'sort_key': 'lifetime_start',
                      'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs_cata) \
            .AndReturn(iter(api_catalogs))

        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list('100', kwargs_pri) \
            .AndReturn([])

        self.mox.ReplayAll()

        catalog_price, has_prev, has_more = api.ticket.catalog_price_list(
            self.request,
            catalogs_fixture.PROJECT_ID,
            sort_dir='desc',
            sort_key='catalog_id')
        self.assertEqual(catalog_price, [])
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',),
                        horizon.messages: ('horizon_message_already_queued',)})
    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_price_list_no_price_data_exception(self):
        """"Verify that all catalog prices
        if price data is none.
        """
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        api_catalogs = []
        api_catalogs.append(
            Catalog(self, catalogs_fixture.CATALOG_DATA_LIST[0], loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        kwargs_cata = {'limit': limit,
                       'sort_dir': 'desc',
                       'sort_key': 'catalog_id', }
        kwargs_pri = {'limit': limit,
                      'sort_dir': 'desc',
                      'sort_key': 'lifetime_start',
                      'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs_cata) \
            .AndReturn(iter(api_catalogs))

        horizon.messages.horizon_message_already_queued(
            self.request,
            'Unable to retrieve project catalog list.').AndReturn(True)

        afloclient.price = self.mox.CreateMockAnything()
        afloclient.price.list('100', kwargs_pri) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        catalog_price, has_prev, has_more = api.ticket.catalog_price_list(
            self.request, catalogs_fixture.PROJECT_ID,
            sort_dir='desc', sort_key='catalog_id')
        self.assertEqual(catalog_price, [])
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_catalog_scope_list(self):
        """Test to get public data and private data.
        Test the operation of the standard.
        """
        # Get catalog data
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST[:5]:
            api_catalogs.append(
                Catalog(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        kwargs_cata = {'limit': limit,
                       'sort_dir': None,
                       'sort_key': None}

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs_cata) \
            .AndReturn(iter(api_catalogs))

        # Get public catalog scope data
        api_public_catalog_scope = []
        for data in catalogs_fixture.VALID_PUBLIC_DATA_LIST[:6]:
            api_public_catalog_scope.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        kwargs_public = {'limit': limit,
                         'sort_dir': 'asc',
                         'sort_key': 'catalog_id',
                         'scope': 'Default',
                         'lifetime': lifetime,
                         'refine_flg': True}

        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs_public) \
            .AndReturn(iter(api_public_catalog_scope))

        # Get private catalog scope data
        api_private_catalog_scope = []
        for data in catalogs_fixture.VALID_PRIVATE_DATA_LIST[:3]:
            api_private_catalog_scope.append(
                ValidCatalog(self, data, loaded=True))

        kwargs_public = {'limit': limit,
                         'sort_dir': 'asc',
                         'sort_key': 'catalog_id',
                         'scope': '5a53a6a5aab54293884b96e3cb1b1754',
                         'lifetime': lifetime,
                         'refine_flg': True}

        afloclient.valid_catalog.list(kwargs_public) \
            .AndReturn(iter(api_private_catalog_scope))

        self.mox.ReplayAll()

        catalog_scope, has_prev, has_more = api.ticket.catalog_scope_list(
            self.request,
            catalogs_fixture.PROJECT_ID)
        self.assertEqual(catalog_scope[0].catalog_id,
                         api_catalogs[0].catalog_id)
        self.assertEqual(catalog_scope[0].public_price,
                         _get_price_string(api_public_catalog_scope[0].price))
        self.assertEqual(catalog_scope[0].private_price,
                         _get_price_string(api_private_catalog_scope[0].price))
        self.assertEqual(catalog_scope[1].catalog_id,
                         api_catalogs[1].catalog_id)
        self.assertEqual(catalog_scope[1].public_price,
                         _get_price_string(api_public_catalog_scope[1].price))
        self.assertEqual(catalog_scope[1].private_price, '-')
        self.assertEqual(catalog_scope[2].catalog_id,
                         api_catalogs[2].catalog_id)
        self.assertEqual(catalog_scope[2].public_price, '-')
        self.assertEqual(catalog_scope[2].private_price,
                         _get_price_string(api_private_catalog_scope[1].price))
        self.assertEqual(catalog_scope[3].catalog_id,
                         api_catalogs[3].catalog_id)
        self.assertEqual(catalog_scope[3].public_price,
                         _get_price_string(api_public_catalog_scope[2].price))
        self.assertEqual(catalog_scope[3].private_price,
                         _get_price_string(api_private_catalog_scope[2].price))
        self.assertEqual(catalog_scope[4].catalog_id,
                         api_catalogs[4].catalog_id)
        self.assertEqual(catalog_scope[4].public_price, '-')
        self.assertEqual(catalog_scope[4].private_price, '-')
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_catalog_scope_list_no_catalog(self):
        """Test to get public data and private data.
        Test the operation of catalog data without.
        """
        # Get catalog data
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        kwargs_cata = {'limit': limit,
                       'sort_dir': None,
                       'sort_key': None}

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs_cata) \
            .AndReturn([])

        # Get public catalog scope data
        api_public_catalog_scope = []
        for data in catalogs_fixture.VALID_PUBLIC_DATA_LIST[:6]:
            api_public_catalog_scope.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        kwargs_public = {'limit': limit,
                         'sort_dir': 'asc',
                         'sort_key': 'catalog_id',
                         'scope': 'Default',
                         'lifetime': lifetime,
                         'refine_flg': True}

        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs_public) \
            .AndReturn(iter(api_public_catalog_scope))

        # Get private catalog scope data
        api_private_catalog_scope = []
        for data in catalogs_fixture.VALID_PRIVATE_DATA_LIST[:3]:
            api_private_catalog_scope.append(
                ValidCatalog(self, data, loaded=True))

        kwargs_public = {'limit': limit,
                         'sort_dir': 'asc',
                         'sort_key': 'catalog_id',
                         'scope': '5a53a6a5aab54293884b96e3cb1b1754',
                         'lifetime': lifetime,
                         'refine_flg': True}

        afloclient.valid_catalog.list(kwargs_public) \
            .AndReturn(iter(api_private_catalog_scope))

        self.mox.ReplayAll()

        catalog_scope, has_prev, has_more = api.ticket.catalog_scope_list(
            self.request,
            catalogs_fixture.PROJECT_ID)
        self.assertEqual(catalog_scope, [])
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',),
                        horizon.messages: ('horizon_message_already_queued',)})
    def test_catalog_scope_list_exception(self):
        """Test to get public data and private data.
        Test the operation of exception has occurred.
        """
        # Get catalog data
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_DATA_LIST[:5]:
            api_catalogs.append(
                Catalog(self, data, loaded=True))

        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        kwargs_cata = {'limit': limit,
                       'sort_dir': None,
                       'sort_key': None}

        afloclient = self.stub_afloclient()
        afloclient.catalogs = self.mox.CreateMockAnything()
        afloclient.catalogs.list(kwargs_cata) \
            .AndReturn(iter(api_catalogs))

        # Get public catalog scope data
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        horizon.messages.horizon_message_already_queued(
            self.request, 'Unable to retrieve catalog scope list.').AndReturn(
                True)

        kwargs_public = {'limit': limit,
                         'sort_dir': 'asc',
                         'sort_key': 'catalog_id',
                         'scope': 'Default',
                         'lifetime': lifetime,
                         'refine_flg': True}

        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs_public)  \
            .AndRaise(OSError)

        self.mox.ReplayAll()

        catalog_scope, has_prev, has_more = api.ticket.catalog_scope_list(
            self.request,
            catalogs_fixture.PROJECT_ID)
        self.assertEqual(catalog_scope, [])
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_valid_catalog_list_no_pagination(self):
        """Test to get valid catalog data.
        Test the operation of none pagination.
        """
        api_catalogs = []
        for data in catalogs_fixture.VALID_DATA_LIST:
            api_catalogs.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'asc',
                  'sort_key': 'catalog_id',
                  'scope': scope,
                  'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.valid_catalog_list(
            self.request)
        self.assertItemsEqual(catalogs, api_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_valid_catalog_list_filters(self):
        """Test to get valid catalog data.
        Test with all parameters.
        """
        api_catalogs = []
        for data in catalogs_fixture.VALID_DATA_LIST:
            api_catalogs.append(
                ValidCatalog(self, data, loaded=True))

        kwargs = {'limit': 2,
                  'sort_dir': 'desc',
                  'sort_key': 'scope',
                  'scope': 'Default',
                  'lifetime': '2015-08-01T12:30:45.000000',
                  'catalog_id': '100',
                  'refine_flg': True,
                  'catalog_marker': '100',
                  'catalog_scope_marker': 'scope_id0-111-222-333-001',
                  'price_marker': '2'}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.valid_catalog_list(
            self.request,
            catalog_id='100',
            scope='Default',
            refine_flg=True,
            lifetime='2015-08-01T12:30:45.000000',
            marker='100|scope_id0-111-222-333-001|2',
            limit=2,
            sort_key='scope',
            sort_dir='desc')
        self.assertItemsEqual(catalogs, api_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_valid_catalog_list_pagination_more_page_size(self):
        """Test to get valid catalog data.
        Test the operation of small in page size.
        """
        page_size = settings.API_RESULT_PAGE_SIZE

        api_catalogs = []
        for data in catalogs_fixture.VALID_DATA_LIST:
            api_catalogs.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id',
                  'scope': scope,
                  'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.valid_catalog_list(
            self.request,
            sort_dir='desc',
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertTrue(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_valid_catalog_list_pagination_less_page_size(self):
        """Test to get valid catalog data.
        Test the operation of large in page size.
        """
        page_size = settings.API_RESULT_PAGE_SIZE

        api_catalogs = []
        for data in catalogs_fixture.VALID_DATA_LIST:
            api_catalogs.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id',
                  'scope': scope,
                  'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.valid_catalog_list(
            self.request,
            sort_dir='desc',
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=7)
    def test_valid_catalog_list_pagination_equal_page_size(self):
        """Test to get valid catalog data.
        Test the operation of page size equal data size.
        """
        page_size = settings.API_RESULT_PAGE_SIZE

        api_catalogs = []
        for data in catalogs_fixture.VALID_DATA_LIST:
            api_catalogs.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id',
                  'scope': scope,
                  'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.valid_catalog_list(
            self.request,
            sort_dir='desc',
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)
        self.assertEqual(len(expected_catalogs), len(catalogs))

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_valid_catalog_list_pagination_marker(self):
        """Test to get valid catalog data.
        Tests getting a second page with a marker.
        """
        api_catalogs = []
        for data in catalogs_fixture.VALID_DATA_LIST:
            api_catalogs.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id',
                  'scope': scope,
                  'lifetime': lifetime,
                  'catalog_marker': '300',
                  'catalog_scope_marker': 'scope_id0-111-222-333-001',
                  'price_marker': '2'}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.valid_catalog_list(
            self.request,
            sort_dir='desc',
            marker='300|scope_id0-111-222-333-001|2',
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_valid_catalog_list_pagination_marker_prev(self):
        """Test to get valid catalog data.
        Tests getting previous page with a marker.
        """
        api_catalogs = []
        for data in catalogs_fixture.VALID_DATA_LIST:
            api_catalogs.append(
                ValidCatalog(self, data, loaded=True))

        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'asc',
                  'sort_key': 'catalog_id',
                  'scope': scope,
                  'lifetime': lifetime,
                  'catalog_marker': '300',
                  'catalog_scope_marker': 'scope_id0-111-222-333-001',
                  'price_marker': '2'}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.valid_catalog_list(
            self.request,
            sort_dir='asc',
            marker='300|scope_id0-111-222-333-001|2',
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_valid_catalog_list_exception(self):
        """Test to get valid catalog data.
        Test the operation of exception has occurred.
        """
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id',
                  'scope': scope,
                  'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.valid_catalog = self.mox.CreateMockAnything()
        afloclient.valid_catalog.list(kwargs) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.valid_catalog_list,
                          self.request,
                          sort_dir='desc')

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_catalog_scope_update_or_create(self):
        """Test to update or create catalog scope data.
        Test the operation of standard.
        """
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        api_catalogs = CatalogScope(
            self,
            catalogs_fixture.CATALOG_SCOPE_DATA_LIST[0],
            loaded=True)

        catalog_id = '100'
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id,
                  'scope': scope,
                  'lifetime': lifetime}

        field = {'price': '200',
                 'lifetime_start': lifetime,
                 'lifetime_end': '9999-12-31T23:59:59.999999'}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter([api_catalogs]))

        afloclient.catalog_scope.update(
            api_catalogs.id,
            {'lifetime_end': "2015-08-01T12:30:44.000000"}) \
            .AndReturn(api_catalogs)

        afloclient.catalog_scope.create(catalog_id, scope, field) \
            .AndReturn(api_catalogs)

        self.mox.ReplayAll()

        catalogs = api.ticket.catalog_scope_update_or_create(
            self.request,
            catalog_id=catalog_id,
            scope=scope,
            fields={'price': '200'})
        self.assertEqual(catalogs, api_catalogs)

    def test_catalog_scope_update_or_create_filters(self):
        """Test to update or create catalog scope data.
        Test with all parameters.
        """
        api_catalogs = CatalogScope(
            self,
            catalogs_fixture.CATALOG_SCOPE_DATA_LIST[0],
            loaded=True)

        catalog_id = '100'
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        lifetime = '2015-11-01T12:30:45.000000'

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id,
                  'scope': scope,
                  'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter([api_catalogs]))

        afloclient.catalog_scope.update(
            api_catalogs.id,
            {'lifetime_end': "2015-11-01T12:30:44.000000"}) \
            .AndReturn(api_catalogs)

        self.mox.ReplayAll()

        catalogs = api.ticket.catalog_scope_update_or_create(
            self.request,
            catalog_id=catalog_id,
            scope=scope,
            fields={'price': '200'},
            now='2015-11-01T12:30:45.000000',
            del_flg=True)
        self.assertEqual(catalogs, {})

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_catalog_scope_update_or_create_no_data(self):
        """Test to update or create catalog scope data.
        Test the operation of update data without.
        """
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        api_catalogs = CatalogScope(
            self,
            catalogs_fixture.CATALOG_SCOPE_DATA_LIST[0],
            loaded=True)

        catalog_id = '100'
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id,
                  'scope': scope,
                  'lifetime': lifetime}

        field = {'price': '200',
                 'lifetime_start': lifetime,
                 'lifetime_end': '9999-12-31T23:59:59.999999'}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn([])

        afloclient.catalog_scope.create(catalog_id, scope, field) \
            .AndReturn(api_catalogs)

        self.mox.ReplayAll()

        catalogs = api.ticket.catalog_scope_update_or_create(
            self.request,
            catalog_id=catalog_id,
            scope=scope,
            fields={'price': '200'})
        self.assertEqual(catalogs, api_catalogs)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_catalog_scope_update_or_create_exception(self):
        """Test to update or create catalog scope data.
        Test the operation of exception has occurred.
        """
        lifetime = api.ticket.get_datetime_now(). \
            AndReturn("2015-08-01T12:30:45.000000")

        catalog_id = '100'
        scope = 'Default'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id,
                  'scope': scope,
                  'lifetime': lifetime}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.catalog_scope_update_or_create,
                          self.request,
                          catalog_id=catalog_id,
                          scope=scope,
                          fields={'price': '200'})

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_scope_list_detailed_no_pagination(self):
        """Test to get catalog scope data.
        Test the operation of none pagination.
        """
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_SCOPE_DATA_LIST:
            api_catalogs.append(
                CatalogScope(self, data, loaded=True))

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_scope_list_detailed(
            self.request,
            catalog_id)
        self.assertItemsEqual(catalogs, api_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_scope_list_detailed_filters(self):
        """Test to get catalog scope data.
        Test with all parameters.
        """
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_SCOPE_DATA_LIST:
            api_catalogs.append(
                CatalogScope(self, data, loaded=True))

        catalog_id = '100'

        kwargs = {'limit': 2,
                  'sort_dir': 'asc',
                  'sort_key': 'id',
                  'catalog_id': catalog_id,
                  'scope': 'Default',
                  'lifetime': '2015-08-01T12:30:45.000000',
                  'marker': 'scope_id0-111-222-333-001'
                  }

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter(api_catalogs))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_scope_list_detailed(
            self.request,
            catalog_id='100',
            scope='Default',
            lifetime='2015-08-01T12:30:45.000000',
            marker='scope_id0-111-222-333-001',
            limit=2,
            sort_key='id',
            sort_dir='asc')
        self.assertItemsEqual(catalogs, api_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_scope_list_detailed_pagination_more_page_size(self):
        """Test to get catalog scope data.
        Test the operation of small in page size.
        """
        page_size = settings.API_RESULT_PAGE_SIZE

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_SCOPE_DATA_LIST:
            api_catalogs.append(
                CatalogScope(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter(catalogs_iter))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_scope_list_detailed(
            self.request,
            catalog_id,
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertTrue(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_catalog_scope_list_detailed_pagination_less_page_size(self):
        """Test to get catalog scope data.
        Test the operation of large in page size.
        """
        page_size = settings.API_RESULT_PAGE_SIZE

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_SCOPE_DATA_LIST:
            api_catalogs.append(
                CatalogScope(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter(catalogs_iter))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_scope_list_detailed(
            self.request,
            catalog_id,
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=6)
    def test_catalog_scope_list_detailed_pagination_equal_page_size(self):
        """Test to get catalog scope data.
        Test the operation of large in page size.
        """
        page_size = settings.API_RESULT_PAGE_SIZE

        api_catalogs = []
        for data in catalogs_fixture.CATALOG_SCOPE_DATA_LIST:
            api_catalogs.append(
                CatalogScope(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter(catalogs_iter))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_scope_list_detailed(
            self.request,
            catalog_id,
            paginate=True)
        expected_catalogs = api_catalogs[:page_size]
        self.assertItemsEqual(catalogs, expected_catalogs)
        self.assertFalse(has_more)
        self.assertFalse(has_prev)
        self.assertEqual(len(expected_catalogs), len(catalogs))

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_scope_list_detailed_pagination_marker(self):
        """Test to get catalog scope data.
        Tests getting a second page with a marker.
        """
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_SCOPE_DATA_LIST:
            api_catalogs.append(
                CatalogScope(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = 'scope_id0-111-222-333-004'

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id,
                  'marker': marker}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter(catalogs_iter))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_scope_list_detailed(
            self.request,
            catalog_id,
            marker=marker,
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    def test_catalog_scope_list_detailed_pagination_marker_prev(self):
        """Test to get catalog scope data.
        Tests getting previous page with a marker.
        """
        api_catalogs = []
        for data in catalogs_fixture.CATALOG_SCOPE_DATA_LIST:
            api_catalogs.append(
                CatalogScope(self, data, loaded=True))
        catalogs_iter = iter(api_catalogs)

        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
        marker = 'scope_id0-111-222-333-004'

        kwargs = {'limit': limit,
                  'sort_dir': 'asc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id,
                  'marker': marker}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndReturn(iter(catalogs_iter))
        self.mox.ReplayAll()

        catalogs, has_prev, has_more = api.ticket.catalog_scope_list_detailed(
            self.request,
            catalog_id,
            marker=marker,
            sort_dir='asc',
            paginate=True)
        self.assertTrue(has_more)
        self.assertTrue(has_prev)

    @test.create_stubs({api.ticket: ('get_datetime_now',)})
    def test_catalog_scope_list_detailed_exception(self):
        """Test to get catalog scope data.
        Test the operation of exception has occurred.
        """
        catalog_id = '100'
        limit = getattr(settings, 'API_RESULT_LIMIT', 1000)

        kwargs = {'limit': limit,
                  'sort_dir': 'desc',
                  'sort_key': 'lifetime_start',
                  'catalog_id': catalog_id}

        afloclient = self.stub_afloclient()
        afloclient.catalog_scope = self.mox.CreateMockAnything()
        afloclient.catalog_scope.list(kwargs) \
            .AndRaise(OSError)
        self.mox.ReplayAll()

        self.assertRaises(OSError,
                          api.ticket.catalog_scope_list_detailed,
                          self.request,
                          catalog_id)


class Catalog(object):
    """Catalog resource."""

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
        """String of catalog object."""
        return "<Catalog %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass


class Price(object):
    """Price resource."""

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
        """String of price object."""
        return "<Price %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass


class CatalogScope(object):
    """Represents a catalog scope."""

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

        return "<Catalog Scope %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass


class ValidCatalog(object):
    """Represents a valid catalog."""

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
        return "<Valid Catalog %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass


def _get_price_string(value):
    """Get Price string from value.
    :Param value: price string
    """
    try:
        return CURRENCY_FORMAT.format(Decimal(value))
    except (TypeError, decimal.InvalidOperation):
        return value


class ProjectCatalog(object):
    """Project Catalog Class"""
    def __init__(self,
                 catalog_id,
                 scope,
                 seq_no,
                 catalog_name,
                 price,
                 project_id):

        self.catalog_id = escape(catalog_id)
        self.scope = escape(scope)
        self.seq_no = escape(seq_no)
        self.catalog_name = escape(catalog_name)
        self.price = _get_price_string(escape(price))
        self.project_id = escape(project_id)


def _get_datetime_utcnow():
    utcnow = datetime.datetime.utcnow()
    return utcnow.strftime('%Y-%m-%dT%H:%M:%S.%f')
