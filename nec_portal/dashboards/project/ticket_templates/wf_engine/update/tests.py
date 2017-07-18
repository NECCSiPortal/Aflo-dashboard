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

import copy
import datetime
import json
import six

from decimal import Decimal
from mox3.mox import IsA

from django.core.urlresolvers import reverse
from django import http

from openstack_dashboard.test import helpers as test

from afloclient.v1.catalogs import Catalog
from afloclient.v1.price import Price
from afloclient.v1.tickets import Ticket
from afloclient.v1.tickettemplates import Tickettemplate

from nec_portal import api
from nec_portal.dashboards.project.ticket_list import \
    utils as ticket_utils
from nec_portal.dashboards.project.ticket_templates import \
    fixture_20160627 as fixture
from nec_portal.dashboards.project.ticket_templates import panel  # noqa
from nec_portal.test import aflo_helpers as aflo_test

PARAM_PREFIX = '__param_'
# Maximum number value is 9999.
NUMBER_MAX_VALUE = 9999
# Maximum string value is 512.
STRING_MAX_VALUE = unicode('a' * 512)
DATE_VALUE = '2016-06-27'
EMAIL_VALUE = 'xxxxx@xxxxx.xxxxx'
# allowed_pattern: "\d{2}-[a-z]{5}"
REGULAR_EXPRESSION_VALUE = '99-xxxxx'
POST_DATA = {
    '__param_number_parameter': NUMBER_MAX_VALUE,
    '__param_string_parameter': STRING_MAX_VALUE,
    '__param_date_parameter': '2016-06-27',
    '__param_email_parameter': 'xxxxx@xxxxx.xxxxx',
    '__param_boolean_parameter': True,
    '__param_select_item_parameter': '0',
    '__param_regular_expression_parameter': '99-xxxxx',
    '__param_hidden_parameter': ''
}


