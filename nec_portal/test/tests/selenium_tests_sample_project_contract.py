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

"""Test 'Project Contract' on Aflo.
Please operate setting.
  Step1. Create Projects
    - admin
    - demo
      No child project.
  Step2. Create Users
    - admin
    - demo
  Step3. Create Roles
    - admin
      Grant: [admin] project - [admin] user
    - C__Global__ProjectAdmin
      Grant: [demo] project - [demo] user
    - O__<Region Name>__ContractManager
      Grant: [admin] project - [admin] user
             [demo] project - [admin] user
  Step4. Create Workflows
    Create Ticket Template and Workflow Pattern.
    - New Project Contract
    - Cancel Project Contract
  Step5. Change Selenium Parameters
    - SET_BASE_URL
    - DB_USER
    - DB_PASS
    - DEMO_PROJECT_ID
    - DEMO_USER_ID
"""

import datetime
import os
import subprocess
import time
import traceback

from horizon.test import helpers as test

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# Command executor. Hub URL of Jenkins.
SET_COMMAND_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'
# Base URL. Environment for testing.
# As for the URL, the last slash is unnecessary.
SET_BASE_URL = 'http://127.0.0.1/dashboard'
# Login user.
SET_USER = {
    'admin': {
        'USERNM': 'admin',
        'PASSWORD': 'xxxx'
    },
    'demo': {
        'USERNM': 'demo',
        'PASSWORD': 'xxxx'
    }
}
# Width of the window.
SET_WIDTH = 1280
# Height of the window.
SET_HEIGHT = 1024
# Implicitly wait & Timeout.
SET_IMPLICITLY_WAIT = 90
SET_TIMEOUT = 5
# Capture of location.
SET_CAPPATH = 'openstack_dashboard/test/tests/screenshots/'
# They are arranged sequentially by setting the browser target.
SET_BROWSER_LIST = {
    'firefox': {
        'browserName': 'firefox',
        'version': '',
        'platform': 'ANY',
        'javascriptEnabled': True,
    },
    'chrome': {
        'browserName': 'chrome',
        'version': '',
        'platform': 'ANY',
        'javascriptEnabled': True,
    },
    'ie11': {
        'browserName': 'internet explorer',
        'version': '11',
        'platform': 'WINDOWS',
        'javascriptEnabled': True,
    },
}

# They are arranged sequentially by setting the execution target.
SET_METHOD_LIST = [
    # Initialize.
    'delete_data',
    # New project contract.
    # Project user.
    'sign_in_admin',
    'change_setting',
    'project_new_project_contract_entry',
    # Approval user.
    'admin_new_project_contract_approval_canceled',
    'admin_new_project_contract_approval_rejected',
    'admin_new_project_contract_approval_accepted_to_canceled',
    'admin_new_project_contract_approval_accepted_to_rejected',
    'admin_new_project_contract_approval_working_to_canceled',
    'admin_new_project_contract_approval_working_to_rejected',
    'admin_new_project_contract_approval_done',
    'sign_out',
    # Cancel project contract.
    # Project user.
    'sign_in_demo',
    'project_cancel_project_contract_entry',
    'project_cancel_project_contract_canceled',
    'sign_out',
    # Approval user.
    'sign_in_admin_project_demo',
    'project_cancel_project_contract_approval_rejected',
    'project_cancel_project_contract_approval_final_approval',
    'admin_project_list_confirm',
    # Close.
    'sign_out',
]

# Take the capture.
SET_CAPFLG = True
# Test language pattern.
SET_TEST_LANGUAGE = {
    'en': True,
    'ja': True,
}
# Test browser pattern.
SET_TEST_BROWSER = {
    'firefox': True,
    'chrome': True,
    'ie11': True,
}

SET_SPECIAL_CODE = '<>?!"#$%&\'()'

DB_USER = 'aflo'
DB_PASS = 'aflo'

TAB_NAME = 'ticket_templates_group_tabs__request_tab'

TICKET_TEMPLATE_ID_NEW_PROJECT_CONTRACT = '30'

MAX_LENGTH_UUID = 32
MAX_LENGTH_NAME = 256
MAX_LENGTH_MESSAGE = 512

