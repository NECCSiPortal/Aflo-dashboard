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

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from nec_portal.dashboards.project.ticket_templates.application_kinds \
    import urls as application_kinds_urls
from nec_portal.dashboards.project.ticket_templates.wf_engine.create \
    import urls as wf_engine_create

from nec_portal.dashboards.project.ticket_templates import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.IndexView.as_view(),
        name='index'),
    url(r'^\?tab=application_kinds_group_tabs__applications_tab$',
        views.IndexView.as_view(),
        name='applications_tab'),
    url(r'',
        include(application_kinds_urls, namespace='application_kinds')),

    url(r'^workflow/(?P<ticket_template_id>[^/]+)/create/$',
        include(wf_engine_create, namespace='wf_engine_create')),
)
