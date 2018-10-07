from selenium import webdriver
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
        self.fail('Finish the test!')
        # invite user to enter a new to-do item

        # user enters title into a text box

        # user hits enter, page updates, page lists added to-do item

        # user enters another title into a text box

        # user hits enter, page updates, page lists both to-do items

        # page generates unique url for the user

        # user visits his unique url & sees his added to-do items


# check if script executed from the command line or imported by another script
if __name__ == '__main__':
    unittest.main()
