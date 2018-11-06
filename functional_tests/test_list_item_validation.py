from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # user goes to the homepage and tries to submit an empty list item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # homepage refreshes and shows an error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # user fills in the input field and successfully submits an item
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys('Keys.ENTER')
        self.wait_for_row_in_table('1: Buy milk')

        # user submits second blank item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # homepage refreshes and shows the same error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # user fills in the input field and successfully submits again
        self.browser.find_element_by_id('id_new_item').send_keys('Make tead')
        self.browser.find_element_by_id('id_new_item').send_keys('Keys.ENTER')
        self.wait_for_row_in_table('1: Buy milk')
        self.wait_for_row_in_table('2: Make tea')
