from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # helper functions
    def check_if_item_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve_it_later(self):
        # user opens homepage
        self.browser.get('http://localhost:8000')

        # user checks page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # invite user to enter a new to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
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
        time.sleep(1)

        self.check_if_item_in_table('1: Buy peacock feathers')

        # user enters another title into a text box
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.fail('Finish the test.')

        # user hits enter, page updates, page lists both to-do items
        self.check_if_item_in_table('1: Buy peacock feathers')
        self.check_if_item_in_table('2: Use peacock feathers to make a fly')

        # page generates unique url for the user

        # user visits his unique url & sees his added to-do items