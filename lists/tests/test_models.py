from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelsTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

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
