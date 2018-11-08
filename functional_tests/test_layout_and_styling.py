from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # user visits homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # he notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # he starts new list & sees the inputbox is centered there too
        inputbox.send_keys('Layout test')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Layout test')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
