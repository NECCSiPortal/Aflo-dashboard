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

# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'request'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'admin'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'request'

# Python panel class of the PANEL to be added.
ADD_PANEL = \
    'nec_portal.dashboards.admin.ticket_list.panel.TicketListPanel'

# A list of scss files to be included in the compressed set of files
ADD_SCSS_FILES = ['nec_portal/aflo/aflo.scss']

# Automatically discover static resources in installed apps
AUTO_DISCOVER_STATIC_FILES = True

# A list of js files to be included in the compressed set of files
ADD_JS_FILES = ['nec_portal/aflo/wf_engine_confirm.js',
                'nec_portal/aflo/wf_engine_datepicker.js']
