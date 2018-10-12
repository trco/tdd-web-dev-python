from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve_it_later(self):
        # user opens homepage
        self.browser.get('http://localhost:8000')

        # user checks page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        self.fail('Finish the test!')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # user enters another title into a text box

        # user hits enter, page updates, page lists both to-do items

        # page generates unique url for the user

        # user visits his unique url & sees his added to-do items


# check if script executed from the command line or imported by another script
if __name__ == '__main__':
    unittest.main()
