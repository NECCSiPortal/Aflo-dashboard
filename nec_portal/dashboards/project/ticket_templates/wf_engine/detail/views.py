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

import json
import logging

from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.project.ticket_list import utils as ticket_utils
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import constants
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import views as common_views
from nec_portal.dashboards.project.ticket_templates.wf_engine.detail \
    import tabs as detail_tabs
from nec_portal.dashboards.project.ticket_templates.wf_engine.update \
    import views as update_views

LOG = logging.getLogger(__name__)


class DetailView(tabs.TabView,
                 common_views.CallPluginMixin,
                 update_views.GetInputedValueMixin):
    """Detail view engine.
    When you display a detail from a new menu,
    it is necessary to make views.py class and inherits to this class.
    And make the urls.py and include to parent-urls.py to it.
    The class in inherits to this class perform overriding of a later property.
    Method 'get_redirect_url': return redirect url(must override)
    """
    tab_group_class = detail_tabs.DetailTabs
    template_name = 'project/ticket_templates/wf_engine/detail/detail.html'
    page_title = None

    def get_context_data(self, **kwargs):
        # Get a detail from key information from request.
        context = super(DetailView, self).get_context_data(**kwargs)

        ticket_id = self.kwargs['ticket_id']
        detail_plugins = {}

        (ticket_data, ticket_template_data) = self._get_data(ticket_id)
        template_contents = ticket_template_data.template_contents

        # Set constant plugins call settings.
        self._set_constant_plugins(detail_plugins)

        request_form = ticket_utils.get_language_name(
            self.request,
            template_contents['application_kinds_name'])

        # Set title
        self.page_title = string_concat(_(template_contents['ticket_type']),
                                        " / ", request_form)  # noqa
        context['action_url'] = self.get_redirect_url()
        context['allowed_submit'] = self._has_available_next_status(
            ticket_data.workflow)

        # Set information block
        context['project_name'] = ticket_data.tenant_name
        context['category'] = _(template_contents['ticket_type'])  # noqa
        context['type'] = ticket_utils.get_language_name(
            self.request,
            template_contents['ticket_template_name'])
        context['request_form'] = request_form
        context['ticket_id'] = ticket_id

        # Set inputed parameter
        #  (created ticket data and updated workflow status)
        context['created_input_list'] = self._get_created_input_list(
            template_contents['create'].get('parameters', []),
            json.loads(ticket_data.ticket_detail))
        context['updated_input_list'] = self._get_updated_input_list(
            template_contents['update'].get('parameters', []),
            ticket_data.workflow)

        # Set plugin data
        context['custom_bottom'] = self._get_plugin_names(detail_plugins,
                                                          'bottom')

        # Set plugins data
        self._call_plugins(context, detail_plugins,
                           template_contents=template_contents,
                           ticket_data=ticket_data)

        return context

    def _get_data(self, ticket_id):
        """Get form view data
        :param ticket_id: get the ticket id
        """
        ticket_data = None
        ticket_template_data = None

        try:
            ticket_data = ticket_api.ticket_get_detailed(
                self.request, ticket_id)

            # Get a tickettemplate context
            ticket_template_data = \
                ticket_api.tickettemplates_get(self.request,
                                               ticket_data.ticket_template_id)
        except Exception as e:
            LOG.error(e)
            exceptions.handle(self.request, _('Unable to get the request.'))
            raise

        return (ticket_data, ticket_template_data)

    def _has_available_next_status(self, ticket_workflow):
        """Have next available status
        :param ticket_workflow: Workflow data of ticket
        """
        # Get last updated workflow data.
        current_workflow_rows = filter(
            lambda workflow:
            workflow['status'] == constants.WORKFLOW_STATUS_CURRENT,
            ticket_workflow)[0]

        # Get valid status to user can move it.
        next_status_list = ticket_utils.get_next_status_list(
            self.request, current_workflow_rows['status_detail'])

        return 0 < len(next_status_list)

    def _set_constant_plugins(self, detail_plugins):
        detail_plugins['custom'] = [{'wf_status_list': 'bottom'}]

    def get_tabs(self, request, *args, **kwargs):
        return self.tab_group_class(request, **kwargs)

    def get_redirect_url(self):
        raise NotImplementedError()
