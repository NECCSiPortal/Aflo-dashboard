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
from horizon import forms
from horizon import messages

from nec_portal.api import ticket
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import forms as base_forms

LOG = logging.getLogger(__name__)


class UpdateForm(base_forms.BaseForm):
    class Meta(object):
        name = _('Update Ticket')

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)

        # Create move to next status of workflow input item
        approval_flg = forms.ChoiceField(label=_('Confirmation'),
                                         widget=forms.RadioSelect)
        available_next_status = \
            kwargs['initial'].get('available_next_status')
        approval_flg.choices = available_next_status

        if len(available_next_status) != 0:
            approval_flg.initial = available_next_status[0][0]

        self.fields['approval_flg'] = approval_flg

    def handle(self, request, data):
        selected_status = self._get_selected_status_information(
            data['approval_flg'])
        url_kwargs_list = self._get_url_kwargs_fields(data)
        params_list = self._get_params_list(data)

        ticket_data = {
            'additional_data': json.dumps(params_list),
        }
        # Set 'from status' and 'to status' information
        ticket_data.update(selected_status)

        try:
            LOG.info(ticket_data)
            ticket.ticket_update(self.request, url_kwargs_list['ticket_id'],
                                 ticket_data)

            message = _('Successfully updated request."')
            messages.success(request, message)

        except Exception as e:
            LOG.error(e)

            exceptions.handle(
                request, _('An error occurred while processing your request.'))
            raise

        return True
