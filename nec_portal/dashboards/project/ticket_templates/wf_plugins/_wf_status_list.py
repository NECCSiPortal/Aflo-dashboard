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

from django.utils.html import escape

from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import constants
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import plugin as base_plugin


class WfStatusList(base_plugin.BasePlugin):
    """Workflow status list plugin"""

    def set_context_data(
            self, called_object, context, form_template, **kwargs):

        ticket_detail = json.loads(kwargs['ticket_data'].ticket_detail)
        ticket_workflow = kwargs['ticket_data'].workflow
        context['passed_status_messages'] = \
            self._get_passed_status_messages(called_object,
                                             ticket_detail, ticket_workflow)

    def _get_passed_status_messages(self, called_object,
                                    ticket_detail, ticket_workflow):
        """Get updated messages of passed statuses
        :param called_object: pulugin called class
        :param ticket_detail: created input data of ticket
        :param ticket_workflow: workflow data of ticket
        """
        # Get passed workflow data and sort confirmed date.
        passed_workflow_rows = filter(
            lambda row:
            row['status'] != constants.WORKFLOW_STATUS_INITIAL,
            ticket_workflow)
        sort_passed_workflow_rows = sorted(passed_workflow_rows,
                                           key=lambda status:
                                           status.get('confirmed_at'),
                                           reverse=False)
        created_message = ticket_detail.get('message',
                                            ticket_detail.get('Message', ''))
        flg = False
        passed_status_messages = []

        # Get updated messages of passed workflow data.
        for workflow in sort_passed_workflow_rows:
            display_workflow = {}
            display_workflow['user'] = workflow.get('confirmer_name')
            display_workflow['update_date'] = escape(
                ticket_utils.get_localize_display_datetime(
                    called_object.request, workflow.get('confirmed_at')))

            status_detail = workflow.get('status_detail')
            status_detail_name = status_detail.get('status_name')

            display_workflow['status'] = ticket_utils.get_language_name(
                called_object.request, status_detail_name)

            if not flg:
                display_workflow['message'] = created_message
                flg = True
            else:
                additional_data = json.loads(workflow.get('additional_data',
                                                          '{}'))
                display_workflow['message'] = additional_data.get(
                    'message', additional_data.get('Message', ''))

            passed_status_messages.append(display_workflow)

        return passed_status_messages
