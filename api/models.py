# -*- coding: utf-8 -*-
from uuid import uuid4
from django.db import models, connection

# Get some db logging
# import logging
# logger = logging.getLogger('django.db.backends')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

# Note: use this for a live binding.pry experience
# import code
# code.interact(local=dict(globals(), **locals()))


class TodoList(models.Model):
    code = models.CharField(max_length=36, unique=True,
                            default=uuid4, editable=False)
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.code == None or self.code == "":
            self.code = uuid4

        super(TodoList, self).save(*args, **kwargs)

    def todo_list_items(self):
        return TodoListItem.objects.all().filter(todo_list_id=self.id)

    def last_item_position(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    MAX(position) AS last_position
                FROM
                    api_todolistitem
                WHERE
                    todo_list_id = %s
                """, [self.id])
            row = cursor.fetchone()
            last_position = row[0]

            if last_position == None:
                return 0
            else:
                return last_position

    def items_after_position(self, position):
        return TodoListItem.objects.filter(todo_list_id=id, position__gt=position).order_by('position', '-updated_at')


class TodoListItem(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    name = models.CharField(max_length=32)
    done_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    __force_update = False
    __position_was = None

    class Meta:
        ordering = ('position', '-updated_at', 'name')

    def __unicode__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(TodoListItem, self).__init__(*args, **kwargs)
        self.__position_was = self.position

    def force_update(self):
        self.__force_update = True

    def save(self, *args, **kwargs):
        insert_self_at = self.normalized_position()

        needs_create = self.id == None
        position_changed = self.__position_was != insert_self_at

        if needs_create:
            self.position = 0
            super(TodoListItem, self).save(*args, **kwargs)

        if needs_create or position_changed or self.__force_update:
            self.after_save_reorder(insert_self_at)

        self.__force_update = False

    def after_save_reorder(self, insert_self_at):
        positions_with_ids = self.after_save_reorder_positions_with_ids(insert_self_at)

        self.after_save_reorder_update_siblings(positions_with_ids)

    def after_save_reorder_positions_with_ids(self, insert_self_at):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                           SELECT
                               id,
                               position
                           FROM
                               api_todolistitem
                           WHERE
                               todo_list_id = %s
                           ORDER BY
                               position ASC
                           """,
                [self.todo_list_id])

            return self.build_positions_with_ids([], cursor.fetchall(), 1,
                                                insert_self_at)

    def after_save_reorder_update_siblings(self, positions_with_ids):
        with connection.cursor() as cursor:
            cursor.executemany(
                """
                               UPDATE
                                   api_todolistitem
                               SET
                                   position = %s
                               WHERE
                                   id = %s
                               """, positions_with_ids)

    def build_positions_with_ids(self, memo, positions_with_ids, normalized_position, insert_self_at):
        if len(positions_with_ids) == 0:
            return memo

        else:
            (id, position) = positions_with_ids[0]

            if id == self.id and normalized_position != insert_self_at:
                return self.build_positions_with_ids(memo, positions_with_ids[1:], normalized_position, insert_self_at)

            elif id != self.id and normalized_position == insert_self_at:
                to_insert = [
                    (normalized_position, self.id),
                    (normalized_position + 1, id)
                ]

                return self.build_positions_with_ids(memo + to_insert, positions_with_ids[1:], normalized_position + 2, insert_self_at)

            else:
                return self.build_positions_with_ids(memo + [(normalized_position, id)], positions_with_ids[1:], normalized_position + 1, insert_self_at)

    def is_first(self):
        return self.position == 1

    def is_last(self):
        todo_list = self.todo_list if self.id > 0 else TodoList.objects.get(
            id=self.todo_list_id)
        return todo_list.last_item_position() == self.position

    def normalized_position(self):
        todo_list = self.todo_list if self.id > 0 else TodoList.objects.get(
            id=self.todo_list_id)

        last_position = todo_list.last_item_position()

        normalized_position = self.position
        if self.position <= 0:
            normalized_position = last_position - self.position

        return max(1, min(normalized_position, last_position + 1))
