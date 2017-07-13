# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import TodoListItem


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
        item = TodoListItem(todo_list_id=1, position=0)
        self.assertIs(item.is_last(), False)
