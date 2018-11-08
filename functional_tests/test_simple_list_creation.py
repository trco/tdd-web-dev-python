from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_list_and_retrieve_it_later(self):
        # user opens homepage
        # self.live_server_url relates to LiveServerTestCase
        self.browser.get(self.live_server_url)

        # user checks page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # invite user to enter a new to-do item
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # user enters title into a text box
        inputbox.send_keys('Buy peacock feathers')
        # user hits enter, page updates, page lists added to-do item in a table
        # refresh the page
        inputbox.send_keys(Keys.ENTER)
        # explicit wait to wait for the browser to completely load the page
        # before making any assertion

        self.wait_for_row_in_table('1: Buy peacock feathers')

        # user enters another title into a text box
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # user hits enter, page updates, page lists both to-do items
        self.wait_for_row_in_table('1: Buy peacock feathers')
        self.wait_for_row_in_table('2: Use peacock feathers to make a fly')

        # self.fail('Finish the test.')

    def test_mulitple_users_can_start_lists_at_different_urls(self):
        # for comments see test_can_start_list_and_retrieve_it_later
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy peacock feathers')

        # page generates unique url for the user
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')

        # second user comes to the site

        # new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        # check there is no trace of first user's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # second user starts new list by adding an item
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')

        # page generates unique url for the second user
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')

        # check that first and second user's urls are different
        self.assertNotEqual(user_list_url, second_user_list_url)

        # check there is no trace of first user's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Buy peacock feathers', page_text)
        self.assertIn('1: Buy milk', page_text)
