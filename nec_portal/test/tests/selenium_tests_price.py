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

"""Test 'Price' on Aflo.
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
    - _member_
      Grant: [demo] project - [demo] user
  Step4. Create Catalogs
    Create Goods, Catalog, Catalog Contents, Price and Catalog Scope.
    - VCPU x 10 CORE(S)
    - RAM 20 GB
    - Volume Storage 50 GB
  Step5. Change Selenium Parameters
    - SET_BASE_URL
    - DEMO_PROJECT_ID
"""

import datetime
import os
import time
import traceback

from horizon.test import helpers as test

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# Command executor. Hub URL of Jenkins
SET_COMMAND_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'
# Base URL. Environment for testing.
# As for the URL, the last slash is unnecessary
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
# Width of the window
SET_WIDTH = 1280
# Height of the window
SET_HEIGHT = 1024
# Implicitly wait & Timeout
SET_IMPLICITLY_WAIT = 90
SET_TIMEOUT = 5
# Capture of location
SET_CAPPATH = 'openstack_dashboard/test/tests/screenshots/'
# Data prefix
SET_DATAPREFIX = 'selenium_longname_ui_' + \
    datetime.datetime.today().strftime('%Y%m%d%H%M%S')
# They are arranged sequentially by setting the browser target
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

# They are arranged sequentially by setting the execution target
SET_METHOD_LIST = [
    'change_setting',
    'sign_in',
    'admin_price_list',
    'admin_public_price_update',
    'admin_private_price_update',
    'project_price_list',
    'project_price_detail',
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

MAX_LENGTH_NUMBER = 4
MAX_LENGTH_DESCRIPTION = 255

DEMO_PROJECT_ID = 'adb27177f0d449888f42a3625b9eb3d1'


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
        # Capture count
        self.cap_count = 1
        # Method name
        self.method = ''

    def test_main(self):
        """Main execution method"""
        try:
            # Datetime
            self.datetime = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

            # Browser order definition
            for key, value in SET_BROWSER_LIST.items():
                if key not in SET_TEST_BROWSER or not SET_TEST_BROWSER[key]:
                    continue

                if not self.caps == key:
                    self.caps = key
                    self.selenium = webdriver.Remote(
                        command_executor=SET_COMMAND_EXECUTOR,
                        desired_capabilities=value)

                    self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)

                # Browser display waiting time
                self.selenium.implicitly_wait(SET_IMPLICITLY_WAIT)
                # Set the size of the window
                self.selenium.set_window_size(SET_WIDTH, SET_HEIGHT)

                for language, flg in SET_TEST_LANGUAGE.items():
                    if not flg:
                        continue

                    print ('Test language = [' + language + ']')

                    for is_admin in [True, False]:
                        self.is_admin = is_admin

                        # Initializing process
                        self.initialize()
                        # Object language
                        self.multiple_languages = language
                        # Call execution method
                        self.execution()

            print ('Test has been completed')

        except Exception:
            print ('Test failed')

    def execution(self):
        """Execution method"""
        # Method execution order definition
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
            # Make directory
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

    def fill_field_by_css(self, css, value):
        """Enter a value to the css"""
        self.fill_field_clear_by_css(css)
        self.selenium.find_element_by_css_selector(css).send_keys(value)

    def fill_field_clear(self, field_id):
        """Clear to the field"""
        self.selenium.find_element_by_id(field_id).clear()

    def fill_field_clear_by_name(self, field_name):
        """Clear to the field"""
        self.selenium.find_element_by_name(field_name).clear()

    def fill_field_clear_by_css(self, css):
        """Clear to the css"""
        self.selenium.find_element_by_css_selector(css).clear()

    def click_and_wait(self, field_id, nextId, timeout=SET_TIMEOUT):
        """Click on the button"""
        element = self.selenium.find_element_by_id(field_id)
        element.click()
        self.wait_id(nextId, timeout)

    def click_id(self, field_id, timeout=SET_TIMEOUT):
        """Click on the button id(no wait)"""
        element = self.selenium.find_element_by_id(field_id)
        element.click()

    def click_name(self, field_name, timeout=SET_TIMEOUT):
        """Click on the button name(no wait)"""
        element = self.selenium.find_element_by_name(field_name)
        element.click()

    def click_link_text(self, link_text, timeout=SET_TIMEOUT):
        """Click on the link text(no wait)"""
        element = self.selenium.find_element_by_link_text(link_text)
        element.click()

    def click_css(self, css, timeout=SET_TIMEOUT):
        """Click on the button css(no wait)"""
        element = self.selenium.find_element_by_css_selector(css)
        element.click()

    def click_xpath(self, xpath, timeout=SET_TIMEOUT):
        """Click on the button xpath"""
        element = self.selenium.find_element_by_xpath(xpath)
        element.click()

    def click_css_and_ajax_wait(self, css, timeout=SET_TIMEOUT):
        """Click on the button css ajax wait"""
        element = self.selenium.find_element_by_css_selector(css)
        element.click()
        self.wait_ajax(timeout)

    def click_xpath_and_ajax_wait(self, xpath, timeout=SET_TIMEOUT):
        """Click on the button xpath ajax wait"""
        element = self.selenium.find_element_by_xpath(xpath)
        element.click()
        self.wait_ajax(timeout)

    def set_select_value(self, field_id, value):
        """Set of pull-down menu by value"""
        Select(self.selenium.find_element_by_id(field_id))\
            .select_by_value(value)

    def wait_id(self, nextId, timeout=SET_TIMEOUT):
        """Wait until the ID that you want to schedule is displayed"""
        WebDriverWait(self.selenium, timeout).until(
            EC.visibility_of_element_located((By.ID, nextId)))

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

        # Move next page
        self.click_css('#%s > tfoot > tr > td > a' % table_id)
        time.sleep(SET_TIMEOUT)
        self.save_screenshot()

        # Move previous page
        self.click_css('#%s > tfoot > tr > td > a' % table_id)
        time.sleep(SET_TIMEOUT)
        self.save_screenshot()

    def sign_in(self):
        """Sign in"""
        # Capture the initial display
        self.trans_and_wait('loginBtn', '')

        if self.is_admin:
            user = SET_USER.get('admin')
            self.fill_field('id_username', user.get('USERNM'))
            self.fill_field('id_password', user.get('PASSWORD'))
        else:
            user = SET_USER.get('demo')
            self.fill_field('id_username', user.get('USERNM'))
            self.fill_field('id_password', user.get('PASSWORD'))

        self.click_id('loginBtn')
        time.sleep(SET_TIMEOUT)

        # Set project.
        self._select_project(user.get('USERNM'))

    def _select_project(self, project_name='demo'):
        """Select project name"""
        self.click_css('span.fa-caret-down')

        time.sleep(SET_TIMEOUT)
        self.click_xpath_and_ajax_wait(
            '//span[@class="dropdown-title"][contains(text(),"%s")]'
            % project_name)

    def sign_out(self):
        """Sign out"""
        self.trans_and_wait('loginBtn', '/auth/logout/')
        time.sleep(SET_TIMEOUT)

    def change_setting(self, page=2):
        """Change Language, pagesize page"""
        # Sign In
        self.sign_in()

        # Change Language
        self.trans_and_wait('id_pagesize', '/settings/')
        self.fill_field('id_pagesize', page)
        self.set_select_value('id_language', self.multiple_languages)
        time.sleep(SET_TIMEOUT)
        self.click_css('input.btn.btn-primary')
        time.sleep(SET_TIMEOUT)

        # Sign Out
        self.sign_out()

    def admin_price_list(self, save_screen=True):
        """Show price list.
        :param save_screen: Save screenshot image.
        """
        if not self.is_admin:
            return

        # Show price list
        self.trans_and_wait('tenants', '/admin/private_price_lists/')
        if save_screen:
            self.save_screenshot()

        # Filter
        self.fill_field_by_name('tenants__filter__q', 'no_data')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.fill_field_by_name('tenants__filter__q', 'demo')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

    def admin_public_price_update(self, save_screen=True):
        """Entry a public price update.
        :param save_screen: Save screenshot image.
        """
        if not self.is_admin:
            return

        # Show price list
        self.admin_price_list(False)
        if save_screen:
            self.save_screenshot()

        # Show price update
        self.click_and_wait('tenants__action_public_price',
                            'public_price_lists_update')
        if save_screen:
            self.save_screenshot()

        # Move page
        self._change_page('public_price_lists_update', True)
        time.sleep(SET_TIMEOUT)

        # Filter
        self.fill_field_by_name('public_price_lists_update__filter__q',
                                'no_data')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.fill_field_by_name('public_price_lists_update__filter__q',
                                'VCPU x 10 CORE')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.fill_field_by_name('public_price_lists_update__filter__q', '')
        self.click_name('public_price_lists_update__filter__q')
        time.sleep(SET_TIMEOUT)

        # Ajax price text-box
        td_css = 'td.inline_edit_available.sortable.normal_column'
        td = self.selenium.find_element_by_css_selector(td_css)
        hover = ActionChains(self.selenium).move_to_element(td)
        hover.perform()
        time.sleep(SET_TIMEOUT)
        self.click_css('button.ajax-inline-edit')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        # input check : max_len
        self.fill_field_by_css('.inline-edit-form input', '1234567890.1234')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.click_name('action')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        # input check : char
        self.fill_field_by_css('.inline-edit-form input', 'a')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.click_name('action')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        # price update or insert
        self.fill_field_by_css('.inline-edit-form input', '123.45')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.click_name('action')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

    def admin_private_price_update(self, save_screen=True):
        """Entry a private price update.
        :param save_screen: Save screenshot image.
        """
        if not self.is_admin:
            return

        # Show price list
        self.admin_price_list(False)
        if save_screen:
            self.save_screenshot()

        # Show price update
        self.click_and_wait('tenants__row_%s__action_edit' %
                            DEMO_PROJECT_ID,
                            'private_price_lists_update')
        if save_screen:
            self.save_screenshot()

        # Move page
        self._change_page('private_price_lists_update', True)
        time.sleep(SET_TIMEOUT)

        # Filter
        self.fill_field_by_name('private_price_lists_update__filter__q',
                                'no_data')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.fill_field_by_name('private_price_lists_update__filter__q',
                                'VCPU x 10 CORE')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.fill_field_by_name('private_price_lists_update__filter__q', '')
        self.click_name('private_price_lists_update__filter__q')
        time.sleep(SET_TIMEOUT)

        # Ajax price text-box
        td_css = 'td.inline_edit_available.sortable.normal_column'
        td = self.selenium.find_element_by_css_selector(td_css)
        hover = ActionChains(self.selenium).move_to_element(td)
        hover.perform()
        time.sleep(SET_TIMEOUT)
        self.click_css('button.ajax-inline-edit')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        # input check : max_len
        self.fill_field_by_css('.inline-edit-form input', '1234567890.1234')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.click_name('action')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        # input check : char
        self.fill_field_by_css('.inline-edit-form input', 'a')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.click_name('action')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        # price update or insert
        self.fill_field_by_css('.inline-edit-form input', '123.45')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        self.click_name('action')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

    def project_price_list(self, save_screen=True):
        """Show price list.
        :param save_screen: Save screenshot image.
        """
        # Show price list
        self.trans_and_wait('catalogs',
                            '/project/private_price_lists/')
        if save_screen:
            self.save_screenshot()

        # Filter
        self.fill_field_by_name('catalogs__filter__q', 'no_data')
        time.sleep(SET_TIMEOUT)
        self.click_and_wait('catalogs__action_filter',
                            'catalogs')
        if save_screen:
            self.save_screenshot()

        self.fill_field_by_name('catalogs__filter__q',
                                'VCPU x 10 CORE')
        self.fill_field_by_name('catalogs__filter__q',
                                '')
        time.sleep(SET_TIMEOUT)
        self.click_and_wait('catalogs__action_filter',
                            'catalogs')
        if save_screen:
            self.save_screenshot()

    def project_price_detail(self, save_screen=True):
        """Entry a price detail.
        :param save_screen: Save screenshot image.
        """
        # Show price list
        self.trans_and_wait('catalogs',
                            '/project/private_price_lists/')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()

        # Show price detail
        self.click_css('td.sortable.anchor.normal_column a')
        time.sleep(SET_TIMEOUT)
        if save_screen:
            self.save_screenshot()
