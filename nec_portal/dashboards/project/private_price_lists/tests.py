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

from nec_portal.api import ticket
from nec_portal.dashboards.project.private_price_lists import fixture
from nec_portal.dashboards.project.private_price_lists import panel  # noqa
from nec_portal.dashboards.project.private_price_lists import tables \
    as i_tables
from nec_portal.dashboards.project.private_price_lists import views as i_views
from nec_portal.test import aflo_helpers as aflo_test

object_id = fixture.CATALOG_ID + '|scope_id0-111-222-333-001|2'
CATALOG_INDEX_URL = reverse('horizon:project:private_price_lists:index')
CATALOG_DETAIL_URL = \
    reverse('horizon:project:private_price_lists:detail',
            kwargs={"catalog_id": object_id})


class CatalogViewTest(aflo_test.TestCase):
    """Catalogs view test class"""

    @test.create_stubs({i_views.IndexView: ('get_filters',)})
    @test.create_stubs({ticket: ('valid_catalog_list',)})
    def test_catalog_list_one_data(self):
        """Test 'List Search of catalogs' if the retrieved result is of 1.
        This is a test in the case of price information
        can be multiple acquisition.
        """

        # Create a filter condition.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        catalog_data = \
            [Catalog(self, fixture.VALID_DATA_LIST[0], loaded=True)]

        # Search for catalogs.
        ticket.valid_catalog_list(IsA(http.HttpRequest),
                                  scope='1',
                                  refine_flg=False,
                                  marker=None,
                                  paginate=True,
                                  filters=filters,
                                  sort_dir='desc') \
            .AndReturn([catalog_data, False, False])

        self.mox.ReplayAll()
        res = self.client.get(CATALOG_INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/private_price_lists/index.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({i_views.IndexView: ('get_filters',)})
    @test.create_stubs({ticket: ('valid_catalog_list',)})
    def test_catalog_list_no_data(self):
        """Test 'List Search of catalogs' if the retrieved result is of 1.
        This is a test in the case of price information
        can be multiple acquisition.
        """

        # Create a filter condition.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        # Search for catalogs.
        ticket.valid_catalog_list(IsA(http.HttpRequest),
                                  scope='1',
                                  refine_flg=False,
                                  marker=None,
                                  paginate=True,
                                  filters=filters,
                                  sort_dir='desc') \
            .AndReturn([[], False, False])

        self.mox.ReplayAll()
        res = self.client.get(CATALOG_INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/private_price_lists/index.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({i_views.IndexView: ('get_filters',)})
    @test.create_stubs({ticket: ('valid_catalog_list',)})
    def test_catalog_list_multiple_catalog_data(self):
        """Test 'List Search of catalogs' if the retrieved result is of 3.
        """

        # Create a filter condition.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        catalog_data = []
        for data in fixture.VALID_DATA_LIST[:3]:
            catalog_data.append(Catalog(self, data, loaded=True))

        # Search for catalogs.
        ticket.valid_catalog_list(IsA(http.HttpRequest),
                                  scope='1',
                                  refine_flg=False,
                                  marker=None,
                                  paginate=True,
                                  filters=filters,
                                  sort_dir='desc') \
            .AndReturn([catalog_data, False, False])

        self.mox.ReplayAll()
        res = self.client.get(CATALOG_INDEX_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/private_price_lists/index.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({i_views.IndexView: ('get_filters',)})
    @test.create_stubs({ticket: ('valid_catalog_list',)})
    def test_catalog_list_get_pagination(self):
        """Test 'List Search of catalogs'.
        Next page of paging.
        """

        # Create catalog data list.
        catalog_data_list = []
        for data in fixture.VALID_DATA_LIST:
            catalog_data_list.append(
                Catalog(self, data, loaded=True))

        catalogs = catalog_data_list[:5]

        # Search for catalogs.
        # Get all.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_1 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=None,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='desc') \
            .AndReturn([catalogs, False, False])

        # Get first page with 2 items.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_2 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=None,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='desc') \
            .AndReturn([catalogs[:2], True, True])

        # Get second page.(items 2-4)
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_3 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=catalogs[2].catalog_id,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='desc') \
            .AndReturn([catalogs[2:4], True, True])

        # Get third page.(item 5)
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_4 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=catalogs[4].catalog_id,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='desc') \
            .AndReturn([catalogs[4:], True, True])

        # Test execution and verification.
        # Get all.
        self.mox.ReplayAll()
        res = self.client.get(CATALOG_INDEX_URL)

        self.assertEqual(len(res_1[0]), len(catalogs))
        self.assertTemplateUsed(res, 'project/private_price_lists/index.html')

        # Get first page with 2 items.
        self.client.get(CATALOG_INDEX_URL)

        self.assertEqual(len(res_2[0]), settings.API_RESULT_PAGE_SIZE)

        # Get second page.(items 2-4)
        pagination = i_tables.CatalogsTable._meta.pagination_param
        params = "=".join([pagination, catalogs[2].catalog_id])
        url = "?".join([CATALOG_INDEX_URL, params])
        self.client.get(url)

        self.assertEqual(len(res_3[0]), settings.API_RESULT_PAGE_SIZE)

        # Get third page.(item 5)
        params = "=".join([pagination, catalogs[4].catalog_id])
        url = "?".join([CATALOG_INDEX_URL, params])
        self.client.get(url)

        self.assertEqual(len(res_4[0]), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({i_views.IndexView: ('get_filters',)})
    @test.create_stubs({ticket: ('valid_catalog_list',)})
    def test_catalog_list_get_prev_pagination(self):
        """Test 'List Search of catalogs'.
        Prev page of paging.
        """

        # Create catalog data list.
        catalog_data_list = []
        for data in fixture.VALID_DATA_LIST:
            catalog_data_list.append(
                Catalog(self, data, loaded=True))

        catalogs = catalog_data_list[:3]

        # Search for catalogs.
        # Get all.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_1 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=None,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='desc') \
            .AndReturn([catalogs, True, False])

        # Get first page with 2 items.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_2 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=None,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='desc') \
            .AndReturn([catalogs[:2], True, True])

        # Get second page.(item 3)
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_3 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=catalogs[2].catalog_id,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='desc') \
            .AndReturn([catalogs[2:], True, True])

        # Prev back to get first page with 2 items.
        filters = i_views.IndexView.get_filters(). \
            AndReturn({'lifetime': '2015-08-02T12:30:45.000000'})

        res_4 = ticket.valid_catalog_list(IsA(http.HttpRequest),
                                          scope='1',
                                          refine_flg=False,
                                          marker=catalogs[2].catalog_id,
                                          paginate=True,
                                          filters=filters,
                                          sort_dir='asc') \
            .AndReturn([catalogs[:2], True, True])

        # Test execution and verification.
        # Get all.
        self.mox.ReplayAll()
        res = self.client.get(CATALOG_INDEX_URL)

        self.assertEqual(len(res_1[0]), len(catalogs))
        self.assertTemplateUsed(res, 'project/private_price_lists/index.html')

        # Get first page with 2 items.
        self.client.get(CATALOG_INDEX_URL)

        self.assertEqual(len(res_2[0]), settings.API_RESULT_PAGE_SIZE)

        # Get second page.(item 3)
        pagination = i_tables.CatalogsTable._meta.pagination_param
        params = "=".join([pagination, catalogs[2].catalog_id])
        url = "?".join([CATALOG_INDEX_URL, params])
        self.client.get(url)

        self.assertEqual(len(res_3[0]), 1)

        # Prev back to get first page with 2 items.
        prev_pagination = i_tables.CatalogsTable._meta.prev_pagination_param
        params = "=".join([prev_pagination, catalogs[2].catalog_id])
        url = "?".join([CATALOG_INDEX_URL, params])
        self.client.get(url)

        self.assertEqual(len(res_4[0]), settings.API_RESULT_PAGE_SIZE)


class CatalogDetailTest(aflo_test.TestCase):
    """Catalog view test class"""

    @test.create_stubs({ticket: ('valid_catalog_list',)})
    @test.create_stubs({ticket: ('catalog_get_detailed',)})
    def test_catalog_detail_multiple_of_price_information(self):
        """Test 'View a catalog detail'"""
        # Create a catalog of return data.
        valid_data = [Catalog(self, fixture.VALID_DATA_LIST[1], loaded=True)]
        catalog_data = Catalog(self, fixture.CATALOG_DATA_LIST[0], loaded=True)

        # Search for catalog.
        ticket.valid_catalog_list(IsA(http.HttpRequest),
                                  scope='1',
                                  refine_flg=False,
                                  filters={'catalog_id': fixture.CATALOG_ID}) \
            .AndReturn([valid_data, False, False])

        ticket.catalog_get_detailed(IsA(http.HttpRequest),
                                    fixture.CATALOG_ID).AndReturn(catalog_data)

        self.mox.ReplayAll()
        res = self.client.get(CATALOG_DETAIL_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/private_price_lists/detail.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({ticket: ('valid_catalog_list',)})
    @test.create_stubs({ticket: ('catalog_get_detailed',)})
    def test_catalog_detail_price_information_default_only(self):
        """Test 'View a catalog detail'"""
        # Create a catalog of return data.
        valid_data = [Catalog(self, fixture.VALID_DATA_LIST[3], loaded=True)]
        catalog_data = Catalog(self, fixture.CATALOG_DATA_LIST[2], loaded=True)

        # Search for catalog.
        ticket.valid_catalog_list(IsA(http.HttpRequest),
                                  scope='1',
                                  refine_flg=False,
                                  filters={'catalog_id': fixture.CATALOG_ID}) \
            .AndReturn([valid_data, False, False])

        ticket.catalog_get_detailed(IsA(http.HttpRequest),
                                    fixture.CATALOG_ID).AndReturn(catalog_data)

        self.mox.ReplayAll()
        res = self.client.get(CATALOG_DETAIL_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/private_price_lists/detail.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({ticket: ('valid_catalog_list',)})
    @test.create_stubs({ticket: ('catalog_get_detailed',)})
    def test_catalog_detail_price_information_project_only(self):
        """Test 'View a catalog detail'."""
        # Create a catalog of return data.
        valid_data = [Catalog(self, fixture.VALID_DATA_LIST[5], loaded=True)]
        catalog_data = Catalog(self, fixture.CATALOG_DATA_LIST[3], loaded=True)

        # Search for catalog.
        ticket.valid_catalog_list(IsA(http.HttpRequest),
                                  scope='1',
                                  refine_flg=False,
                                  filters={'catalog_id': fixture.CATALOG_ID}) \
            .AndReturn([valid_data, False, False])

        ticket.catalog_get_detailed(IsA(http.HttpRequest),
                                    fixture.CATALOG_ID).AndReturn(catalog_data)

        self.mox.ReplayAll()
        res = self.client.get(CATALOG_DETAIL_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'project/private_price_lists/detail.html')
        self.assertEqual(res.status_code, 200)


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
