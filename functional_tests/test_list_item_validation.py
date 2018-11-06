from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # user goes to the homepage and tries to submit an empty list item

        # homepage refreshes and shows an error message

        # user fills in the input field and successfully submits an item

        # user submits second blank item

        # homepage refreshes and shows the same error message

        # user fills in the input field and successfully submits again
        self.fail('write me!')
