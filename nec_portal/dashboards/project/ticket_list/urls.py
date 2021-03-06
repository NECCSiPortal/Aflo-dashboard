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
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from nec_portal.dashboards.project.ticket_list import views
from nec_portal.dashboards.project.ticket_list.wf_engine.detail \
    import urls as wf_engine_detail
from nec_portal.dashboards.project.ticket_list.wf_engine.update \
    import urls as wf_engine_update


url_pattern = 'nec_portal.dashboards.project.ticket_list.views'
urlpatterns = patterns(
    url_pattern,
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^workflow/(?P<ticket_id>[^/]+)/detail/$',
        include(wf_engine_detail, namespace='wf_engine_detail')),
    url(r'^workflow/(?P<ticket_id>[^/]+)/update/$',
        include(wf_engine_update, namespace='wf_engine_update')),
)
