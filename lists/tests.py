from django.test import TestCase
from .models import Item


class HomePageTest(TestCase):
    # test url & view
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_create_read_items(self):
        item_one = Item()
        item_one.text = 'Item one'
        item_one.save()

        item_two = Item()
        item_two.text = 'Item two'
        item_two.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        saved_item_one = saved_items[0]
        saved_item_two = saved_items[1]
        self.assertEqual('Item one', saved_item_one.text)
        self.assertEqual('Item two', saved_item_two.text)
