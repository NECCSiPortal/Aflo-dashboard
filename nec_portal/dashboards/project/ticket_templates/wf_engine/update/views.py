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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import constants
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import views as base_views
from nec_portal.dashboards.project.ticket_templates.wf_engine.update \
    import forms as wf_engine_forms

LOG = logging.getLogger(__name__)


class GetInputedValueMixin(object):
    """This class provides created/updated input value"""

    def _get_created_input_list(self,
                                create_parameters,
                                ticket_detail):
        """Get the ticket created input data
        :param create_parameters: Create ticket parameters context
        :param ticket_detail: Ticket created input data
        """
        data = []

        for param in create_parameters:
            if param['type'] == 'hidden' or param['key'] == 'message':
                continue
            value = ticket_detail.get(param['key'])

            row = {}
            row['key'] = param['key']
            row['name'] = ticket_utils.get_language_name(
                self.request, param['label'])
            if param['type'] != 'date':
                row['value'] = value
            else:
                row['value'] = ticket_utils.get_localize_display_date(
                    self.request, value)

            data.append(row)

        return data

    def _get_updated_input_list(self,
                                update_parameters,
                                ticket_workflow):
        """Get the ticket updated input data
        :param update_parameters: Update ticket parameters context
        :param ticket_workflow: Workflow status at ticket updated
        """
        data = []

        sort_workflow = \
            ticket_utils.sort_ticket_workflow_by_confirmed_at(ticket_workflow)

        for idx, workflow in enumerate(sort_workflow):
            parameters = filter(
                lambda param:
                (param.get('status', workflow['status_code']) ==
                 workflow['status_code']) & (param['type'] != 'hidden' and
                                             param['key'] != 'message'),
                update_parameters)
            if not (parameters):
                continue

            row = {}

            # Set status name for title
            row['status_name'] = ticket_utils.get_language_name(
                self.request,
                workflow['status_detail']['status_name'])
            row['input_list'] = []

            # No input data by current status
            if workflow['status'] == constants.WORKFLOW_STATUS_CURRENT:
                continue
            additional_data = sort_workflow[idx + 1].get('additional_data', '')
            input_value_data = json.loads(additional_data) \
                if additional_data else {}

            for param in parameters:
                value = input_value_data.get(param['key'], '')

                input_list = {}
                input_list['name'] = ticket_utils.get_language_name(
                    self.request, param['label'])
                if param['type'] != 'date':
                    input_list['value'] = value
                else:
                    input_list['value'] = \
                        ticket_utils.get_localize_display_date(
                            self.request, value)

                row['input_list'].append(input_list)

            data.append(row)

        return data


class UpdateView(base_views.BaseView, GetInputedValueMixin):
    """Update view engine.
    When you display an update from a new menu,
    it is necessary to make views.py class and inherits to this class.
    And make the urls.py and include to parent-urls.py to it.
    The class in inherits to this class perform overriding of a later property.
    Property 'success_url_viewname': Move to urls-viewname
        (see django-urls-reverse) when succeeded in processing
    """
    form_id = 'update_form'
    form_class = wf_engine_forms.UpdateForm
    template_name = 'project/ticket_templates/wf_engine/update/update.html'
    success_url = None
    success_url_viewname = None
    submit_url = None
    ticket_id = None
    ticket_data = None
    available_next_status = None

    def get_initial(self):
        initial = self._create_initial()

        self.ticket_id = self.kwargs['ticket_id']
        try:
            self.ticket_data = ticket_api.ticket_get_detailed(
                self.request,
                self.ticket_id)

            self.kwargs['ticket_template_id'] = \
                self.ticket_data.ticket_template_id
            self.available_next_status = self._get_available_next_status(
                self.ticket_data.workflow)
        except Exception as e:
            LOG.error(e)
            exceptions.handle(self.request, ('Unable to get the request.'))
            raise

        super(UpdateView, self).get_initial()

        form_template = self.template_contents['update']

        self.submit_url = self.get_submit_url(self.request)

        initial['current_status'] = self._get_current_status(
            self.ticket_data.workflow)
        initial['parameters'] = form_template['parameters']
        initial['available_next_status'] = self.available_next_status

        return initial

    def get_context_data(self, **kwargs):
        # Get a update from key information from request.
        allowed_submit = True

        form_template = self.template_contents['update']

        # Set constant plugins call settings.
        self._set_constant_plugins(form_template)

        if self.available_next_status is None or \
                len(self.available_next_status) == 0:
            allowed_submit = False

        context = super(UpdateView, self).get_context_data(**kwargs)

        # Set base context for form
        context['title'] = _(self.template_contents['ticket_type'])  # noqa
        context['sub_title'] = ticket_utils.get_language_name(
            self.request,
            self.template_contents['application_kinds_name'])
        context['description'] = ticket_utils.get_language_name(
            self.request,
            form_template.get('description', {'default': ''}))

        # Set inputed parameter
        #  (created ticket data and updated workflow status)
        context['created_input_list'] = self._get_created_input_list(
            self.template_contents['create'].get('parameters', []),
            json.loads(self.ticket_data.ticket_detail))
        context['updated_input_list'] = self._get_updated_input_list(
            self.template_contents['update'].get('parameters', []),
            self.ticket_data.workflow)

        # Set input parameter values and call plugin names for the html
        context['parameters'] = form_template['parameters']
        context['custom_left'] = self._get_plugin_names(form_template,
                                                        'left')
        context['custom_right'] = self._get_plugin_names(form_template,
                                                         'right')
        context['custom_bottom'] = self._get_plugin_names(form_template,
                                                          'bottom')

        context['allowed_submit'] = allowed_submit

        # Set plugins data
        self._call_plugins(context, form_template,
                           template_contents=self.template_contents,
                           ticket_data=self.ticket_data)

        return context

    def _set_constant_plugins(self, form_template):
        if not('custom' in form_template):
            form_template['custom'] = []
        form_template['custom'].insert(0, {'project_info': 'left'})
        form_template['custom'].insert(0, {'wf_status_list': 'bottom'})

    def _get_available_next_status(self, ticket_workflow):
        """Get next available status list of select form
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

        available_next_status = []
        for next_status in next_status_list:
            status_info = filter(lambda workflow:
                                 workflow['status_code'] ==
                                 next_status.get('next_status_code'),
                                 ticket_workflow)
            status_name = ticket_utils.get_language_name(
                self.request,
                status_info[0]['status_detail'].get('status_name'))
            available_next_status.append(
                ('%s:%s:%s:%s' %
                 (next_status.get('next_status_code'),
                  status_info[0]['id'],
                  current_workflow_rows['status_code'],
                  current_workflow_rows['id']),
                 status_name))

        return available_next_status

    def _get_current_status(self, ticket_workflow):
        """Get current status code
        :param ticket_workflow: Workflow data of ticket
        """
        # Get last updated workflow data.
        return filter(
            lambda workflow:
            workflow['status'] == constants.WORKFLOW_STATUS_CURRENT,
            ticket_workflow)[0].get('status_code', None)
