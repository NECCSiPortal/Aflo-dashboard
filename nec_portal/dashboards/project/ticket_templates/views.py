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

from nec_portal.dashboards.project.ticket_templates \
    import tabs as tickettemplates_tabs


class IndexView(tabs.TabbedTableView):
    """Index view class"""

    tab_group_class = tickettemplates_tabs.TicketTemplatesGroupTabs
    template_name = 'project/ticket_templates/index.html'
    page_title = _("Request Menu")
