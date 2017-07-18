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

"""Test 'Add Announcement' on Aflo.
Please operate setting.
  Step1. Create Projects
    - admin
    - demo
  Step2. Create Users
    - admin
    - demo
    - service_provider_user
    - contract_manager_user
    - service_manager_user
  Step3. Create Roles
    - admin
      Grant: [admin] project - [demo] user
             [admin] project - [service_provider_user] user
             [admin] project - [contract_manager_user] user
             [admin] project - [service_manager_user] user
    - C__Global__ProjectAdmin
      Grant: [admin] project - [demo] user
    - O__<Region Name>__ServiceProvider
      Grant: [admin] project - [service_provider_user] user
    - O__<Region Name>__ContractManager
      Grant: [admin] project - [contract_manager_user] user
    - O__<Region Name>__ServiceManager
      Grant: [admin] project - [service_manager_user] user
  Step4. Create Workflows
    Create Ticket Template and Workflow Pattern.
    - Add Announcement
  Step5. Change Selenium Parameters
    - SET_BASE_URL
    - DB_USER
    - DB_PASS
    To set the information that exists in 'Drupal'.
    - TYPE_MAINTENANCE
    - LANGUAGE
    - CATEGORY_NAME
    - SCOPE_PROJECT
    - SCOPE_REGION
    - TARGET_NAME_PROJECT
    - TARGET_NAME_REGION
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
    'service_provider_user': {
        'USERNM': 'service_provider_user',
        'PASSWORD': 'xxxx'
    },
    'contract_manager_user': {
        'USERNM': 'contract_manager_user',
        'PASSWORD': 'xxxx'
    },
    'service_manager_user': {
        'USERNM': 'service_manager_user',
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
    # Demo user.
    'sign_in_demo',
    'change_setting',
    'show_ticket_template_list',
    'sign_out',
    # Admin user(Service provider).
    'sign_in_admin_service_provider',
    'admin_add_announcement_entry_scope_project',
    'sign_out',
    # Admin user(Contract manager).
    'sign_in_admin_contract_manager',
    'admin_add_announcement_entry_scope_region',
    'sign_out',
    # Admin user(Service manager).
    'sign_in_admin_service_manager',
    'admin_add_announcement_entry_scope_all',
    'admin_add_announcement_approval_canceled',
    'admin_add_announcement_approval_rejected',
    'admin_add_announcement_approval_scope_all_final_approval',
    'admin_add_announcement_approval_scope_region_final_approval',
    'admin_add_announcement_approval_scope_project_final_approval',
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

TICKET_TEMPLATE_ID_ADD_ANNOUNCEMENT = '90'

MAX_LENGTH_TITLE = 255
MAX_LENGTH_MESSAGE = 512
MAX_LENGTH_MAIN_TEXT = 2000

FORM_CREATE = 'create_form'
FORM_UPDATE = 'update_form'

TYPE_MAINTENANCE = 'maintenance'
LANGUAGE = 'en'
CATEGORY_NAME = 'new'
SCOPE_PROJECT = 'project'
SCOPE_REGION = 'region'
TARGET_NAME_PROJECT = 'xxxxxxx'
TARGET_NAME_REGION = 'RegionOne'


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
        self.selenium.execute_script(
            'arguments[0].scrollIntoView(true);', element)
        element.click()

    def click_xpath_and_ajax_wait(self, xpath, timeout=SET_TIMEOUT):
        """Click on the button xpath ajax wait"""
        time.sleep(timeout)
        element = self.selenium.find_element_by_xpath(xpath)
        self.selenium.execute_script(
            'arguments[0].scrollIntoView(true);', element)
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

    def change_setting(self):
        """Change Language"""
        self.trans_and_wait('user_settings_modal', '/settings/')
        self.set_select_value('id_language', self.multiple_languages)
        self.click_css('input[type=submit]')

    def sign_in_admin_service_provider(self):
        """Sign in service provider user"""
        self._sign_in('service_provider_user', 'admin')

    def sign_in_admin_contract_manager(self):
        """Sign in contract manager user"""
        self._sign_in('contract_manager_user', 'admin')

    def sign_in_admin_service_manager(self):
        """Sign in service manager user"""
        self._sign_in('service_manager_user', 'admin')

    def sign_in_demo(self):
        """Sign in demo user"""
        self._sign_in('demo', 'admin')

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

    def show_ticket_template_list(self):
        """Show ticket template list form"""
        self._project_ticket_templates_list(True)

    # ==================================================

    def _test_add_announcement_irregular_required(self):
        """Entry a 'Add Announcement' ticket.
        Required error pattern.
        """
        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        self.wait_id(FORM_CREATE)

        self.save_screenshot()

    def _test_add_announcement_irregular_max_length_over(self):
        """Entry a 'Add Announcement' ticket.
        Max length error pattern.
        """
        # Test Title(over).
        title = u'\u3042' + ''.rjust(MAX_LENGTH_TITLE - 1, 'a') + 'E'
        # Test Message(over).
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - 1, 'a') + 'E'
        # Test Main text(over).
        main_text = u'\u3042' + ''.rjust(MAX_LENGTH_MAIN_TEXT - 1, 'a') + 'E'
        self.fill_field('id___param_title', title)
        self.fill_field('id___param_field_maintext', main_text)
        self.fill_field('id___param_field_target', message)
        self.fill_field('id___param_field_workcontent', main_text)
        self.fill_field('id___param_field_acknowledgements', message)
        self.fill_field('id___param_message', message)

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        self.wait_id(FORM_CREATE)

        self.save_screenshot()

    # ==================================================

    def admin_add_announcement_entry_scope_all(self):
        """Entry a 'Add Announcement' ticket.
        Scope is all.
        """
        self._project_ticket_templates_list(False)

        # Create 3 ticket.(Add Announcement)
        #  Root 1: [Add Announcement] -> Canceled
        #  Root 2: [Add Announcement] -> Rejected
        #  Root 3: [Add Announcement] -> Final approval
        for row_idx in range(3):
            save_screen = True if row_idx == 0 else False

            self._project_ticket_entry_form_show(
                TICKET_TEMPLATE_ID_ADD_ANNOUNCEMENT, FORM_CREATE)
            self._test_add_announcement_entry(SCOPE_PROJECT, '', save_screen)

            self._project_ticket_templates_list(False)

    def admin_add_announcement_entry_scope_project(self):
        """Entry a 'Add Announcement' ticket.
        Scope is project.
        """
        self._project_ticket_templates_list(True)

        # Add Announcement.
        self._project_ticket_entry_form_show(
            TICKET_TEMPLATE_ID_ADD_ANNOUNCEMENT, FORM_CREATE)
        self._test_add_announcement_irregular_required()
        self._test_add_announcement_irregular_max_length_over()
        self._cancel_request()

        self._project_ticket_entry_form_show(
            TICKET_TEMPLATE_ID_ADD_ANNOUNCEMENT, FORM_CREATE)
        self._test_add_announcement_entry(SCOPE_PROJECT, TARGET_NAME_PROJECT)

    def admin_add_announcement_entry_scope_region(self):
        """Entry a 'Add Announcement' ticket.
        Scope is region.
        """
        self._project_ticket_templates_list(False)

        # Add Announcement.
        self._project_ticket_entry_form_show(
            TICKET_TEMPLATE_ID_ADD_ANNOUNCEMENT, FORM_CREATE)
        self._test_add_announcement_entry(SCOPE_REGION, TARGET_NAME_REGION)

    def _test_add_announcement_entry(
            self, scope, target_name, save_screen=True):
        """Entry a 'Add Announcement' ticket.
        :param scope: Scope to select.
        :param target_name: Target name.
        :param save_screen: Save screenshot image.
        """
        time.sleep(SET_TIMEOUT)

        if save_screen:
            self.save_screenshot()

        # Success ticket entry form.
        # It is necessary for the entry to perform sleep
        # for async processing.

        # Test Title.
        title = u'\u3042' + ''.rjust(MAX_LENGTH_TITLE - len(
            SET_SPECIAL_CODE) - 1, 'a') + SET_SPECIAL_CODE
        # Test Message.
        message = u'\u3042' + ''.rjust(MAX_LENGTH_MESSAGE - len(
            SET_SPECIAL_CODE) - 1, 'a') + SET_SPECIAL_CODE
        # Test Main text.
        main_text = u'\u3042' + ''.rjust(MAX_LENGTH_MAIN_TEXT - len(
            SET_SPECIAL_CODE) - 1, 'a') + SET_SPECIAL_CODE
        self.fill_field('id___param_title', title)
        self.fill_field('id___param_field_maintext', main_text)
        self.fill_field('id___param_field_workdays', SET_SPECIAL_CODE)
        self.fill_field('id___param_field_target', message)
        self.fill_field('id___param_field_workcontent', main_text)
        self.fill_field('id___param_field_acknowledgements', message)
        self.fill_field('id___param_field_category', CATEGORY_NAME)
        self.set_select_value('id___param_scope', scope)
        self.fill_field('id___param_target_name', target_name)
        self.fill_field('id___param_field_announcementdate', SET_SPECIAL_CODE)
        self.fill_field('id___param_publish_on', SET_SPECIAL_CODE)
        self.fill_field('id___param_unpublish_on', SET_SPECIAL_CODE)
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

    def admin_add_announcement_approval_canceled(self):
        """Update 'Add Announcement' status to admin selected status"""
        # Show ticket list form.
        self._admin_request_list()

        # Show detail form.
        self._click_ticket_list('request_list', 4, 1)

        # Update status.
        self._update_request_from_detail('canceled')

    def admin_add_announcement_approval_rejected(self):
        """Update 'Add Announcement' status to admin selected status"""
        # Update status.
        self._update_request_list(2, 'rejected')

    def admin_add_announcement_approval_scope_all_final_approval(self):
        """Update 'Add Announcement' status to admin selected status"""
        # Update status.
        self._update_request_list(3, 'final approval')

    def admin_add_announcement_approval_scope_region_final_approval(self):
        """Update 'Add Announcement' status to admin selected status"""
        # Update status.
        self._update_request_list(4, 'final approval')

    def admin_add_announcement_approval_scope_project_final_approval(self):
        """Update 'Add Announcement' status to admin selected status"""
        # Update status.
        self._update_request_list(5, 'final approval')

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

    def _admin_request_list(self, save_screen=True):
        """Show ticket list form of admin.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('request_list', '/admin/request_list/')

        if save_screen:
            time.sleep(SET_TIMEOUT)
            self.save_screenshot()

    def _project_ticket_entry_form_show(self, ticket_template_id, form_id):
        """Show entry form from ticket list of project.
        :param ticket_template_id: Ticket template id.
        :param form_id: The Id of form tag.
        """
        self.click_css((
            '#%s #tickettemplates__row__%s > td.anchor.normal_column > a') %
            (TAB_NAME, ticket_template_id))
        self.wait_id(form_id)

    def _click_ticket_list(self, table_id, col_idx=1, row_idx=1):
        """Show issued requests list form.
        :param table_id: Target table id.
        :param col_idx: Column index.
        :param row_idx: Row index.
        """
        self.click_css((
            '#%s > tbody > tr:nth-child(%s) > td:nth-child(%s) > a') %
            (table_id, row_idx, col_idx))

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
        self.click_css('div.modal.aflo_confirm_dialog'
                       ' a.btn-primary')

    def _update_request_list(self, ticket_row_idx, next_status_value):
        """Update a request from request list form.
        :param ticket_row_idx: Set row index of ticket list form.
        :param next_status_value: Change a status to value.
        """
        self._click_ticket_list('request_list', 11, ticket_row_idx)

        self._update_request(next_status_value)

    def _update_request_from_detail(self, next_status_value):
        """Update a request from detail form.
        :param next_status_value: Change a status to value.
        """
        self.click_css('a.btn-edit')

        self._update_request(next_status_value)

    def _update_request(self, next_status_value):
        """Update a request.
        :param ticket_row_idx: Set row index of ticket list form.
        :param next_status_value: Change a status to value.
        """
        self.wait_id(FORM_UPDATE, SET_TIMEOUT)

        # Test Message.
        message = u'\u3042' + ''.rjust(
            MAX_LENGTH_MESSAGE - len(SET_SPECIAL_CODE) - 1, 'a') + \
            SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        self.click_xpath_and_ajax_wait(
            "//input[contains(@value, '%s')]" % next_status_value)

        time.sleep(SET_TIMEOUT)

        self.save_screenshot()

        self._submit_confirm(FORM_UPDATE)

        time.sleep(SET_TIMEOUT)

        self.save_screenshot()

    # ==================================================

    def delete_data(self):
        """Delete test data.
        Delete target is ticket table and workflow table.
        """
        self._execute_sql('delete from workflow;')
        self._execute_sql('delete from ticket;')
