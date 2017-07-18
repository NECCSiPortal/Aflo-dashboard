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

from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from nec_portal.dashboards.project.private_price_lists import \
    constants


class OverviewTab(tabs.Tab):
    """Overview tab class"""
    name = _("Overview")
    slug = "catalog_overview"
    template_name = constants.CATALOG_DETAIL_OVERVIEW_TEMPLATE

    def get_context_data(self, request):
        catalog = self.tab_group.kwargs['catalog']

        return {"catalog": catalog}


class CatalogDetailTabs(tabs.TabGroup):
    """Catalog detail tabs class"""
    slug = "catalog_details"
    tabs = (OverviewTab,)
