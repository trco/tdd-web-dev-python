from django.test import TestCase
from .models import Item, List


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
        list_ = List.objects.create()
        Item.objects.create(text='Item one', list=list_)
        Item.objects.create(text='Item two', list=list_)

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


class ListAndItemModelTest(TestCase):

    def test_create_read_items(self):
        # create list
        list_ = List()
        list_.save()

        # create item 1 and add list to it
        item_one = Item()
        item_one.text = 'Item one'
        item_one.list = list_
        item_one.save()

        # create item 2 and add list to it
        item_two = Item()
        item_two.text = 'Item two'
        item_two.list = list_
        item_two.save()

        # check if saved list is equal to created list
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        saved_item_one = saved_items[0]
        saved_item_two = saved_items[1]
        self.assertEqual('Item one', saved_item_one.text)
        # check if item is linked to the list
        self.assertEqual(saved_item_one.list, list_)
        self.assertEqual('Item two', saved_item_two.text)
        self.assertEqual(saved_item_two.list, list_)
