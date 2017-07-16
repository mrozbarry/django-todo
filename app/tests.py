# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import TodoList, TodoListItem


class TodoListTests(TestCase):

    def test_last_item_position(self):
        todo_list = TodoList(name='last_item_test')
        todo_list.save()
        self.assertIs(todo_list.last_item_position(), 0)


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
