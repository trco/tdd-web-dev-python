from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # user goes to the homepage and tries to submit an empty list item
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # homepage refreshes and shows an error message
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid')
        )

        # user fills in the input field and successfully submits an item
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid')
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')

        # user submits second blank item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # homepage refreshes and shows the same error message
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid')
        )

        # user fills in the input field and successfully submits again
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid')
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')
        self.wait_for_row_in_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            DUPLICATE_ITEM_ERROR
        ))
