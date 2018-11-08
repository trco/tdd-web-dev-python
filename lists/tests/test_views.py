from django.test import TestCase
from django.utils.html import escape
from lists.forms import ItemForm
from lists.models import Item, List


class HomePageTest(TestCase):
    # test get: url & view
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_can_save_a_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view_after_post(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    # test empty post
    def test_the_validation_errors_are_sent_back_to_list_page(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/',
                                    data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


class NewListTest(TestCase):
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    # test empty post
    def test_the_validation_errors_are_sent_back_to_homepage(self):
        response = self.client.post('/lists/new',
                                    data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    # test post
    def test_can_save_a_post_request(self):
        # urls without trailing slash are action urls, which modify database
        response = self.client.post('/lists/new',
                                    data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    # test redirection
    def test_redirect_after_post(self):
        response = self.client.post('/lists/new',
                                    data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')
