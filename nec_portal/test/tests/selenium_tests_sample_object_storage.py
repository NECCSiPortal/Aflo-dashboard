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

"""Test 'Request Object Storage Contract' on Aflo.
Please operate setting.
  Step1. Create Projects
    - admin
    - demo
  Step2. Create Users
    - admin
    - p_admin
    - demo
  Step3. Create Roles
    - admin
      Grant: [demo] project - [admin] user
    - C__Global__ProjectAdmin
      Grant: [demo] project - [p_admin] user
    - T__<Region Name>__ProjectMember
      Grant: [demo] project - [demo] user
    - T__<Region Name>__ObjectStore
      Grant: no set
  Step4. Create Catalogs
    Create Goods, Catalog, Catalog Contents, Price and Catalog Scope.
    - Object Storage
  Step5. Create Workflows
    Create Ticket Template and Workflow Pattern.
    - New Object Storage Contract
    - Cancel Object Storage Contract
  Step6. Change Selenium Parameters
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
# Login user
SET_USER = {
    'admin': {
        'USERNM': 'admin',
        'PASSWORD': 'xxxx'
    },
    'p_admin': {
        'USERNM': 'p_admin',
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
    # Object Storage registration.
    #  Admin user.(not_unauthorized_users)
    'sign_in_contract_admin',
    'change_setting',
    'project_contract_registration_entry_not_unauthorized_users',
    'sign_out',
    #  Project user.
    'sign_in_project_user',
    'project_contract_registration_entry',
    'project_contract_registration_canceled',
    'sign_out',
    #  Approval user.
    'sign_in_project_admin',
    'project_contract_registration_approval_final_approval',
    'project_contract_registration_approval_rejected',
    'project_contract_registration_approval_double_contract',
    'project_contract_cancelling_entry_not_unauthorized_users',
    'sign_out',
    #  Admin user.(check result)
    'sign_in_contract_admin',
    'project_contract_registration_success',
    'sign_out',
    #  Project user.(double contract error)
    'sign_in_project_user',
    'project_contract_registration_entry_double_contract',
    # Object Storage cancelling.
    #  Project user.
    'project_contract_cancelling_irregular_entry',
    'project_contract_cancelling_entry',
    'project_contract_cancelling_canceled',
    'sign_out',
    #  Approval user.
    'sign_in_project_admin',
    'project_contract_cancelling_approval_final_approval',
    'project_contract_cancelling_approval_rejected',
    'project_contract_cancelling_approval_double_cancelling',
    'sign_out',
    #  Admin user.(check result)
    'sign_in_contract_admin',
    'project_contract_registration_success',
    # View ticket list of admin menu.
    #  Admin user.
    'admin_project_list_confirm',
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

TICKET_TEMPLATE_ID_OST_REGISTRATION = '17'

MAX_LENGTH_MESSAGE = 512

FORM_CREATE = 'create_form'
FORM_UPDATE = 'update_form'

DEMO_PROJECT_ID = 'adb27177f0d449888f42a3625b9eb3d1'
DEMO_USER_ID = '5ee7d7bcb71444a6891abf6ad240952d'


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
                       ":" + e.message)
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
        self.selenium.get(SET_BASE_URL + urlpath)
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
        self.selenium.find_element_by_name(field_name).send_keys(value)

    def fill_field_clear(self, field_id):
        """Clear to the field"""
        self.selenium.find_element_by_id(field_id).clear()

    def fill_field_clear_by_name(self, field_name):
        """Clear to the field"""
        self.selenium.find_element_by_name(field_name).clear()

    def click_id(self, element_id):
        """Click on the button"""
        element = self.selenium.find_element_by_id(element_id)
        element.click()

    def click_css(self, css, timeout=SET_TIMEOUT):
        """Click on the button css(no wait)"""
        element = self.selenium.find_element_by_css_selector(css)
        element.click()

    def click_xpath_and_ajax_wait(self, xpath, timeout=SET_TIMEOUT):
        """Click on the button xpath ajax wait"""
        element = self.selenium.find_element_by_xpath(xpath)
        element.click()
        self.wait_ajax(timeout)

    def set_select_value(self, element_id, value):
        """Set of pull-down menu by value"""
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

    def sign_in_project_admin(self):
        """Sign in admin user"""
        self._sign_in('p_admin', 'demo')

    def sign_in_project_user(self):
        """Sign in project user"""
        self._sign_in('demo', 'demo')

    def sign_in_contract_admin(self):
        """Sign in project user"""
        self._sign_in('admin', 'demo')

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

    def project_contract_registration_entry_not_unauthorized_users(self):
        """No unauthorized users.
        Entry a 'Object Storage Registration' ticket.
        """
        self._project_ticket_templates_list(True)
        time.sleep(SET_TIMEOUT)
        self.save_screenshot()

    def project_contract_registration_entry(self):
        """Entry a 'Object Storage Registration' ticket"""
        self._project_ticket_templates_list(True)

        # Add New Contract.
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_OST_REGISTRATION,
            FORM_CREATE)
        self._test_contract_registration_irregular_max_length_over()
        self._cancel_request()

        # Create 3 ticket.(registration and cancelling)
        #  Root 1: [Registration] -> Final Approval ->
        #          [Cancelling]   -> Final Approval
        #          [Cancelling]   -> Canceled
        #          [Cancelling]   -> Rejected
        #          [Cancelling]   -> Double contract error
        #  Root 2: [Registration] -> Canceled
        #  Root 3: [Registration] -> Rejected
        #  Root 4: [Registration] -> Double contract error
        for i in range(4):
            save_screen = True if i == 0 else False

            self._project_registration_form_show(
                TICKET_TEMPLATE_ID_OST_REGISTRATION,
                FORM_CREATE)
            self._test_contract_registration_entry(save_screen)

    def _test_contract_registration_irregular_max_length_over(self):
        """Entry a 'Object Storage Registration' ticket.
        Max length error pattern.
        """
        # Test Message(over).
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1,
                                       'a') + 'E'
        self.fill_field('id___param_message', message)
        self.save_screenshot()
        self.wait_id(FORM_CREATE)

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)
        time.sleep(SET_TIMEOUT)
        self.save_screenshot()

    def _test_contract_registration_entry(self, save_screen=True):
        """Entry a 'Object Storage Registration' ticket.
        :param save_screen: Save screenshot image.
        """
        if save_screen:
            self.save_screenshot()

        # Test Message.
        message = u'\u3042' + ''.rjust(
            MAX_LENGTH_MESSAGE - len(SET_SPECIAL_CODE) - 1, 'a') + \
            SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        if save_screen:
            self.save_screenshot()

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)
        self.wait_id('tickettemplates__row__%s' %
                     TICKET_TEMPLATE_ID_OST_REGISTRATION)
        time.sleep(SET_TIMEOUT)

        if save_screen:
            self.save_screenshot()

    # ==================================================

    def project_contract_registration_canceled(self):
        """Update 'Object Storage Registration' status to canceled"""
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_0: canceled)
        self._update_ticket_list(2, 'id_approval_flg_0')

    def project_contract_registration_approval_rejected(self):
        """Update 'Object Storage Registration' status to rejected"""
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_1: rejected)
        self._update_ticket_list(3, 'id_approval_flg_1')

    # ==================================================

    def project_contract_registration_approval_final_approval(self):
        """Update 'Object Storage Registration' status to final approval"""
        # Show ticket list form.
        self._project_ticket_list()
        # Show detail form.
        self._click_ticket_list('ticket_list', 3, 4)
        # Update status.(id_approval_flg_0: final approval)
        self._update_project_ticket_from_detail('id_approval_flg_0')

    # ==================================================

    def project_contract_registration_success(self):
        """Show role of Identity menu projects"""
        self.trans_and_wait('tenants', '/identity/')
        self.click_css('#tenants__row_%s__action_users' % DEMO_PROJECT_ID)
        time.sleep(SET_TIMEOUT)
        self.click_css(
            'li[data-update_members-id=id_update_members_%s] ~ li ~ li a' %
            DEMO_USER_ID)
        time.sleep(SET_TIMEOUT)
        self.save_screenshot()

    # ==================================================

    def project_contract_registration_approval_double_contract(self):
        """Update 'Object Storage Registration' double contract error test"""
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_0: final approval)
        self._update_ticket_list(1, 'id_approval_flg_0')

    # ==================================================

    def project_contract_cancelling_entry_not_unauthorized_users(self):
        """Not unauthorized_users Entry
        a 'Object Storage Cancelling' ticket.
        """
        self._project_contract_list(True)

    # ==================================================

    def project_contract_registration_entry_double_contract(self):
        """Create 'Object Storage Registration' double contract error test"""
        self._project_ticket_templates_list(True)
        self._project_registration_form_show(
            TICKET_TEMPLATE_ID_OST_REGISTRATION,
            FORM_CREATE)
        save_screen = True
        self._test_contract_registration_entry(save_screen)

    # ==================================================

    def project_contract_cancelling_irregular_entry(self):
        """Entry a 'Object Storage Cancelling' ticket.
        Required error pattern.
        """
        self._project_contract_list(True)
        self._click_ticket_list('contracts', 7, 1)
        self._test_contract_cancelling_irregular_max_length_over()

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)
        time.sleep(SET_TIMEOUT)
        self.save_screenshot()

        self._cancel_request()

    # ==================================================

    def project_contract_cancelling_entry(self):
        """Entry a 'Object Storage Cancelling' ticket"""
        self._project_contract_list(True)
        self._click_ticket_list('contracts', 2, 1)
        self.click_css('a.btn-edit')
        self._test_contract_cancelling_entry(True)

        # Create 3 ticket.(cancelling)
        #  Root 1: [Cancelling]   -> Final Approval
        #  Root 2: [Cancelling]   -> Canceled
        #  Root 3: [Cancelling]   -> Rejected
        for i in range(3):
            self._click_ticket_list('contracts', 7, 1)
            if i == 0:
                self._test_contract_cancelling_entry(True)
            else:
                self._test_contract_cancelling_entry(False)

    # ==================================================

    def _test_contract_cancelling_irregular_max_length_over(self):
        """Entry a 'Object Storage Cancelling' ticket.
        Max length error pattern.
        """
        # Test Message(over).
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1,
                                       'a') + 'E'
        self.fill_field('id___param_message', message)
        self.wait_id(FORM_CREATE)
        self.save_screenshot()

    def _test_contract_cancelling_entry(self, save_screen=True):
        """Entry a 'Object Storage Cancelling' ticket.
        :param save_screen: Save screenshot image.
        """
        if save_screen:
            self.save_screenshot()

        # Test Message.
        message = u'\u3042' + ''.rjust(
            MAX_LENGTH_MESSAGE - len(SET_SPECIAL_CODE) - 1, 'a') + \
            SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)
        if save_screen:
            self.save_screenshot()

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

    # ==================================================

    def project_contract_cancelling_approval_final_approval(self):
        """Update 'Object Storage Cancelling' status to final approval"""
        # Show ticket list form.
        self._project_ticket_list()
        # Show detail form.
        self._click_ticket_list('ticket_list', 3, 1)
        # Update status.(id_approval_flg_0: final approval)
        self._update_project_ticket_from_detail('id_approval_flg_0')
        time.sleep(SET_TIMEOUT)

    # ==================================================

    def project_contract_cancelling_canceled(self):
        """Update 'Object Storage Cancelling' status to canceled"""
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_0: canceled)
        self._update_ticket_list(2, 'id_approval_flg_0')

    # ==================================================

    def project_contract_cancelling_approval_rejected(self):
        """Update 'Object Storage Cancelling' status to rejected"""
        # Show ticket list form.
        self._project_ticket_list()
        # Update status.(id_approval_flg_1: rejected)
        self._update_ticket_list(3, 'id_approval_flg_1')

    # ==================================================

    def project_contract_cancelling_approval_double_cancelling(self):
        """Update 'Object Storage Cancelling' status to final approval"""
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
            self.save_screenshot()

    def _project_ticket_list(self, save_screen=True):
        """Show ticket list form of project.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('ticket_list', '/project/ticket_list/')
        if save_screen:
            self.save_screenshot()

    def _project_contract_list(self, save_screen=True):
        """Show contract list form of admin.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('contracts', '/project/contracts/')
        if save_screen:
            self.save_screenshot()

    def _project_registration_form_show(
            self, ticket_template_id, form_id):
        """Show entry form from ticket list of project.
        :param ticket_template_id: Ticket template id.
        :param form_id: The Id of form tag.
        """
        self.click_css((
            '#%s #tickettemplates__row__%s > ' +
            ' td.anchor.normal_column > a') %
            (TAB_NAME, ticket_template_id))
        self.wait_id(form_id)

    def _click_ticket_list(self, table_id, col_idx=1, row_idx=1,
                           save_screen=True):
        """Show issued requests list form.
        :param table_id: Target table id.
        :param col_idx: Column index.
        :param row_idx: Row index.
        """
        self.click_css((
            '#%s > tbody > tr:nth-child(%s) > td:nth-child(%s) > a') % (
            table_id, row_idx, col_idx))
        self.save_screenshot()

    def _cancel_request(self):
        """Close request form"""
        self.click_css('div#None.modal.in a.close')
        self.save_screenshot()

    def _submit_confirm(self, form_id):
        """Show confirm form and Submit.
        :param form_id: The Id of form tag.
        """
        self.wait_css('#%s input.btn-primary' % form_id)
        self.click_css('#%s input.btn-primary' % form_id)
        time.sleep(SET_TIMEOUT)
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
        self.wait_id(FORM_UPDATE, SET_TIMEOUT)

        # Test Message.
        message = u'\u3042' + ''.rjust(
            MAX_LENGTH_MESSAGE - len(SET_SPECIAL_CODE) - 1, 'a') + \
            SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)
        self.selenium.execute_script(
            'document.getElementById("%s").click();' % next_status_value)

        self.save_screenshot()

        self._submit_confirm(FORM_UPDATE)
        time.sleep(SET_TIMEOUT)

        self.save_screenshot()

    # ==================================================

    def delete_data(self):
        """Delete test data"""
        self._execute_sql('delete from contract;')
        self._execute_sql('delete from workflow;')
        self._execute_sql('delete from ticket;')
