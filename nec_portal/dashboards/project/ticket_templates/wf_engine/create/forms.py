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


class CreateForm(base_forms.BaseForm):
    first_status_code = forms.CharField(widget=forms.HiddenInput())

    class Meta(object):
        name = _('Create Ticket')

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)

    def handle(self, request, data):
        url_kwargs_list = self._get_url_kwargs_fields(data)
        params_list = self._get_params_list(data)
        for key, value in url_kwargs_list.items():
            if key != 'ticket_template_id':
                params_list[key] = value

        ticket_data = {
            'status_code': data.get('first_status_code', ''),
            'ticket_detail': json.dumps(params_list),
            'ticket_template_id': url_kwargs_list['ticket_template_id'],
        }

        try:
            LOG.info(ticket_data)
            ticket.ticket_create(self.request, ticket_data)

            messages.success(
                request,
                _('Successfully registration request.'))

        except Exception as e:
            LOG.error(e)
            exceptions.handle(
                request,
                _('An error occurred while processing your request.'))
            raise

        return True
