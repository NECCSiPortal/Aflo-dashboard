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

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test

from nec_portal import api as ticket_api
from nec_portal.dashboards.admin.private_price_lists import fixture
from nec_portal.dashboards.admin.private_price_lists import panel  # noqa
from nec_portal.dashboards.admin.private_price_lists import tables as i_tables
from nec_portal.dashboards.admin.private_price_lists import views as i_views
from nec_portal.test import aflo_helpers as aflo_test


INDEX_URL = reverse('horizon:admin:private_price_lists:index')
PRIVATE_URL = reverse('horizon:admin:private_price_lists:private',
                      kwargs={"project_id": fixture.PROJECT_ID})
PUBLIC_URL = reverse('horizon:admin:private_price_lists:public')


class CatalogViewTests(aflo_test.BaseAdminViewTests):

    @test.create_stubs({api.keystone: ('tenant_list',)})
    def test_index(self):

        tenant_data = \
            [Project(self, fixture.TENANT_DATA_LIST[0], loaded=True)]

        api.keystone.tenant_list(IsA(http.HttpRequest),
                                 domain=None,
                                 paginate=False) \
            .AndReturn([tenant_data, False])
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/private_price_lists/index.html')
        self.assertEqual(res.status_code, 200)


class PrivateUpdateViewTests(aflo_test.BaseAdminViewTests):

    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog(self):

        catalog_data = \
            [ValidCatalog(self, fixture.CATALOG_PRICE_LIST[0], loaded=True)]

        ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                             fixture.PROJECT_ID,
                                             marker=None,
                                             sort_key='catalog_id',
                                             sort_dir='desc',
                                             filters={},
                                             paginate=True) \
            .AndReturn([catalog_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(PRIVATE_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/private_price_lists/private.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_no_data(self):

        ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                             fixture.PROJECT_ID,
                                             marker=None,
                                             sort_key='catalog_id',
                                             sort_dir='desc',
                                             filters={},
                                             paginate=True) \
            .AndReturn([[], False, False])

        self.mox.ReplayAll()

        res = self.client.get(PRIVATE_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/private_price_lists/private.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({i_views.PrivatePriceViews: ('get_filters',)})
    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_filter_catalog_name(self):

        catalog_name = "CPU 10 pieces S set"

        # Create a filter condition.
        filters = i_views.PrivatePriceViews.get_filters(). \
            AndReturn({"catalog_name": catalog_name})

        catalog_data = \
            [ValidCatalog(self, fixture.CATALOG_PRICE_LIST[0], loaded=True)]

        catalog_list = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters=filters,
                                                 paginate=True) \
            .AndReturn([catalog_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(PRIVATE_URL)

        self.assertEqual(catalog_list[0][0].catalog_name, catalog_name)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/private_price_lists/private.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_get_pagination(self):
        """Test 'List Search of catalogs'
        Next page of paging.
        """

        # Create catalog data list.
        catalog_data_list = []
        for data in fixture.CATALOG_PRICE_LIST:
            catalog_data_list.append(
                ValidCatalog(self, data, loaded=True))

        catalogs = catalog_data_list[:5]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs, True, True])
        rtn_catalog_1 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[:2], True, True])
        rtn_catalog_2 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=catalogs[2].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[2:4], True, True])
        rtn_catalog_3 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=catalogs[4].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[4:], True, True])
        rtn_catalog_4 = rtn_catalog[0]

        self.mox.ReplayAll()
        res = self.client.get(PRIVATE_URL)

        # Get all.
        self.assertEqual(len(rtn_catalog_1),
                         len(catalogs))
        self.assertTemplateUsed(res, 'admin/private_price_lists/private.html')

        self.client.get(PRIVATE_URL)
        # Get first page with 2 items.
        self.assertEqual(len(rtn_catalog_2),
                         settings.API_RESULT_PAGE_SIZE)

        pagination = i_tables.PrivatePriceTable._meta.pagination_param
        params = "=".join([pagination, catalogs[2].catalog_id])
        url = "?".join([PRIVATE_URL, params])
        self.client.get(url)
        # Get second page.(items 2-4)
        self.assertEqual(len(rtn_catalog_3),
                         settings.API_RESULT_PAGE_SIZE)

        params = "=".join([pagination, catalogs[4].catalog_id])
        url = "?".join([PRIVATE_URL, params])
        self.client.get(url)
        # Get third page.(item 5)
        self.assertEqual(len(rtn_catalog_4), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_get_prev_pagination(self):
        """Test 'List Search of catalogs'
        Prev page of paging.
        """

        # Create catalog data list.
        catalog_data_list = []
        for data in fixture.CATALOG_PRICE_LIST:
            catalog_data_list.append(
                ValidCatalog(self, data, loaded=True))

        catalogs = catalog_data_list[:3]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs, True, False])
        rtn_catalog_1 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[:2], True, True])
        rtn_catalog_2 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=catalogs[2].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[2:], True, True])
        rtn_catalog_3 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 fixture.PROJECT_ID,
                                                 marker=catalogs[2].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='asc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[:2], True, True])
        rtn_catalog_4 = rtn_catalog[0]

        self.mox.ReplayAll()
        res = self.client.get(PRIVATE_URL)

        # get all.
        self.assertEqual(len(rtn_catalog_1),
                         len(catalogs))
        self.assertTemplateUsed(res, 'admin/private_price_lists/private.html')

        self.client.get(PRIVATE_URL)
        # get first page with 2 items.
        self.assertEqual(len(rtn_catalog_2),
                         settings.API_RESULT_PAGE_SIZE)

        pagination = i_tables.PrivatePriceTable._meta.pagination_param
        params = "=".join([pagination, catalogs[2].catalog_id])
        url = "?".join([PRIVATE_URL, params])
        self.client.get(url)
        # get second page.(item 3)
        self.assertEqual(len(rtn_catalog_3), 1)

        prev_pagination = \
            i_tables.PrivatePriceTable._meta.prev_pagination_param
        params = "=".join([prev_pagination, catalogs[2].catalog_id])
        url = "?".join([PRIVATE_URL, params])
        self.client.get(url)
        # prev back to get first page with 2 items.
        self.assertEqual(len(rtn_catalog_4),
                         settings.API_RESULT_PAGE_SIZE)