FORM_CREATE = 'create_form'
FORM_UPDATE = 'update_form'

DEMO_PROJECT_ID = 'cd464f0c5fb74f86897dd8a8195a0eb7'
DEMO_USER_ID = '2c4a9587ead94f99947d69fae6134224'


class BrowserTests(test.SeleniumTestCase):
    """Selenium Test of Browser"""

    def setUp(self):
        """Setup selenium settings"""
        super(BrowserTests, self).setUp()

        # One setting of the browser is necessary
        # to carry out a test of selenium.
        key = SET_BROWSER_LIST.keys()[0]
        value = SET_BROWSER_LIST[key]

        print (value)
        self.caps = key
        self.selenium = webdriver.Remote(
            command_executor=SET_COMMAND_EXECUTOR,
            desired_capabilities=value)

        self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)

    def initialize(self):
        """Initializing process"""
        # Capture count.
        self.cap_count = 1
        # Method name.
        self.method = ''

    def test_main(self):
        """Main execution method"""
        try:
            # Datetime.
            self.datetime = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

            # Browser order definition.
            for key, value in SET_BROWSER_LIST.items():
                if key not in SET_TEST_BROWSER or \
                        not SET_TEST_BROWSER[key]:
                    continue

                if not self.caps == key:
                    self.caps = key
                    self.selenium = webdriver.Remote(
                        command_executor=SET_COMMAND_EXECUTOR,
                        desired_capabilities=value)

                    self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)

                # Browser display waiting time.
                self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)
                # Set the size of the window.
                self.selenium.set_window_size(SET_WIDTH, SET_HEIGHT)

                for language, flg in SET_TEST_LANGUAGE.items():
                    if not flg:
                        continue

                    print ('Test language = [' + language + ']')

                    # Initializing process
                    self.initialize()
                    # Object language
                    self.multiple_languages = language
                    # Call execution method
                    self.execution()

            print ('Test has been completed')

        except Exception as e:
            print (' Test Failure:' + e.message)
            print (traceback.print_exc())

    def execution(self):
        """Execution method"""
        # Method execution order definition.
        for self.method in SET_METHOD_LIST:
            try:
                method = getattr(self, self.method)
                method()

                print (' Success:' + self.caps + ':' + self.method)
            except Exception as e:
                print (' Failure:' + self.caps + ':' + self.method +
                       ':' + e.message)
                print (traceback.print_exc())

    def save_screenshot(self):
        """Save a screenshot"""
        if SET_CAPFLG:
            filepath = SET_CAPPATH + self.datetime + '/' + \
                self.multiple_languages + '/' + self.caps + '/'
            filename = str(self.cap_count).zfill(4) + \
                '_' + self.method + '.png'
            # Make directory.
            if not os.path.isdir(filepath):
                os.makedirs(filepath)

            time.sleep(SET_TIMEOUT)
            self.selenium.get_screenshot_as_file(filepath + filename)
            self.cap_count = self.cap_count + 1

    def trans_and_wait(self, nextId, urlpath, timeout=SET_TIMEOUT):
        """Transition to function"""
        time.sleep(timeout)
        self.selenium.get(SET_BASE_URL + urlpath)

        if nextId:
            self.wait_id(nextId, timeout)

    def fill_field(self, field_id, value):
        """Enter a value to the field"""
        self.fill_field_clear(field_id)
        if type(value) in (int, long):
            value = str(value)
        while 0 < len(value):
            split_value = value[0:10]
            self.selenium.find_element_by_id(field_id).send_keys(split_value)
            value = value[10:]

    def fill_field_by_name(self, field_name, value):
        """Enter a value to the field"""
        self.fill_field_clear_by_name(field_name)

        time.sleep(SET_TIMEOUT)
        self.selenium.find_element_by_name(field_name).send_keys(value)

    def fill_field_clear(self, field_id):
        """Clear to the field"""
        time.sleep(SET_TIMEOUT)
        self.selenium.find_element_by_id(field_id).clear()

    def fill_field_clear_by_name(self, field_name):
        """Clear to the field"""
        time.sleep(SET_TIMEOUT)
        self.selenium.find_element_by_name(field_name).clear()

    def click_id(self, field_id, timeout=SET_TIMEOUT):
        """Click on the button id(no wait)"""
        element = self.selenium.find_element_by_id(field_id)
        element.click()

    def click_css(self, css, timeout=SET_TIMEOUT):
        """Click on the button css(no wait)"""
        time.sleep(timeout)
        element = self.selenium.find_element_by_css_selector(css)
        element.click()

    def click_xpath_and_ajax_wait(self, xpath, timeout=SET_TIMEOUT):
        """Click on the button xpath ajax wait"""
        time.sleep(timeout)
        element = self.selenium.find_element_by_xpath(xpath)
        element.click()
        self.wait_ajax(timeout)

    def set_select_value(self, element_id, value):
        """Set of pull-down menu by value"""
        time.sleep(SET_TIMEOUT)
        Select(self.selenium.find_element_by_id(
            element_id)).select_by_value(value)

    def wait_id(self, nextId, timeout=SET_TIMEOUT):
        """Wait until the ID that you want to schedule is displayed"""
        WebDriverWait(self.selenium, timeout).until(
            EC.visibility_of_element_located((By.ID, nextId)))

    def wait_css(self, nextCss, timeout=SET_TIMEOUT):
        """Wait until the ID that you want to schedule is displayed"""
        WebDriverWait(self.selenium, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, nextCss)))

    def wait_ajax(self, timeout=SET_TIMEOUT):
        """Wait until ajax request is completed"""
        WebDriverWait(self.selenium, timeout).until(
            lambda s: s.execute_script('return jQuery.active == 0'))

    def change_setting(self, page=20):
        """Change Language"""
        self.trans_and_wait('user_settings_modal', '/settings/')
        self.fill_field('id_pagesize', page)
        self.set_select_value('id_language', self.multiple_languages)
        self.click_css('input[type=submit]')

    def sign_in_admin(self):
        """Sign in admin user"""
        self._sign_in('admin', 'admin')

    def sign_in_admin_project_demo(self):
        """Sign in admin user of demo project"""
        self._sign_in('admin', 'demo')

    def sign_in_demo(self):
        """Sign in demo user"""
        self._sign_in('demo', 'demo')

    def _sign_in(self, username='admin', project='admin'):
        """Sign in"""
        # Run a sign-in
        self.trans_and_wait('loginBtn', '')

        self.fill_field('id_username', SET_USER.get(username).get('USERNM'))
        self.fill_field('id_password', SET_USER.get(username).get('PASSWORD'))

        self.click_id('loginBtn')

        # Set project.
        self._select_project(project)

        self.save_screenshot()

    def sign_out(self):
        """Sign out"""
        self.trans_and_wait('loginBtn', '/auth/logout/')
        time.sleep(SET_TIMEOUT)

    def _select_project(self, project_name='demo'):
        """Select project name"""
        time.sleep(SET_TIMEOUT)
        self.click_css('span.fa-caret-down')

        time.sleep(SET_TIMEOUT)
        self.click_xpath_and_ajax_wait(
            '//span[@class="dropdown-title"][contains(text(),"%s")]'
            % project_name)

    def _execute_sql(self, sql):
        """Execute sql by local mysql command.
        :param sql: execute sql string.
        """
        subprocess.call(
            ['mysql', '-D', 'aflo', '-u' + DB_USER, '-p' + DB_PASS, '-e', sql])

    # ==================================================

    def project_new_project_contract_entry(self):
        """Entry a 'New Project Contract' ticket"""
        self._project_ticket_templates_list(True)

        # Add New Project Contract.
        self._project_new_project_contract_form_show(
            TICKET_TEMPLATE_ID_NEW_PROJECT_CONTRACT, FORM_CREATE)
        self._test_new_project_contract_irregular_required()
        self._test_new_project_contract_irregular_value()
        self._test_new_project_contract_irregular_max_length_over()
        self._cancel_request()

        # Create 7 ticket.(New Project Contract)
        #  Root 1: [New Project Contract] -> Canceled
        #  Root 2: [New Project Contract] -> Rejected
        #  Root 3: [New Project Contract] -> Accepted -> Canceled
        #  Root 4: [New Project Contract] -> Accepted -> Rejected
        #  Root 5: [New Project Contract] -> Accepted -> Working -> Canceled
        #  Root 6: [New Project Contract] -> Accepted -> Working -> Rejected
        #  Root 7: [New Project Contract] -> Accepted -> Working -> Done
        for row_idx in range(7):
            save_screen = True if row_idx == 0 else False

            self._project_new_project_contract_form_show(
                TICKET_TEMPLATE_ID_NEW_PROJECT_CONTRACT, FORM_CREATE)
            self._test_new_project_contract_entry(save_screen)

            self._project_ticket_templates_list(False)

    def _test_new_project_contract_irregular_required(
            self, form_type=FORM_CREATE):
        """Entry a 'New Project Contract' ticket.
        Required error pattern.
        :param form_type: Form type.
        """
        # Show confirm form and Submit.
        self._submit_confirm(form_type)

        self.wait_id(form_type)

        self.save_screenshot()

    def _test_new_project_contract_irregular_value(
            self, last_status_flag=False, form_type=FORM_CREATE):
        """Entry a 'New Project Contract' ticket.
        Irregular_value pattern.
        :param last_status_flag: Last status flag.
        :param form_type: Form type.
        """
        if last_status_flag:
            # Test UUID(irregular).
            self.fill_field('id___param_project_id', SET_SPECIAL_CODE)
            self.fill_field('id___param_user_id', SET_SPECIAL_CODE)
        else:
            # Test Email(irregular).
            self.fill_field('id___param_email', SET_SPECIAL_CODE)

        # Show confirm form and Submit.
        self._submit_confirm(form_type)

        self.wait_id(form_type)

        self.save_screenshot()

    def _test_new_project_contract_irregular_max_length_over(
            self, last_status_flag=False, form_type=FORM_CREATE):
        """Entry a 'New Project Contract' ticket.
        Max length error pattern.
        :param last_status_flag: Last status flag.
        :param form_type: Form type.
        """
        if last_status_flag:
            # Test UUID(over).
            name = u'\u3042' + ''.rjust(MAX_LENGTH_UUID - 1, 'a') + 'E'
            self.fill_field('id___param_project_id', name)
            self.fill_field('id___param_user_id', name)
        else:
            # Test Name(over).
            name = u'\u3042' + ''.rjust(MAX_LENGTH_NAME - 1, 'a') + 'E'
            self.fill_field('id___param_user_name', name)
            self.fill_field('id___param_project_name', name)

        # Test Message(over).
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1, 'a') + 'E'
        self.fill_field('id___param_message', message)

        # Show confirm form and Submit.
        self._submit_confirm(form_type)

        self.wait_id(form_type)

        self.save_screenshot()

    def _test_new_project_contract_entry(self, save_screen=True):
        """Entry a 'New Project Contract' ticket.
        :param save_screen: Save screenshot image.
        """
        time.sleep(SET_TIMEOUT)

        if save_screen:
            self.save_screenshot()

        # Success ticket entry form.
        # It is necessary for the entry to perform sleep for async processing.

        # Test Name.
        name = u'\u3042' + ''.rjust(MAX_LENGTH_NAME - len(
            SET_SPECIAL_CODE) - 1, 'a') + SET_SPECIAL_CODE
        self.fill_field('id___param_user_name', name)
        self.fill_field('id___param_project_name', name)
        # Test Email.
        self.fill_field('id___param_email', 'xxxxx@xxxxx.xxxxx')
        # Test Date.
        self.fill_field('id___param_preferred_date', SET_SPECIAL_CODE)
        # Test Message.
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - len(
            SET_SPECIAL_CODE) - 1, 'a') + SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        if save_screen:
            time.sleep(5)
            self.save_screenshot()

    # ==================================================

    def admin_new_project_contract_approval_canceled(self):
        """Update 'New Project Contract' status to canceled"""
        # Show ticket list form.
        self._admin_request_list()

        # Show detail form.
        self._click_ticket_list('request_list', 4, 1)
        # Update status.(id_approval_flg_2: canceled)
        self._update_request_from_detail('id_approval_flg_2')

    def admin_new_project_contract_approval_rejected(self):
        """Update 'New Project Contract' status to rejected by approval"""
        # Update status.(id_approval_flg_1: rejected)
        self._update_new_project_ticket(['id_approval_flg_1'], 11, 2)

    def admin_new_project_contract_approval_accepted_to_canceled(self):
        """Update 'New Project Contract' status to canceled"""
        # Update status.
        # (id_approval_flg_0: accepted, id_approval_flg_2: canceled)
        self._update_new_project_ticket(
            ['id_approval_flg_0', 'id_approval_flg_2'], 11, 3)

    def admin_new_project_contract_approval_accepted_to_rejected(self):
        """Update 'New Project Contract' status to rejected by approval"""
        # Update status.
        # (id_approval_flg_0: accepted, id_approval_flg_1: rejected)
        self._update_new_project_ticket(
            ['id_approval_flg_0', 'id_approval_flg_1'], 11, 4)

    def admin_new_project_contract_approval_working_to_canceled(self):
        """Update 'New Project Contract' status to canceled"""
        # Update status.
        # (id_approval_flg_0: accepted, id_approval_flg_0: working,
        #  id_approval_flg_2: canceled)
        self._update_new_project_ticket(
            ['id_approval_flg_0', 'id_approval_flg_0', 'id_approval_flg_2'],
            11, 5)

    def admin_new_project_contract_approval_working_to_rejected(self):
        """Update 'New Project Contract' status to rejected by approval"""
        # Update status.
        # (id_approval_flg_0: accepted, id_approval_flg_0: working,
        #  id_approval_flg_1: rejected)
        self._update_new_project_ticket(
            ['id_approval_flg_0', 'id_approval_flg_0', 'id_approval_flg_1'],
            11, 6)

    # ==================================================

    def admin_new_project_contract_approval_done(self):
        """Update 'New Project Contract' status to done"""
        # Update status.
        # (id_approval_flg_0: accepted, id_approval_flg_0: working)
        self._update_new_project_ticket(
            ['id_approval_flg_0', 'id_approval_flg_0'], 11, 7)

        # Show detail form.
        self._click_ticket_list('request_list', 11, 7)

        self._test_new_project_contract_irregular_required(FORM_UPDATE)
        self._test_new_project_contract_irregular_value(True, FORM_UPDATE)
        self._test_new_project_contract_irregular_max_length_over(
            True, FORM_UPDATE)
        self._cancel_request()

        # Update status.(id_approval_flg_0: done)
        self._update_new_project_ticket(['id_approval_flg_0'], 11, 7, True)

    # ==================================================

    def project_cancel_project_contract_entry(self):
        """Entry a 'Cancel Project Contract' ticket.
        Required error pattern.
        """
        self._project_contract_list(True)

        # Add Cancel Project Contract.
        self._click_ticket_list('contracts', 7, 1)
        self._test_cancel_project_contract_irregular_required()
        self._test_cancel_project_contract_irregular_max_length_over()
        self._cancel_request()

        # Create 3 ticket.(Cancel Project Contract)
        #  Root 1: [Cancel Project Contract] -> Canceled
        #  Root 2: [Cancel Project Contract] -> Rejected
        #  Root 3: [Cancel Project Contract] -> Final Approval
        for row_idx in range(3):
            if row_idx == 0:
                self._click_ticket_list('contracts', 2, 1)
                self.click_css('a.btn-edit')
                self._test_cancel_project_contract_entry(True)
            else:
                self._click_ticket_list('contracts', 7, 1)
                self._test_cancel_project_contract_entry(False)

    def _test_cancel_project_contract_irregular_required(
            self, form_type=FORM_CREATE):
        """Entry a 'Cancel Project Contract' ticket.
        Required error pattern.
        :param form_type: Form type.
        """
        # Show confirm form and Submit.
        self._submit_confirm(form_type)

        self.wait_id(form_type)

        self.save_screenshot()

    def _test_cancel_project_contract_irregular_max_length_over(
            self, form_type=FORM_CREATE):
        """Entry a 'Cancel Project Contract' ticket.
        Max length error pattern.
        :param form_type: Form type.
        """
        # Test Message(over).
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1, 'a') + 'E'
        self.fill_field('id___param_message', message)

        # Show confirm form and Submit.
        self._submit_confirm(form_type)

        self.wait_id(form_type)

        self.save_screenshot()

    def _test_cancel_project_contract_entry(self, save_screen=True):
        """Entry a 'Cancel Project Contract' ticket.
        :param save_screen: Save screenshot image.
        """
        time.sleep(SET_TIMEOUT)

        if save_screen:
            self.save_screenshot()

        # Success ticket entry form.
        # It is necessary for the entry to perform sleep for async processing.

        # Test Date.
        self.fill_field('id___param_preferred_date', SET_SPECIAL_CODE)
        # Test Message.
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - len(
            SET_SPECIAL_CODE) - 1, 'a') + SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        if save_screen:
            time.sleep(5)
            self.save_screenshot()

    # ==================================================

    def project_cancel_project_contract_canceled(self):
        """Update 'Cancel Project Contract' status to canceled"""
        # Show ticket list form.
        self._project_ticket_list()

        # Show detail form.
        self._click_ticket_list('ticket_list', 3, 1)

        # Update status.(id_approval_flg_0: canceled)
        self._update_ticket_from_detail('id_approval_flg_0')

    def project_cancel_project_contract_approval_rejected(self):
        """Update 'Cancel Project Contract' status to rejected"""
        # Show ticket list form.
        self._project_ticket_list()

        # Update status.(id_approval_flg_1: rejected)
        self._update_ticket_list(2, 'id_approval_flg_1', True)

    # ==================================================

    def project_cancel_project_contract_approval_final_approval(self):
        """Update 'Cancel Project Contract' status to final approval"""
        # Show detail form.
        self._click_ticket_list('ticket_list', 10, 3)

        self._test_cancel_project_contract_irregular_required(FORM_UPDATE)
        self._test_cancel_project_contract_irregular_max_length_over(
            FORM_UPDATE)
        self._cancel_request()

        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(3, 'id_approval_flg_0', True, True)

    # ==================================================

    def admin_project_list_confirm(self):
        """Show ticket list form of admin"""
        # Show ticket list form.
        self.trans_and_wait('admin_ticket_list', '/admin/ticket_list/')

        self.save_screenshot()

        # Show detail form.
        self._click_ticket_list('admin_ticket_list', 4, 1)

        self.save_screenshot()

    # ==================================================

    def _project_ticket_templates_list(self, save_screen=True):
        """Show ticket template list form.
        :param save_screen: Save screenshot image.
        """
        # Show ticket template form.
        self.trans_and_wait(
            'tickettemplates', '/project/ticket_templates/?tab=' + TAB_NAME)

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

    def _project_ticket_list(self, save_screen=True):
        """Show ticket list form of project.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('ticket_list', '/project/ticket_list/')

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

    def _project_contract_list(self, save_screen=True):
        """Show contract list form of admin.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('contracts', '/project/contracts/')

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

    def _admin_request_list(self, save_screen=True):
        """Show ticket list form of admin.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('request_list', '/admin/request_list/')

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

    def _project_new_project_contract_form_show(
            self, ticket_template_id, form_id):
        """Show entry form from ticket list of project.
        :param ticket_template_id: Ticket template id.
        :param form_id: The Id of form tag.
        """
        self.click_css(
            ('#%s #tickettemplates__row__%s > td.anchor.normal_column > a') % (
                TAB_NAME, ticket_template_id))
        self.wait_id(form_id)

    def _click_ticket_list(self, table_id, col_idx=1, row_idx=1):
        """Show issued requests list form.
        :param table_id: Target table id.
        :param col_idx: Column index.
        :param row_idx: Row index.
        """
        self.click_css(
            ('#%s > tbody > tr:nth-child(%s) > td:nth-child(%s) > a') % (
                table_id, row_idx, col_idx))

        time.sleep(SET_TIMEOUT)

        self.save_screenshot()

    def _cancel_request(self):
        """Close request form"""
        self.click_css('div#None.modal.in a.close')

        time.sleep(SET_TIMEOUT)

        self.save_screenshot()

    def _submit_confirm(self, form_id):
        """Show confirm form and Submit.
        :param form_id: The Id of form tag.
        """
        time.sleep(SET_TIMEOUT)
        self.wait_css('#%s input.btn-primary' % form_id)
        self.click_css('#%s input.btn-primary' % form_id)
        self.click_css('div.modal.aflo_confirm_dialog a.btn-primary')

    def _update_request_from_detail(self, next_status_value, done_flg=False):
        """Update a request from detail form.
        :param next_status_value: Change a status to value.
        :param done_flg: Next status is done.
        """
        self.click_css('a.btn-edit')
        self._update_request(next_status_value, done_flg)

    def _update_new_project_ticket(
            self, update_status_values, col_idx=1, row_idx=1, done_flg=False):
        """Update new project ticket.
        :param update_status_values: Update status values.
        :param col_idx: Column index.
        :param row_idx: Row index.
        :param done_flg: Next status is done.
        """
        for update_status_value in update_status_values:
            # Show detail form.
            self._click_ticket_list('request_list', col_idx, row_idx)
            # Update status.
            self._update_request(update_status_value, done_flg)

    def _update_request(self, next_status_value, done_flg=False):
        """Update a request.
        :param next_status_value: Change a status to value.
        :param done_flg: Next status is done.
        """
        self.wait_id(FORM_UPDATE, SET_TIMEOUT)

        if done_flg:
            # Test UUID.
            self.fill_field('id___param_project_id', DEMO_PROJECT_ID)
            self.fill_field('id___param_user_id', DEMO_USER_ID)
            # Test Date.
            self.fill_field('id___param_join_date', SET_SPECIAL_CODE)

        # Test Message.
        message = u'\u3042' + ''.rjust(
            MAX_LENGTH_MESSAGE - len(SET_SPECIAL_CODE) - 1, 'a') + \
            SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        self.selenium.execute_script(
            'document.getElementById("%s").click();' % next_status_value)

        time.sleep(SET_TIMEOUT)

        self.save_screenshot()

        self._submit_confirm(FORM_UPDATE)
        time.sleep(5)

        self.save_screenshot()

    def _update_ticket_list(
            self, row_idx, next_status_value, save_screen=True,
            final_approval_flg=False):
        """Update a ticket from ticket list form.
        :param row_idx: Set row index of ticket list form.
        :param next_status_value: Change a status to value.
        :param save_screen: Save screenshot image.
        :param final_approval_flg: Next status is final approval.
        """
        self._click_ticket_list('ticket_list', 10, row_idx)

        self._update_ticket(next_status_value, save_screen, final_approval_flg)

    def _update_ticket_from_detail(self, next_status_value, save_screen=True,
                                   final_approval_flg=False):
        """Update a ticket from detail form.
        :param next_status_value: Change a status to value.
        :param save_screen: Save screenshot image.
        :param final_approval_flg: Next status is final approval.
        """
        self.click_css('a.btn-edit')

        self._update_ticket(next_status_value, save_screen, final_approval_flg)

    def _update_ticket(self, next_status_value, save_screen=True,
                       final_approval_flg=False):
        """Update a ticket.
        :param next_status_value: Change a status to value.
        :param save_screen: Save screenshot image.
        :param final_approval_flg: Next status is final approval.
        """
        self.wait_id(FORM_UPDATE, SET_TIMEOUT)

        if final_approval_flg:
            # Test Date.
            self.fill_field('id___param_withdrawal_date', FORM_UPDATE)

        # Test Message.
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - len(
            SET_SPECIAL_CODE) - 1, 'a') + SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        self.selenium.execute_script(
            'document.getElementById("%s").click();' % next_status_value)

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

        self._submit_confirm(FORM_UPDATE)

        if save_screen:
            time.sleep(5)
            self.save_screenshot()

    # ==================================================

    def delete_data(self):
        """Delete test data"""
        self._execute_sql('delete from contract;')
        self._execute_sql('delete from workflow;')
        self._execute_sql('delete from ticket;')
