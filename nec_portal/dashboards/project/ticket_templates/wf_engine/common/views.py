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

import logging
import re

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from nec_portal.api import ticket as ticket_api
from nec_portal.dashboards.project.ticket_templates.wf_engine.common \
    import constants

LOG = logging.getLogger(__name__)


class CallPluginMixin(object):
    """This class provides a necessary function to call plugin"""

    def _get_plugin_names(self, form_template, position):
        """Get plugin names from form context.
        A plugin has 'left:left-top' or 'right:right-bottom' position property.
        By this method, it gets plugin of the designated position
        from the form context.
        :param form_template: Form context of ticket template contents
        :param position: Position to get(set left or right value)
        """
        plugin_names = []

        for plugin in form_template.get('custom', []):
            plugin_name = plugin.keys()[0]
            plugin_position = plugin[plugin_name]
            if position == plugin_position:
                html_path = '%(template)s_%(plugin_name)s.html' % {
                    'template': constants.PLUGIN_TEMPLATE,
                    'plugin_name': plugin_name}

                msg = 'Call plugin(template): %s' % html_path
                LOG.info(msg)

                plugin_names.append(html_path)

        return plugin_names

    def _call_plugins(self, context, form_template, **kwargs):
        """Call plugin from a tickettemplate contexts
        :param context: View context data
        :param form_template: Form context of tickettemlate contents
        :param kwargs: **kwargs
        """
        plugins = form_template.get('custom', [])

        for plugin in plugins:
            # Load plugin class
            plugin_name = plugin.keys()[0]
            class_name = re.sub(r'(^.)|_.',
                                lambda m: m.group().upper().replace('_', ''),
                                plugin_name)
            plugin_path = '%(namespace)s_%(plugin_name)s.%(class_name)s' % {
                'namespace': constants.PLUGIN_NAMESPACE,
                'plugin_name': plugin_name,
                'class_name': class_name}

            msg = 'Call plugin: %s' % plugin_path
            LOG.info(msg)

            plugin_class = self._load_class(plugin_path)()
            plugin_class.set_context_data(self, context, form_template,
                                          **kwargs)

    def _load_class(self, class_path):
        """Load class from a path string
        :param class_path: example) package.aaa.bbb.Class
        """
        target = class_path.split('.')
        package = target[0]
        module = '.'.join(target[:-1])
        class_name = target[-1]

        return getattr(__import__(module, fromlist=[str(package)]),
                       class_name)


class BaseView(forms.ModalFormView, CallPluginMixin):
    """View base class of workflow view form engine.
    All workflow view needs to get a ticket template data to create each view.
    And workflow view form engine has a mechanism of calling function defined
    by plugins.
    This class has these implementation as a base class.
    Property 'submit_label': Form submit button label(not override)
    Property 'cancel_label': Form cancel button label(not override)
    Property 'ticket_template_id': Id of tickettemplate data
    Property 'ticket_template_data': Get the tickettemplate data
    Property 'template_contents': Contents on the tickettemplate data
    """
    submit_label = _('Submit')
    cancel_label = _('Cancel')
    ticket_template_id = None
    ticket_template_data = None
    template_contents = None

    def get_initial(self):
        self.ticket_template_id = self.kwargs['ticket_template_id']

        try:
            # Get a tickettemplate context
            self.ticket_template_data = \
                ticket_api.tickettemplates_get(self.request,
                                               self.ticket_template_id)
        except Exception as e:
            LOG.error(e)
            exceptions.handle(
                self.request,
                _('An error occurred while processing your request.') + e)
            raise

        self.template_contents = self.ticket_template_data.template_contents

    def _create_initial(self):
        initial = {}

        initial['url_kwargs'] = {}
        for key, value in self.kwargs.items():
            initial['url_kwargs'][key] = value

        return initial

    def get_success_url(self, request=None):
        """Returns the URL to redirect to after a successful action."""
        if self.success_url:
            return self.success_url
        elif self.success_url_viewname:
            return reverse_lazy(self.success_url_viewname)

        return request.get_full_path()

    def get_submit_url(self, request=None):
        """Returns the URL to redirect to after a submit action."""
        if self.submit_url:
            return self.submit_url

        return request.get_full_path()

    def get_cancel_url(self):
        return self.get_success_url()
