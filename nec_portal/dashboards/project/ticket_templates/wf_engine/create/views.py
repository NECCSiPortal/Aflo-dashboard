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

from django.utils.translation import ugettext_lazy as _

from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils
from nec_portal.dashboards.project.ticket_templates.wf_engine.common import \
    views as base_views
from nec_portal.dashboards.project.ticket_templates.wf_engine.create \
    import forms as wf_engine_forms


class CreateView(base_views.BaseView):
    """Create view engine.
    When you display an create from a new menu,
    it is necessary to make views.py class and inherits to this class.
    And make the urls.py and include to parent-urls.py to it.
    The class in inherits to this class perform overriding of a later property.
    Property 'success_url_viewname': Move to urls-viewname
        (see django-urls-reverse) when succeeded in processing
    """
    form_id = 'create_form'
    form_class = wf_engine_forms.CreateForm
    template_name = 'project/ticket_templates/wf_engine/create/create.html'
    success_url = None
    success_url_viewname = 'horizon:project:ticket_templates:index'
    submit_url = None

    def get_initial(self):
        super(CreateView, self).get_initial()

        form_template = self.template_contents['create']

        initial = self._create_initial()

        self.submit_url = self.get_submit_url(self.request)

        initial['first_status_code'] = \
            self.template_contents['first_status_code']
        initial['parameters'] = form_template['parameters']

        return initial

    def get_context_data(self, **kwargs):
        # Get a create form key information from request.
        allowed_submit = True

        form_template = self.template_contents['create']
        workflow_pattern = self.ticket_template_data.workflow_pattern

        wf_pattern_contents = workflow_pattern.get('wf_pattern_contents')
        all_status = wf_pattern_contents.get('status_list')

        next_status_source = filter(lambda row:
                                    row.get('status_code', None) == 'none',
                                    all_status)[0]
        next_status_list = ticket_utils.get_next_status_list(
            self.request, next_status_source)

        if len(next_status_list) == 0:
            allowed_submit = False

        context = super(CreateView, self).get_context_data(**kwargs)

        # Set base context for form
        context['title'] = _(self.template_contents['ticket_type'])  # noqa
        context['sub_title'] = ticket_utils.get_language_name(
            self.request,
            self.template_contents['application_kinds_name'])
        context['description'] = ticket_utils.get_language_name(
            self.request,
            form_template.get('description', {'default': ''}))

        # Set input parameter values and call plugin names for the html
        context['parameters'] = form_template['parameters']
        context['custom_left'] = self._get_plugin_names(form_template,
                                                        'left')
        context['custom_right'] = self._get_plugin_names(form_template,
                                                         'right')
        context['custom_bottom'] = self._get_plugin_names(form_template,
                                                          'bottom')

        context['allowed_submit'] = allowed_submit
        context['first_status_code'] = \
            self.template_contents['first_status_code']

        # Set plugins data
        self._call_plugins(context, form_template,
                           template_contents=self.template_contents)

        return context