class WorkflowEngineTicketUpdateTest(aflo_test.BaseAdminViewTests):
    """Workflow engine ticket update test class"""

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_view(self):
        """Test 'Display the update screen' to successfully run"""

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']
        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        api.ticket.tickettemplates_get(
            IsA(http.HttpRequest),
            ticket_template_id).AndReturn(
                Tickettemplate(self, template_data, loaded=True))

        api.ticket.ticket_get_detailed(
            IsA(http.HttpRequest), ticket_detail_id).AndReturn(
                Ticket(self, ticket_detail_data, loaded=True))

        self._search_catalog_price_list(
            template_data['template_contents']['target_id'], True)

        self.mox.ReplayAll()

        url = reverse(
            'horizon:project:ticket_list:wf_engine_update:index',
            args=[ticket_detail_id])

        res = self.client.get(url)

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, 'project/ticket_templates/wf_engine/update/update.html')

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_view_nextstatus_not_display(self):
        """Test 'Display the update screen' to successfully run"""

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']
        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        workflow_list = ticket_detail_data['workflow']
        for workflow in workflow_list:
            if workflow['status'] == 1:
                for next_status in workflow['status_detail']['next_status']:
                    next_status['grant_role'] = 'test'

        api.ticket.tickettemplates_get(
            IsA(http.HttpRequest),
            ticket_template_id).AndReturn(
            Tickettemplate(self, template_data, loaded=True))

        api.ticket.ticket_get_detailed(
            IsA(http.HttpRequest), ticket_detail_id).AndReturn(
                Ticket(self, ticket_detail_data, loaded=True))

        self._search_catalog_price_list(
            template_data['template_contents']['target_id'], True)

        self.mox.ReplayAll()

        url = reverse(
            'horizon:project:ticket_list:wf_engine_update:index',
            args=[ticket_detail_id])

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, 'project/ticket_templates/wf_engine/update/update.html')

    @test.create_stubs({api.ticket: ('ticket_get_detailed',
                                     'tickettemplates_get',
                                     'ticket_update',)})
    def test_ticket_update(self):
        """Test 'Update a new ticket' to successfully run"""

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']
        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)

        params_list = self._get_params_list(post_data)

        post_data['__url_param_ticket_id'] = ticket_detail_id
        post_data['approval_flg'] = fixture.APPROVAL_FLAGS[0][0]

        self._ticket_update_successfully_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            params_list)

    @test.create_stubs({api.ticket: ('ticket_get_detailed',
                                     'tickettemplates_get',
                                     'ticket_update',)})
    def test_ticket_update_no_input_data_to_post(self):
        """Test 'Update a new ticket' to successfully run.
        No input data to post.
        """

        template_data = self._get_ticket_template_data(0)

        template_data['template_contents']['update']['parameters'] = []

        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        # No input data to post.
        params_list = {}

        post_data = {}
        post_data['__url_param_ticket_id'] = ticket_detail_id
        post_data['approval_flg'] = fixture.APPROVAL_FLAGS[0][0]

        self._ticket_update_successfully_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            params_list)

    @test.create_stubs({api.ticket: ('ticket_get_detailed',
                                     'tickettemplates_get',
                                     'ticket_update',)})
    def test_ticket_update_minimum_parameters_key(self):
        """Test 'Update a new ticket' to successfully run"""

        template_data = self._get_ticket_template_data(0)

        delete_keys = ['default', 'constraints', 'description', 'multi_line']
        parameters = template_data['template_contents']['update']['parameters']
        for delete_key in delete_keys:
            for parameter in parameters:
                if delete_key in parameter:
                    del parameter[delete_key]

        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)

        params_list = self._get_params_list(post_data)

        post_data['__url_param_ticket_id'] = ticket_detail_id
        post_data['approval_flg'] = fixture.APPROVAL_FLAGS[0][0]

        self._ticket_update_successfully_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            params_list)

    @test.create_stubs({api.ticket: ('ticket_get_detailed',
                                     'tickettemplates_get',
                                     'ticket_update',)})
    def test_ticket_update_input_2byte_string(self):
        """Test 'Update a new ticket' to successfully run
        Input 2byte string value.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Input 2byte string value.
        post_data['__param_string_parameter'] = u'\u5099\u8003'

        params_list = self._get_params_list(post_data)

        post_data['__url_param_ticket_id'] = ticket_detail_id
        post_data['approval_flg'] = fixture.APPROVAL_FLAGS[0][0]

        self._ticket_update_successfully_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            params_list)

    @test.create_stubs({api.ticket: ('ticket_get_detailed',
                                     'tickettemplates_get',
                                     'ticket_update',)})
    def test_ticket_update_input_zero_value(self):
        """Test 'Update a new ticket' to successfully run
        Input zero value.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        parameters = template_data['template_contents']['update']['parameters']
        for parameter in parameters:
            if 'number' in parameter['type']:
                parameter['constraints']['range']['min'] = 0

        post_data = copy.deepcopy(POST_DATA)
        # Input zero value.
        post_data['__param_number_parameter'] = 0

        params_list = self._get_params_list(post_data)

        post_data['__url_param_ticket_id'] = ticket_detail_id
        post_data['approval_flg'] = fixture.APPROVAL_FLAGS[0][0]

        self._ticket_update_successfully_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            params_list)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_required_parameters_not_set(self):
        """Test 'Ticket data update'
        Required parameters not set.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # number_parameter is a required field.
        post_data['__param_number_parameter'] = None

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_maximum_value_over_the_string_parameter(self):
        """Test 'Ticket data update'
        Maximum value over the string parameter.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Maximum value over the string parameter.
        post_data['__param_string_parameter'] = STRING_MAX_VALUE + 'a'

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_minimum_value_over_the_string_parameter(self):
        """Test 'Ticket data update'
        Minimum value over the string parameter.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Minimum value over the string parameter.
        post_data['__param_string_parameter'] = 'a'

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_maximum_value_over_the_number_parameter(self):
        """Test 'Ticket data update'
        Maximum value over the number parameter.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Maximum value over the number parameter.
        post_data['__param_number_parameter'] = NUMBER_MAX_VALUE + 1

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_minimum_value_over_the_number_parameter(self):
        """Test 'Ticket data update'
        Minimum value over the number parameter.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Minimum value over the number parameter.
        post_data['__param_number_parameter'] = 0

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_input_minus_value(self):
        """Test 'Ticket data update'
        Input minus value.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Input minus value.
        post_data['__param_number_parameter'] = -1

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_input_decimal_value(self):
        """Test 'Ticket data update'
        Input decimal value.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Input decimal value.
        post_data['__param_number_parameter'] = Decimal("1.5")

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_date_parameter_incorrect_format(self):
        """Test 'Ticket data update'
        Date parameter incorrect format.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # There is no in date format.
        post_data['__param_date_parameter'] = 'xxxxxxxxxx'

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_email_parameter_incorrect_format(self):
        """Test 'Ticket data update'
        Email parameter incorrect format.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # There is no in email format.
        post_data['__param_email_parameter'] = 'xxxxxxxxxx'

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_value_selection_does_not_exist(self):
        """Test 'Ticket data update'
        Value selection does not exist.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Value selection does not exist.
        post_data['__param_select_item_parameter'] = '99'

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_nextstatus_not_display(self):
        """Test 'Ticket data update'
        Next status does not display.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        workflow_list = ticket_detail_data['workflow']
        for workflow in workflow_list:
            if workflow['status'] == 1:
                for next_status in workflow['status_detail']['next_status']:
                    next_status['grant_role'] = 'test'

        post_data = copy.deepcopy(POST_DATA)
        # Value selection does not exist.
        post_data['__param_select_item_parameter'] = '99'

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_incorrect_regular_expression(self):
        """Test 'Ticket data update'
        Incorrect regular expression.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Incorrect regular expression.
        post_data['__param_regular_expression_parameter'] = 'xx-xxxxx'

        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    @test.create_stubs({api.ticket: ('tickettemplates_get',
                                     'ticket_get_detailed',
                                     'catalog_get_detailed',
                                     'price_list_detailed2',)})
    def test_ticket_update_no_price_data(self):
        """Test 'Ticket data update'
        No price data.
        """

        template_data = self._get_ticket_template_data(0)
        ticket_template_id = template_data['id']

        ticket_detail_data = self._get_ticket_detail_data(0)
        ticket_detail_id = ticket_detail_data['id']

        post_data = copy.deepcopy(POST_DATA)
        # Incorrect regular expression.
        post_data['__param_regular_expression_parameter'] = 'xx-xxxxx'

        # No price data.
        self._ticket_update_error_action(
            ticket_template_id, template_data,
            ticket_detail_id, ticket_detail_data, post_data,
            True)

    def _get_ticket_template_data(self, index):
        return copy.deepcopy(fixture.TICKET_TEMPLATE_DATA_LIST[index])

    def _get_ticket_detail_data(self, index):
        return copy.deepcopy(fixture.TICKET_DATA_LIST[index])

    def _get_first_status_code(self, template_data):
        return template_data['template_contents']['first_status_code']

    def _ticket_update_successfully_action(
        self, template_id, template_data,
        ticket_detail_id, ticket_detail_data, post_data,
            params_list):

        radival = post_data['approval_flg'].split(":")

        ticket_data = {
            'additional_data': json.dumps(params_list),
            'last_status_code': radival[2],
            'last_workflow_id': radival[3],
            'next_status_code': radival[0],
            'next_workflow_id': radival[1]
        }

        api.ticket.ticket_get_detailed(
            IsA(http.HttpRequest), ticket_detail_id).AndReturn(
                Ticket(self, ticket_detail_data, loaded=True))

        api.ticket.tickettemplates_get(
            IsA(http.HttpRequest),
            template_id).AndReturn(
                Tickettemplate(self, template_data, loaded=True))

        # Update a ticket.
        api.ticket.ticket_update(
            IsA(http.HttpRequest),
            ticket_detail_id, ticket_data)
        self.mox.ReplayAll()

        url = reverse(
            'horizon:project:ticket_list:wf_engine_update:index',
            args=[ticket_detail_id])

        res = self.client.post(url, post_data)

        self.assertNoFormErrors(res)
        self.assertEqual(res.status_code, 302)

    def _ticket_update_error_action(
        self, template_id, template_data,
        ticket_detail_id, ticket_detail_data,
            post_data, price_exists_flag):

        api.ticket.tickettemplates_get(
            IsA(http.HttpRequest),
            template_id).AndReturn(
                Tickettemplate(self, template_data, loaded=True))

        api.ticket.ticket_get_detailed(
            IsA(http.HttpRequest), ticket_detail_id).AndReturn(
                Ticket(self, ticket_detail_data, loaded=True))

        self._search_catalog_price_list(
            template_data['template_contents']['target_id'], price_exists_flag)

        self.mox.ReplayAll()

        url = reverse(
            'horizon:project:ticket_list:wf_engine_update:index',
            args=[ticket_detail_id])
        res = self.client.post(url, post_data)

        self.assertEqual(res.status_code, 200)

    def _search_catalog_price_list(self, target_ids, price_exists_flag):
        count = 0
        for target_id in target_ids:
            catalog_data = Catalog(
                self, copy.deepcopy(fixture.CATALOG_DATA_LIST[count]),
                loaded=True)

            api.ticket.catalog_get_detailed(
                IsA(http.HttpRequest), target_id).AndReturn(catalog_data)

            if price_exists_flag:
                catalog_price_data = [Price(
                    self, copy.deepcopy(
                        fixture.CATALOG_PRICE_DATA_LIST[count]),
                    loaded=True)]
            else:
                catalog_price_data = []

            api.ticket.price_list_detailed2(
                IsA(http.HttpRequest), target_id).AndReturn(catalog_price_data)
            count = count + 1

    def _get_params_list(self, data):
        prefix_length = len(PARAM_PREFIX)
        params = {}
        for (k, v) in six.iteritems(data):
            if k.startswith(PARAM_PREFIX):
                if self._is_date(v):
                    v_date = datetime.datetime.strptime(
                        v, ticket_utils.DISPLAY_DATE_FORMAT)
                    v = ticket_utils.get_utc_datetime_str(self.request, v_date)

                params[k[prefix_length:]] = v

        return params

    def _is_date(self, dt):
        try:
            datetime.datetime.strptime(dt, ticket_utils.DISPLAY_DATE_FORMAT)
        except Exception:
            return False

        return True
