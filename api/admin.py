# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import TodoList, TodoListItem

# Register your models here.

admin.site.register(TodoList)
admin.site.register(TodoListItem)
