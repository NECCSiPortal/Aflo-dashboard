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

"""Test 'Request Change Contract' on Aflo.
Please operate setting.
  Step1. Create Projects
    - admin
    - demo
  Step2. Create Users
    - admin
    - demo
  Step3. Create Roles
    - admin
      Grant: [admin] project - [admin] user
    - C__Global__ProjectAdmin
      Grant: [admin] project - [admin] user
    - T__<Region Name>__ProjectMember
      Grant: [admin] project - [demo] user
             [demo] project - [demo] user does not have this role.
  Step4. Create Catalogs
    Create Goods, Catalog, Catalog Contents, Price and Catalog Scope.
    - VCPU x 10 CORE(S)
    - RAM 20 GB
    - Volume Storage 50 GB
    - VCPU
    - RAM
    - Volume Storage
  Step5. Create Workflows
    Create Ticket Template and Workflow Pattern.
    - New Flat-rate Contract
    - Cancel Flat-rate Contract
    - New Pay-for-use Contract
    - Cancel Pay-for-use Contract
    - Change To Flat-rate Contract
    - Change To Pay-for-use Contract
  Step6. Change Selenium Parameters
    - SET_BASE_URL
    - DB_USER
    - DB_PASS
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
    #  Project user.(not unauthorized users)
    'sign_in_demo',
    'change_setting',
    'project_change_contract_registration_entry_not_unauthorized_users',
    'sign_out',
    #  Project user.(pay-for-use contract)
    'sign_in_demo_project_admin',
    'project_change_to_flatrate_registration_entry_does_not_exist_contract',
    'project_change_to_payforuse_registration_entry_does_not_exist_contract',
    # Pay-for-use registration.
    'project_payforuse_registration_entry',
    'sign_out',
    #  Approval user.(pay-for-use contract)
    'sign_in_admin',
    'project_payforuse_registration_approval_final_approval',
    'project_show_contract_list',
    'project_show_overview',
    'sign_out',
    #  Project user.(change to flat-rate contract)
    'sign_in_demo_project_admin',
    'project_change_to_payforuse_registration_entry_double_contract',
    # Change to flat-rate registration.
    'project_change_to_flatrate_registration_entry',
    'project_change_to_flatrate_registration_approval_canceled',
    'sign_out',
    #  Approval user.(change to flat-rate contract)
    'sign_in_admin',
    'project_change_to_flatrate_registration_approval_rejected',
    'project_change_to_flatrate_registration_approval_final_approval',
    'project_change_to_flatrate_registration_approval_double_contract',
    'project_show_contract_list',
    'project_show_overview',
    'admin_project_list_confirm',
    'sign_out',
    #  Project user.(flat-rate contract)
    'sign_in_demo_project_admin',
    'project_change_to_flatrate_registration_entry_double_contract',
    # Flat-rate registration.
    'project_flatrate_registration_entry',
    'sign_out',
    #  Approval user.(flat-rate contract)
    'sign_in_admin',
    'project_flatrate_registration_approval_final_approval',
    'project_show_contract_list',
    'project_show_overview',
    'sign_out',
    # Project user.(change to pay-for-use contract)
    'sign_in_demo_project_admin',
    # Change to pay-for-use registration.
    'project_change_to_payforuse_registration_entry',
    'project_change_to_payforuse_registration_approval_canceled',
    'sign_out',
    # Approval user.(change pay-for-use contract)
    'sign_in_admin',
    'project_change_to_payforuse_registration_approval_rejected',
    'project_change_to_payforuse_registration_approval_final_approval',
    'project_change_to_payforuse_registration_approval_double_contract',
    'project_show_contract_list',
    'project_show_overview',
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

TAB_NAME = 'ticket_templates_group_tabs__contract_tab'

TICKET_TEMPLATE_ID_FLATRATE_REGISTRATION = '10'
TICKET_TEMPLATE_ID_PAYFORUSE_REGISTRATION = '15'
TICKET_TEMPLATE_ID_CHANGE_FLATRATE = '40'
TICKET_TEMPLATE_ID_CHANGE_PAYFORUSE = '41'

MAX_LENGTH_GOODS_NUMBER_MAX = 4
MAX_LENGTH_MESSAGE = 512

FORM_CREATE = 'create_form'
FORM_UPDATE = 'update_form'


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

    def sign_in_demo(self):
        """Sign in demo user"""
        self._sign_in('demo', 'demo')

    def sign_in_demo_project_admin(self):
        """Sign in demo user of admin project"""
        self._sign_in('demo', 'admin')

    def sign_in_admin(self):
        """Sign in demo user"""
        self._sign_in('admin', 'admin')

    def _sign_in(self, username='admin', project='admin'):
        """Sign in"""
        # Run a sign-in
        self.trans_and_wait('loginBtn', '')

        self.fill_field('id_username', SET_USER.get(username).get('USERNM'))
        self.fill_field('id_password', SET_USER.get(username).get('PASSWORD'))

        self.click_id('loginBtn')

        if username == 'demo' and project == 'demo':
            self._project_overview(False)

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

    def project_change_contract_registration_entry_not_unauthorized_users(
            self):
        """Not unauthorized users.
        Entry a 'Change Contract Registration' ticket.
        """
        self._project_ticket_templates_list(True)

    def project_change_to_flatrate_registration_entry_does_not_exist_contract(
            self):
        """Does not exist contract.
        Entry a 'Change To Flat-rate Contract Registration' ticket.
        """
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_CHANGE_FLATRATE,
            FORM_CREATE)

        self._test_flatrate_registration_entry(True)

    def project_change_to_payforuse_registration_entry_does_not_exist_contract(
            self):
        """Does not exist contract.
        Entry a 'Change To Pay-for-use Contract Registration' ticket.
        """
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_CHANGE_PAYFORUSE,
            FORM_CREATE)

        self._test_payforuse_registration_entry(True)

    # ==================================================

    def project_payforuse_registration_entry(self):
        """Entry a 'Pay-for-use Registration' ticket"""
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_PAYFORUSE_REGISTRATION,
            FORM_CREATE)

        self._test_payforuse_registration_entry(True)

    def _test_payforuse_registration_entry(self, save_screen=True):
        """Entry a 'Pay-for-use Registration' ticket.
        :param save_screen: Save screenshot image.
        """
        time.sleep(SET_TIMEOUT)

        if save_screen:
            self.save_screenshot()

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

    def project_payforuse_registration_approval_final_approval(self):
        """Update 'Pay-for-use Registration' status to final approval"""
        # Show ticket list form.
        self._project_ticket_list(True)
        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(1, 'id_approval_flg_0')

    # ==================================================

    def project_show_contract_list(self):
        """Show contract list"""
        self._project_contract_list(True)

    def project_show_overview(self):
        """Show overview"""
        self._project_overview(True)

    # ==================================================

    def project_change_to_payforuse_registration_entry_double_contract(self):
        """Create 'Change To Pay-for-use Registration' double contract error"""
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_CHANGE_PAYFORUSE,
            FORM_CREATE)

        self._test_payforuse_registration_entry(True)

    # ==================================================

    def project_change_to_flatrate_registration_entry(self):
        """Entry a 'Change To Flat-rate Registration' ticket"""
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_CHANGE_FLATRATE,
            FORM_CREATE)
        self._test_change_to_flatrate_registration_irregular_required()
        self._test_change_to_flatrate_registration_irregular_value()
        self._test_change_to_flatrate_registration_irregular_max_length_over()
        self._cancel_request()

        # Create 4 ticket.(Registration)
        #  Root 1: [Registration] -> Canceled
        #  Root 2: [Registration] -> Rejected
        #  Root 3: [Registration] -> Final Approval
        #  Root 4: [Registration] -> Double Contract
        for i in range(4):
            save_screen = True if i == 0 else False

            self._project_registration_form_show(
                TICKET_TEMPLATE_ID_CHANGE_FLATRATE,
                FORM_CREATE)
            self._test_flatrate_registration_entry(save_screen)

    def _test_change_to_flatrate_registration_irregular_required(self):
        """Entry a 'Change To Flat-rate Registration' ticket.
        Required error pattern.
        """
        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        self.wait_id(FORM_CREATE)

        self.save_screenshot()

    def _test_change_to_flatrate_registration_irregular_value(self):
        """Entry a 'Change To Flat-rate Registration' ticket.
        Value error pattern.
        """
        input_values = [SET_SPECIAL_CODE, '-1', '0.1']

        for number in input_values:
            self.fill_field('id___param_vcpu', number)
            self.fill_field('id___param_ram', number)
            self.fill_field('id___param_volume_storage', number)

            # Show confirm form and Submit.
            self._submit_confirm(FORM_CREATE)

            self.wait_id(FORM_CREATE)

            self.save_screenshot()

    def _test_change_to_flatrate_registration_irregular_max_length_over(self):
        """Entry a 'Change To Flat-rate Registration' ticket.
        Max length error pattern.
        """
        # Test goods number.(over)
        number = int(''.rjust(MAX_LENGTH_GOODS_NUMBER_MAX, '9')) + 1
        self.fill_field('id___param_vcpu', number)
        self.fill_field('id___param_ram', number)
        self.fill_field('id___param_volume_storage', number)

        # Test Message.(over)
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1, 'a') + 'E'
        self.fill_field('id___param_message', message)

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        self.wait_id(FORM_CREATE)

        self.save_screenshot()

    def _test_flatrate_registration_entry(self, save_screen=True):
        """Entry a 'Flat-rate Registration' ticket.
        :param save_screen: Save screenshot image.
        """
        time.sleep(SET_TIMEOUT)

        if save_screen:
            self.save_screenshot()

        # Test goods number.(over)
        number = int(''.rjust(MAX_LENGTH_GOODS_NUMBER_MAX, '9'))
        self.fill_field('id___param_vcpu', number)
        self.fill_field('id___param_ram', number)
        self.fill_field('id___param_volume_storage', number)

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

    def project_change_to_flatrate_registration_approval_canceled(self):
        """Update 'Change To Flat-rate Registration'
        status to canceled.
        """
        # Show ticket list form.
        self._project_ticket_list()
        # Show detail form.
        self._click_ticket_list('ticket_list', 3, 1)
        # Update status.(id_approval_flg_0: canceled)
        self._update_project_ticket_from_detail('id_approval_flg_0')

    def project_change_to_flatrate_registration_approval_rejected(self):
        """Update 'Change To Flat-rate Registration'
        status to rejected.
        """
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_1: rejected)
        self._update_ticket_list(2, 'id_approval_flg_1')

    def project_change_to_flatrate_registration_approval_final_approval(self):
        """Update 'Change To Flat-rate Registration'
        status to final approval.
        """
        # Show ticket list form.
        self._project_ticket_list()

        self._click_ticket_list('ticket_list', 10, 3)
        self._test_change_contract_approval_irregular_max_length_over()
        self._cancel_request()

        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(3, 'id_approval_flg_0')

    def _test_change_contract_approval_irregular_max_length_over(self):
        """Entry a 'Change Contract Approval' ticket.
        Max length error pattern.
        """
        # Test Message.(over)
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1, 'a') + 'E'
        self.fill_field('id___param_message', message)

        # Show confirm form and Submit.
        self._submit_confirm(FORM_UPDATE)

        self.wait_id(FORM_UPDATE)

        self.save_screenshot()

    def project_change_to_flatrate_registration_approval_double_contract(self):
        """Update 'Change To Flat-rate Registration'
        double contract error of approval.
        """
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(4, 'id_approval_flg_0')

    # ==================================================

    def project_change_to_flatrate_registration_entry_double_contract(self):
        """Create 'Change To Flat-rate Registration' double contract error"""
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_CHANGE_FLATRATE, FORM_CREATE)

        self._test_flatrate_registration_entry(True)

    # ==================================================

    def project_flatrate_registration_entry(self):
        """Entry a 'Flat-rate Registration' ticket"""
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_FLATRATE_REGISTRATION, FORM_CREATE)

        self._test_flatrate_registration_entry(True)

    # ==================================================

    def project_flatrate_registration_approval_final_approval(self):
        """Update 'Flat-rate Registration' status to final approval"""
        # Show ticket list form.
        self._project_ticket_list(True)
        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(1, 'id_approval_flg_0')

    # ==================================================

    def project_change_to_payforuse_registration_entry(self):
        """Entry a 'Change To Pay-for-use Registration' ticket"""
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_CHANGE_PAYFORUSE,
            FORM_CREATE)
        self._test_change_to_payforuse_registration_irregular_max_length_over()
        self._cancel_request()

        # Create 4 ticket.(Registration)
        #  Root 1: [Registration] -> Canceled
        #  Root 2: [Registration] -> Rejected
        #  Root 3: [Registration] -> Final Approval
        #  Root 4: [Registration] -> Double Contract
        for i in range(4):
            save_screen = True if i == 0 else False

            self._project_registration_form_show(
                TICKET_TEMPLATE_ID_CHANGE_PAYFORUSE,
                FORM_CREATE)
            self._test_payforuse_registration_entry(save_screen)

    def _test_change_to_payforuse_registration_irregular_max_length_over(self):
        """Entry a 'Change To Pay-for-use Registration' ticket.
        Max length error pattern.
        """
        # Test Message.(over)
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1, 'a') + 'E'
        self.fill_field('id___param_message', message)

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        self.wait_id(FORM_CREATE)

        self.save_screenshot()

    # ==================================================

    def project_change_to_payforuse_registration_approval_canceled(self):
        """Update 'Change To Pay-for-use Registration'
        status to canceled.
        """
        # Show ticket list form.
        self._project_ticket_list()
        # Show detail form.
        self._click_ticket_list('ticket_list', 3, 1)
        # Update status.(id_approval_flg_0: canceled)
        self._update_project_ticket_from_detail('id_approval_flg_0')

    def project_change_to_payforuse_registration_approval_rejected(self):
        """Update 'Change To Pay-for-use Registration'
        status to rejected.
        """
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_1: rejected)
        self._update_ticket_list(2, 'id_approval_flg_1')

    def project_change_to_payforuse_registration_approval_final_approval(self):
        """Update 'Change To Pay-for-use Registration'
        status to final approval.
        """
        # Show ticket list form.
        self._project_ticket_list()

        self._click_ticket_list('ticket_list', 10, 3)
        self._test_change_contract_approval_irregular_max_length_over()
        self._cancel_request()

        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(3, 'id_approval_flg_0')

    def project_change_to_payforuse_registration_approval_double_contract(
            self):
        """Update 'Change To Pay-for-use Registration'
        double contract error of approval.
        """
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(4, 'id_approval_flg_0')

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
        """Show contract list form of project.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('contracts', '/project/contracts/')

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

    def _project_overview(self, save_screen=True):
        """Show overview form of project.
        :param save_screen: Save screenshot image.
        """
        # Show overview form.
        self.trans_and_wait('project_usage', '/project/overview/')

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

    def _project_registration_form_show(self, ticket_template_id, form_id):
        """Show entry form from ticket list of project.
        :param ticket_template_id: Ticket template id.
        :param form_id: The Id of form tag.
        """
        self.click_css((
            '#%s #tickettemplates__row__%s > ' +
            ' td.anchor.normal_column > a') %
            (TAB_NAME, ticket_template_id))

        self.wait_id(form_id)

    def _click_ticket_list(self, table_id, col_idx=1, row_idx=1):
        """Show issued requests list form.
        :param table_id: Target table id.
        :param col_idx: Column index.
        :param row_idx: Row index.
        """
        self.click_css((
            '#%s > tbody > tr:nth-child(%s) > ' + ' td:nth-child(%s) > a') % (
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

    def _update_ticket_list(
            self, row_idx, next_status_flg, save_screen=True):
        """Update a ticket from ticket list form.
        :param row_idx: Set row index of ticket list form.
        :param next_status_flg: Change a status to value.
        :param save_screen: Save screenshot image.
        """
        self._click_ticket_list('ticket_list', 10, row_idx)
        self._update_ticket(next_status_flg, save_screen)

    def _update_project_ticket_from_detail(self,
                                           next_status_value,
                                           save_screen=True):
        """Update a ticket from detail form.
        :param next_status_value: Change a status to value.
        :param save_screen: Save screenshot image.
        """
        self.click_css('a.btn-edit')
        self._update_ticket(next_status_value, save_screen)

    def _update_ticket(self, next_status_value, save_screen=True):
        """Update a ticket.
        :param next_status_value: Change a status to value.
        :param save_screen: Save screenshot image.
        """
        self.wait_id(FORM_UPDATE)

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
