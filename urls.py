# stdlib
from typing import List
# libs
from django.urls import path
# local
from . import views


urlpatterns: List[path] = [
    # App
    path(
        'app/',
        views.AppCollection.as_view(),
        name='app_collection',
    ),
    path(
        'app/<int:pk>/',
        views.AppResource.as_view(),
        name='app_resource',
    ),

    # Member Link
    path(
        'app/<int:app_id>/member/',
        views.MemberLinkCollection.as_view(),
        name='member_link_collection',
    ),

    # Menu Item
    path(
        'app/<int:app_id>/menu_item/',
        views.MenuItemCollection.as_view(),
        name='menu_item_collection',
    ),
    path(
        'app/<int:app_id>/menu_item/<int:pk>/',
        views.MenuItemResource.as_view(),
        name='menu_item_resource',
    ),

    # Menu Item User Link
    path(
        'menu_item/user/<int:user_id>/',
        views.MenuItemUserLinkCollection.as_view(),
        name='menu_item_user_link_collection',
    ),
]