class PublicUpdateViewTests(aflo_test.BaseAdminViewTests):

    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog(self):

        catalog_data = \
            [ValidCatalog(self, fixture.CATALOG_PRICE_LIST[0], loaded=True)]

        ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                             'Default',
                                             marker=None,
                                             sort_key='catalog_id',
                                             sort_dir='desc',
                                             filters={},
                                             paginate=True) \
            .AndReturn([catalog_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(PUBLIC_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/private_price_lists/public.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_no_data(self):

        ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                             'Default',
                                             marker=None,
                                             sort_key='catalog_id',
                                             sort_dir='desc',
                                             filters={},
                                             paginate=True) \
            .AndReturn([[], False, False])

        self.mox.ReplayAll()

        res = self.client.get(PUBLIC_URL)

        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/private_price_lists/public.html')
        self.assertEqual(res.status_code, 200)

    @test.create_stubs({i_views.PublicPriceViews: ('get_filters',)})
    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_filter_catalog_name(self):

        catalog_name = "CPU 10 pieces S set"

        # Create a filter condition.
        filters = i_views.PublicPriceViews.get_filters(). \
            AndReturn({"catalog_name": catalog_name})

        catalog_data = \
            [ValidCatalog(self, fixture.CATALOG_PRICE_LIST[0], loaded=True)]

        catalog_list = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters=filters,
                                                 paginate=True) \
            .AndReturn([catalog_data, False, False])

        self.mox.ReplayAll()

        res = self.client.get(PUBLIC_URL)

        self.assertEqual(catalog_list[0][0].catalog_name, catalog_name)
        self.assertNoFormErrors(res)
        self.assertTemplateUsed(res, 'admin/private_price_lists/public.html')
        self.assertEqual(res.status_code, 200)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_get_pagination(self):
        """Test 'List Search of catalogs'
        Next page of paging.
        """

        # Create catalog data list.
        catalog_data_list = []
        for data in fixture.CATALOG_PRICE_LIST:
            catalog_data_list.append(
                ValidCatalog(self, data, loaded=True))

        catalogs = catalog_data_list[:5]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs, True, True])
        rtn_catalog_1 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[:2], True, True])
        rtn_catalog_2 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=catalogs[2].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[2:4], True, True])
        rtn_catalog_3 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=catalogs[4].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[4:], True, True])
        rtn_catalog_4 = rtn_catalog[0]

        self.mox.ReplayAll()
        res = self.client.get(PUBLIC_URL)

        # Get all.
        self.assertEqual(len(rtn_catalog_1),
                         len(catalogs))
        self.assertTemplateUsed(res, 'admin/private_price_lists/public.html')

        self.client.get(PUBLIC_URL)
        # Get first page with 2 items.
        self.assertEqual(len(rtn_catalog_2),
                         settings.API_RESULT_PAGE_SIZE)

        pagination = i_tables.PublicPriceTable._meta.pagination_param
        params = "=".join([pagination, catalogs[2].catalog_id])
        url = "?".join([PUBLIC_URL, params])
        self.client.get(url)
        # Get second page.(items 2-4)
        self.assertEqual(len(rtn_catalog_3),
                         settings.API_RESULT_PAGE_SIZE)

        params = "=".join([pagination, catalogs[4].catalog_id])
        url = "?".join([PUBLIC_URL, params])
        self.client.get(url)
        # Get third page.(item 5)
        self.assertEqual(len(rtn_catalog_4), 1)

    @override_settings(API_RESULT_PAGE_SIZE=2)
    @test.create_stubs({ticket_api.ticket: ('catalog_scope_list',)})
    def test_catalog_get_prev_pagination(self):
        """Test 'List Search of catalogs'
        Prev page of paging.
        """

        # Create catalog data list.
        catalog_data_list = []
        for data in fixture.CATALOG_PRICE_LIST:
            catalog_data_list.append(
                ValidCatalog(self, data, loaded=True))

        catalogs = catalog_data_list[:3]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs, True, False])
        rtn_catalog_1 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=None,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[:2], True, True])
        rtn_catalog_2 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=catalogs[2].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='desc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[2:], True, True])
        rtn_catalog_3 = rtn_catalog[0]

        rtn_catalog = \
            ticket_api.ticket.catalog_scope_list(IsA(http.HttpRequest),
                                                 'Default',
                                                 marker=catalogs[2].catalog_id,
                                                 sort_key='catalog_id',
                                                 sort_dir='asc',
                                                 filters={},
                                                 paginate=True) \
            .AndReturn([catalogs[:2], True, True])
        rtn_catalog_4 = rtn_catalog[0]

        self.mox.ReplayAll()
        res = self.client.get(PUBLIC_URL)

        # get all.
        self.assertEqual(len(rtn_catalog_1),
                         len(catalogs))
        self.assertTemplateUsed(res, 'admin/private_price_lists/public.html')

        self.client.get(PUBLIC_URL)
        # get first page with 2 items.
        self.assertEqual(len(rtn_catalog_2),
                         settings.API_RESULT_PAGE_SIZE)

        pagination = i_tables.PublicPriceTable._meta.pagination_param
        params = "=".join([pagination, catalogs[2].catalog_id])
        url = "?".join([PUBLIC_URL, params])
        self.client.get(url)
        # get second page.(item 3)
        self.assertEqual(len(rtn_catalog_3), 1)

        prev_pagination = i_tables.PublicPriceTable._meta.prev_pagination_param
        params = "=".join([prev_pagination, catalogs[2].catalog_id])
        url = "?".join([PUBLIC_URL, params])
        self.client.get(url)
        # prev back to get first page with 2 items.
        self.assertEqual(len(rtn_catalog_4),
                         settings.API_RESULT_PAGE_SIZE)


class Project(object):
    """Project resource."""

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
        """String of project object.
        """
        return "<Project %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass


class ValidCatalog(object):
    """Valid catalog resource."""

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
        """String of valid catalog object."""
        return "<ValidCatalog %s>" % self._info

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass
