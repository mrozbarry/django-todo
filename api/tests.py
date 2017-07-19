# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import TodoList, TodoListItem


class TodoListTests(TestCase):

    def test_last_item_position_with_no_items(self):
        todo_list = TodoList(name='last_item_test')
        todo_list.save()
        self.assertIs(todo_list.last_item_position(), 0)


    def test_last_item_position_with_one_item(self):
        todo_list = TodoList(name='last_item_test')
        todo_list.save()
        item = TodoListItem(todo_list_id=todo_list.id, name='test', position=1)
        item.save()
        self.assertIs(todo_list.last_item_position(), 1)


    def test_last_item_position_with_two_items(self):
        todo_list = TodoList(name='last_item_test')
        todo_list.save()
        TodoListItem(todo_list_id=todo_list.id, name='a', position=1).save()
        TodoListItem(todo_list_id=todo_list.id, name='b', position=2).save()
        self.assertIs(todo_list.last_item_position(), 2)


    def test_adding_3_items_at_position_0_puts_them_in_order(self):
        todo_list = TodoList(name='last_item_test')
        todo_list.save()
        TodoListItem(todo_list_id=todo_list.id, name='a', position=0).save()
        TodoListItem(todo_list_id=todo_list.id, name='b', position=0).save()
        TodoListItem(todo_list_id=todo_list.id, name='c', position=0).save()
        todo_list.todo_list_items
        self.assertIs(todo_list.last_item_position(), 3)



class TodoListItemTests(TestCase):

    def test_when_position_is_1_is_first_is_true(self):
        item = TodoListItem(todo_list_id=1, position=1)
        self.assertIs(item.is_first(), True)

    def test_when_position_is_0_is_first_is_false(self):
        item = TodoListItem(todo_list_id=1, position=0)
        self.assertIs(item.is_first(), False)

    def test_when_position_is_2_is_first_is_false(self):
        item = TodoListItem(todo_list_id=1, position=2)
        self.assertIs(item.is_first(), False)

    def test_when_position_is_0_is_last_is_true(self):
        todo_list = TodoList(name="is last test")
        todo_list.save()
        item = TodoListItem(todo_list_id=todo_list.id, position=0)
        self.assertIs(item.is_last(), True)
