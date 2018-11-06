from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    # test get: url & view
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    # test displaying all the items in template
    def test_display_items_for_specific_list(self):
        # create items in test database
        list_ = List.objects.create()
        Item.objects.create(text='Item 1', list=list_)
        Item.objects.create(text='Item 2', list=list_)
        list_second = List.objects.create()
        Item.objects.create(text='Item 3', list=list_second)
        Item.objects.create(text='Item 4', list=list_second)

        response = self.client.get(f'/lists/{list_.id}/')
        # check if created items are in response
        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Item 3')
        self.assertNotContains(response, 'Item 4')

    def test_passes_correct_list_to_template(self):
        list_ = List.objects.create()
        list_second = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertEqual(response.context['list'], list_)


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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    def test_can_add_new_item_to_existing_list(self):
        list_ = List.objects.create()
        list_second = List.objects.create()

        response = self.client.post(
            f'/lists/{list_.id}/add_item',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, list_)

    def test_redirects_to_list_view(self):
        list_ = List.objects.create()
        list_second = List.objects.create()

        response = self.client.post(
            f'/lists/{list_.id}/add_item',
            data={'item_text': 'A new list item'}
        )

        self.assertRedirects(response, f'/lists/{list_.id}/')
