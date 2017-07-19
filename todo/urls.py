from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_nested import routers

from api import views

"""
API Stuff
"""
router = routers.SimpleRouter()
router.register(r'todo_lists', views.TodoListViewSet)

items_router = routers.NestedSimpleRouter(router, r'todo_lists', lookup='todo_list')
items_router.register(r'todo_list_items', views.TodoListItemViewSet, base_name='todo-list-items')

urlpatterns = [
    # API
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(items_router.urls)),
    url(r'^api/', include(items_router.urls)),
    # SPA
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'[^\s]{36}$', TemplateView.as_view(template_name="index.html")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
