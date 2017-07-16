# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from uuid import uuid4

from django.db import models, connection

class TodoList(models.Model):
    code = models.CharField(max_length=36, unique=True, default=uuid4, editable=False)
    name = models.CharField(max_length=32)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.code == None or self.code == "":
            self.code = uuid4

        super(TodoList, self).save(*args, **kwargs)


    def last_item_position(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(position) AS last_position FROM app_todolistitem WHERE todo_list_id = %s", [self.id])
            if cursor.rowcount > 0:
                row = cursor.fetchone()
                if row[0]:
                    return row[0]

        return 0


    def items_after_position(self, position):
        return TodoListItem.objects.filter(todo_list_id = id, position__gt = position).order_by('position')


    def normalize_items_order(self):
        todo_items = self.todo_list_items.order_by('position')
        for position, todo_item in todo_items:
            todo_item.position = position + 1
            todo_item.save()



class TodoListItem(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    position = models.IntegerField()
    name = models.CharField(max_length=32)
    done_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.reorder_list_items()
        super(TodoListItem, self).save(*args, **kwargs)


    def is_first(self):
        return self.position == 1


    def is_last(self):
        todo_list = self.todo_list if self.id > 0 else TodoList.objects.get(id=self.todo_list_id)
        return todo_list.last_item_position() == self.position


    def reorder_list_items(self):
        """
        If position is <= 0, then move it to the last_position - position
        Ie if we had [A, B, C]...
         - adding D to position 0 would result in [A, B, C, D]
         - adding D to position -1 would result in [A, B, D, C]
         - etc.
        """

        todo_list = self.todo_list if self.id > 0 else TodoList.objects.get(id=self.todo_list_id)

        last_position = todo_list.last_item_position()

        if self.position <= 0:
            self.position = last_postition - self.position

        self.position = max(1, min(self.position, last_position + 1))

        todo_items = todo_list.items_after_position(self.position)
        for todo_item in reversed(todo_items):
            todo_item.position = todo_item.position + 1
            todo_item.save()
