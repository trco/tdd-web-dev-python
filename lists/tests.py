from django.test import TestCase
from .models import Item


class HomePageTest(TestCase):
    # test get: url & view
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_list_template(self):
        response = self.client.get('/lists/one-list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    # test displaying all the items in template
    def test_display_all_items_in_template(self):
        # create items in test database
        Item.objects.create(text='Item one')
        Item.objects.create(text='Item two')

        response = self.client.get('/lists/one-list/')
        # check if created items are in response
        self.assertContains(response, 'Item one')
        self.assertContains(response, 'Item two')


class NewListTest(TestCase):
    # test post
    def test_can_save_a_post_request(self):
        # urls without trailing slash are action urls, which modify database
        response = self.client.post('/lists/new',
                                    data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    # test redirection
    def test_redirect_after_post(self):
        response = self.client.post('/lists/new',
                                    data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/one-list/')


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
