# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import TodoListSerializer, TodoListItemSerializer
from .models import TodoList, TodoListItem


class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    lookup_field = 'code'


class TodoListItemViewSet(viewsets.ModelViewSet):
    queryset = TodoListItem.objects.all()
    serializer_class = TodoListItemSerializer

    def list(self, request, todo_list_code=None):
        todo_list = TodoList.objects.get(code=todo_list_code)
        queryset = self.queryset.filter(todo_list_id=todo_list.id)
        serializer = TodoListItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, todo_list_code=None):
        todo_list = TodoList.objects.get(code=todo_list_code)
        todo_list_item = get_object_or_404(Client.objects.filter(), todo_list_id=todo_list.id)
        serializer = TodoListItemSerializer(todo_list_item)
        return Response(serializer.data)
