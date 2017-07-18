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

"""Test 'Request Inquiry' on Aflo.
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
    - T__<Region Name>__ProjectMember
      Grant: [demo] project - [demo] user
  Step4. Create Workflows
    Create Ticket Template and Workflow Pattern.
    - Request Inquiry
  Step5. Change Selenium Parameters
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
# Login user
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
# Data prefix
SET_DATAPREFIX = 'selenium_longname_ui_' + \
    datetime.datetime.today().strftime('%Y%m%d%H%M%S')
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
    # Project user.
    'sign_in_project',
    'change_setting',
    'project_send_inquiry_entry',
    'project_confirm_ticket',
    'sign_out',
    # Admin user.
    'sign_in_admin',
    'admin_send_inquiry_update',
    'sign_out',
    # Project user.
    'sign_in_project',
    'project_send_inquiry_update',
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

TICKET_TEMPLATE_ID_SEND_INQUIRY = '20'

MAX_LENGTH_MESSAGE = 255
MAX_LENGTH_ENTRY_MESSAGE = 512

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
        self.selenium.get(SET_BASE_URL + urlpath)
        self.wait_id(nextId, timeout)

    def fill_field(self, field_id, value):
        """Enter a value to the field"""
        self.fill_field_clear(field_id)
        self.selenium.find_element_by_id(field_id).send_keys(value)

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

    def click_id(self, field_id, timeout=SET_TIMEOUT):
        """Click on the button id(no wait)"""
        element = self.selenium.find_element_by_id(field_id)
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

    def set_select_value(self, id, value):
        """Set of pull-down menu by value"""
        Select(self.selenium.find_element_by_id(id)).select_by_value(value)

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

    def _change_page(self, table_id, save_screen):
        """Move next page and previous page.
        :param table_id: target table id.
        :param save_screen: Save screenshot image.
        """
        if not save_screen:
            return

        # Move next page.
        self.click_css(
            '#%s > tfoot:nth-child(3) > tr:nth-child(1) > '
            'td:nth-child(1) > a:nth-child(3)' % table_id)
        self.save_screenshot()

        # Move previous page.
        self.click_css(
            '#%s > tfoot:nth-child(3) > tr:nth-child(1) > '
            'td:nth-child(1) > a:nth-child(3)' % table_id)
        self.save_screenshot()

    def change_setting(self, page=20):
        """Change Language"""
        self.trans_and_wait('user_settings_modal', '/settings/')
        self.fill_field('id_pagesize', page)
        self.set_select_value('id_language', self.multiple_languages)
        self.click_css('input[type=submit]')

    def sign_in_admin(self):
        """Sign in admin user"""
        self._sign_in('admin', 'admin')

    def sign_in_project(self):
        """Sign in project user"""
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
        subprocess.call(['mysql', '-D', 'aflo', '-u' + DB_USER, '-p' + DB_PASS,
                        '-e', sql])

    # ==================================================

    def project_send_inquiry_entry(self):
        """Entry a 'Send Inquiry' ticket.
        Required error pattern.
        """
        self._project_ticket_templates_list(False)

        # Send Inquiry.
        self._project_ticket_entry_form_show(
            TICKET_TEMPLATE_ID_SEND_INQUIRY,
            FORM_CREATE)
        self._test_send_inquiry_irregular_required()
        self._test_send_inquiry_irregular_max_length_over()
        self._cancel_request()

        self._project_ticket_entry_form_show(
            TICKET_TEMPLATE_ID_SEND_INQUIRY,
            FORM_CREATE)
        self._test_send_inquiry_entry()

    def _test_send_inquiry_irregular_required(self):
        """Entry a 'Send Inquiry' ticket.
        Required error pattern.
        """
        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        self.wait_id(FORM_CREATE)

        self.save_screenshot()

    def _test_send_inquiry_irregular_max_length_over(self):
        """Entry a 'Send Inquiry' ticket.
        Max length error pattern.
        """
        # Test Message(over).
        message = u'\u3042' + ''.rjust(MAX_LENGTH_ENTRY_MESSAGE - 1,
                                       'a') + 'E'
        self.fill_field('id___param_message', message)

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)

        self.wait_id(FORM_CREATE)

        self.save_screenshot()

    def _test_send_inquiry_entry(self):
        """Entry a 'Send Inquiry' ticket"""
        self.save_screenshot()

        # Success ticket entry form.
        #  It is necessary for the entry to perform sleep
        #  for async processing.

        # Test Message.
        message = u'\u3042' + ''.rjust(
            MAX_LENGTH_ENTRY_MESSAGE - len(SET_SPECIAL_CODE) - 1, 'a') + \
            SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        self.save_screenshot()

        # Show confirm form and Submit.
        self._submit_confirm(FORM_CREATE)
        time.sleep(5)

        self.save_screenshot()

    # ==================================================

    def project_confirm_ticket(self):
        """Show ticket list form go to detail form"""
        # Show 'Send Inquiry' ticket detail form.
        self._project_ticket_list(True)
        self._click_ticket_list('ticket_list', 3, 1)

    # ==================================================

    def admin_send_inquiry_update(self):
        """Update 'Send Inquiry' status to admin selected status"""
        # Show ticket list form.
        self._admin_request_list()

        # Show detail form.
        self._click_ticket_list('request_list',
                                4, 1)

        # Update status.(id_approval_flg_1: done)
        self._update_request_from_detail('id_approval_flg_1')

    def project_send_inquiry_update(self):
        """Update 'Send Inquiry' status to closed"""
        # Show ticket list form.
        self._project_ticket_list(True)

        # Show detail form.
        self._click_ticket_list('ticket_list',
                                3, 1)

        # Update status.(id_approval_flg_0: closed)
        self._update_request_from_detail('id_approval_flg_0')

    # ==================================================

    def _project_ticket_templates_list(self, save_screen=True):
        """Show ticket template list form.
        :param save_screen: Save screenshot image.
        """
        # Show ticket template form.
        self.trans_and_wait('tickettemplates',
                            '/project/ticket_templates/?tab=' + TAB_NAME)
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

    def _admin_request_list(self, save_screen=True):
        """Show ticket list form of admin.
        :param save_screen: Save screenshot image.
        """
        # Show ticket list form.
        self.trans_and_wait('request_list', '/admin/request_list/')

        if save_screen:
            self.save_screenshot()

    def _project_ticket_entry_form_show(self,
                                        ticket_template_id,
                                        form_id):
        """Show entry form from ticket list of project"""
        self.click_css(('#%s' +
                        ' #tickettemplates__row__%s > ' +
                        ' td.anchor.normal_column > ' +
                        ' a') % (TAB_NAME, ticket_template_id))
        self.wait_id(form_id)

    def _click_ticket_list(self, table_id, col_idx=1, row_idx=1):
        """Show issued requests list form.
        :param table_id: Target table id.
        :param col_idx: Column index.
        :param row_idx: Row index.
        """
        self.click_css(('#%s > ' +
                        ' tbody > tr:nth-child(%s) > ' +
                        ' td:nth-child(%s) > ' +
                        ' a') % (table_id, row_idx, col_idx))

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
        self.click_css('div.modal.aflo_confirm_dialog'
                       ' a.btn-primary')

    def _update_request_list(self, ticket_row_idx, next_status_flg):
        """Update a request from request list form.
        :param ticket_row_idx: Set row index of ticket list form.
        :param next_status_flg: Change a status to value.
        """
        self._click_ticket_list('request_list',
                                11, ticket_row_idx)

        self._update_request(next_status_flg)

    def _update_ticket_list(self, ticket_row_idx, next_status_flg):
        """Update a request from ticket list form.
        :param ticket_row_idx: Set row index of ticket list form.
        :param next_status_flg: Change a status to value.
        """
        self._click_ticket_list('ticket_list',
                                10, ticket_row_idx)

        self._update_request(next_status_flg)

    def _update_request_from_detail(self, next_status_flg):
        """Update a request from detail form.
        :param next_status_flg: Change a status to value.
        """
        self.click_css('a.btn-edit')

        self._update_request(next_status_flg)

    def _update_request(self, next_status_flg):
        """Update a request.
        :param ticket_row_idx: Set row index of ticket list form.
        :param next_status_flg: Change a status to value.
        """
        self.wait_id(FORM_UPDATE, SET_TIMEOUT)

        # Test Message.
        message = u'\u3042' + ''.rjust(
            MAX_LENGTH_MESSAGE - len(SET_SPECIAL_CODE) - 1, 'a') + \
            SET_SPECIAL_CODE
        self.fill_field('id___param_message', message)

        self.selenium.execute_script(
            'document.getElementById("%s").click();' % next_status_flg)

        self.save_screenshot()

        self._submit_confirm(FORM_UPDATE)
        time.sleep(5)

        self.save_screenshot()

    # ==================================================

    def delete_data(self):
        """Delete test data.
        Delete target is ticket table and workflow table.
        """
        self._execute_sql('delete from workflow;')
        self._execute_sql('delete from ticket;')
