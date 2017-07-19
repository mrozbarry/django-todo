from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .models import TodoList, TodoListItem


class TodoListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoList
        fields = ('id', 'code', 'name')
        lookup_field = 'code'
        extra_kwargs = {
            'url': {'lookup_field': 'code'}
        }

        todo_items = NestedHyperlinkedRelatedField(
            many=True,
            view_name='todo-list-items-list',
            read_only=True,
        )


class TodoListItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoListItem
        fields = ('id', 'position', 'name', 'done_at')
