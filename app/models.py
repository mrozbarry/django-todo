# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TodoList(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TodoListItem(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    position = models.IntegerField()
    name = models.CharField(max_length=32)
    done_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self):
        self.reorder_list_items()
        super(TodoListItem, self).save(*args, **kwargs)

    def is_first(self):
        return self.position == 1

    def is_last(self):
        return False

    def reorder_list_items(self):
        """
        If position is <= 0, then move it to the last_position - position
        Ie if we had [A, B, C]...
         - adding D to position 0 would result in [A, B, C, D]
         - adding D to position -1 would result in [A, B, D, C]
         - etc.
        """
