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

import datetime
import six

from django.utils.translation import ugettext_lazy as _
from horizon import forms

from nec_portal.dashboards.project.ticket_list \
    import utils as ticket_utils


class BuildParameterFieldMixin(object):
    """Methods in this class are copying some implementation from other panel.
    Because this panel has to work without other panels.
    So, basically we don't have to change methods in this class
    in order to reflect original changes easily.
    """
    def _build_parameter_fields(self, parameters, current_status):
        """Create input field object at form.
        :param parameters: Input field context
        :param current_status: Current workflow status
        """
        is_update = (current_status is not None)

        for param in parameters:
            field = None

            if is_update and param.get(
                    'status', current_status) != current_status:
                continue

            field_key = self.param_prefix + param['key']
            field_description = param.get('description', None)
            field_constraints = param.get('constraints', {})
            # Set common field properties
            field_args = {
                'initial': param.get('default', None),
                'label':
                    ticket_utils.get_language_name(self.request,
                                                   param['label']),
                'help_text':
                    ticket_utils.get_language_name(self.request,
                                                   field_description),
                'required': self._get_required(field_constraints, is_update)
            }
            param_type = param['type']

            # Create a field object
            if param_type == 'number':
                if 'range' in field_constraints:
                    if 'min' in field_constraints['range']:
                        field_args['min_value'] = int(
                            field_constraints['range']['min'])
                    if 'max' in field_constraints['range']:
                        field_args['max_value'] = int(
                            field_constraints['range']['max'])

                field = forms.IntegerField(**field_args)

            elif param_type == 'date':
                field = forms.DateField(**field_args)
                field.widget.attrs['class'] = 'datepicker'
                field.widget.attrs['data-date-format'] = 'yyyy-mm-dd'

            elif param_type == 'boolean':
                field = forms.BooleanField(**field_args)

            elif param_type == 'hidden':
                field = forms.CharField(**field_args)
                field.widget = forms.HiddenInput()

            elif 'allowed_values' in field_constraints:
                choices = self._create_choice_value(
                    field_constraints['allowed_values'])
                field_args['choices'] = choices
                field = forms.ChoiceField(**field_args)

            else:
                if 'length' in field_constraints:
                    if 'min' in field_constraints['length']:
                        field_args['min_length'] = int(
                            field_constraints['length']['min'])
                    if 'max' in field_constraints['length']:
                        field_args['max_length'] = int(
                            field_constraints['length']['max'])

                if param_type == 'email':
                    field = forms.EmailField(**field_args)

                elif 'allowed_pattern' in field_constraints:
                    field_args['regex'] = field_constraints['allowed_pattern']
                    field = forms.RegexField(**field_args)

                else:
                    field = forms.CharField(**field_args)

                if param.get('multi_line', False):
                    field.widget = forms.Textarea(
                        attrs={'class': 'modal-body-fixed-width', 'rows': 4})

            if field:
                self.fields[field_key] = field
                self._set_update_required_option(field_key,
                                                 field_constraints,
                                                 is_update)

    def _get_required(self, field_constraints, is_update):
        """Get required option of a field.
        If called from update status, don't use normal validation option.
        because current status move to reject status case.
        """
        if is_update:
            return False

        return field_constraints.get('required', False)

    def _set_update_required_option(self, field_key, field_constraints,
                                    is_update):
        """Get required option of a field for update"""
        if not is_update or not field_constraints.get('required', False):
            return

        required_validate_status = field_constraints.get(
            'required_validate_status', [])

        if not isinstance(required_validate_status, list):
            required_validate_status = [required_validate_status]

        setattr(self, 'clean_%s' % field_key,
                lambda: self._clean_update_required(field_key,
                                                    required_validate_status))

    def _clean_update_required(self, field_key, required_validate_status):
        """Validate required of a field for update"""
        value = self.cleaned_data[field_key]
        selected_status = self._get_selected_status_information(
            self._selected_status_value())['next_status_code']

        if required_validate_status and \
                selected_status in required_validate_status and \
                (not value):
            raise forms.ValidationError(_('This field is required.'))
        return value

    def _selected_status_value(self):
        """Get approval_flg field value from force http requrest data.
        see 'https://github.com/django/django/blob/master/django/forms/forms.py'
        """  # noqa
        name = 'approval_flg'
        field = self.fields[name]

        value = field.widget.value_from_datadict(
            self.data, self.files, self.add_prefix(name))

        return field.clean(value)

    def _get_params_list(self, data):
        """Get input parameter values on html submit form
        :param data: Handle data
        """
        prefix_length = len(self.param_prefix)
        params = {}
        for (k, v) in six.iteritems(data):
            if k.startswith(self.param_prefix):
                if isinstance(v, datetime.date):
                    v = ticket_utils.get_utc_datetime_str(self.request, v)

                params[k[prefix_length:]] = v

        return params

    def _get_selected_status_information(self, approval_flg):
        selected_status = approval_flg.split(":")

        return {
            'last_status_code': selected_status[2],
            'last_workflow_id': selected_status[3],
            'next_status_code': selected_status[0],
            'next_workflow_id': selected_status[1]
        }


class BaseForm(forms.SelfHandlingForm, BuildParameterFieldMixin):
    """Form base class of workflow view form engine.
    This class has methods to analyze parameters
    from ticket template context and to create
    form fields which depend on its parameter.
    Property 'param_prefix': input item name/id prefix string.
    """
    param_prefix = '__param_'
    url_param_prefix = '__url_param_'

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        initial = kwargs['initial']

        # Create url kwargs fields.
        url_kwargs = initial.pop('url_kwargs')
        self._build_url_kwargs_fields(url_kwargs)

        # Create parameter fields.
        current_status = initial.get('current_status', None)
        parameters = initial.pop('parameters')
        self._build_parameter_fields(parameters, current_status)

    def _build_url_kwargs_fields(self, url_kwargs):
        """Create hidden field object at form."""
        for key, value in url_kwargs.items():
            field = forms.CharField(widget=forms.HiddenInput())
            field.initial = value
            self.fields[self.url_param_prefix + key] = field

    def _get_url_kwargs_fields(self, data):
        prefix_length = len(self.url_param_prefix)
        return dict([(k[prefix_length:], v) for (k, v) in six.iteritems(data)
                     if k.startswith(self.url_param_prefix)])

    def _create_choice_value(self, allowed_value):
        """Create tuple value for multi language combobox/checkbox
        :param allowed_value: A combobox/checkbox select value list
        """
        choice_value = []

        for av in allowed_value:
            choice_value.append((av['value'],
                                 ticket_utils.get_language_name(self.request,
                                                                av['label'])))

        return tuple(choice_value)
