# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from app_manager.models.member_link import MemberLink
from app_manager.models.menu_item import MenuItem
from app_manager.models.menu_item_user_link import MenuItemUserLink


__all__ = [
    'Permissions',
]


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create an App is valid if;
        - The requesting User's Member is Member 1
        """
        # The requesting User's Member is Member 1
        if request.user.member['id'] != 1:
            return Http403(error_code='app_manager_menu_item_create_201')
        return None

    @staticmethod
    def read(request: Request, obj: MenuItem):
        """
        The request to read an App is valid if;
        - The Menu Item is public or the requesting user is from member 1
        - The requesting user is an admin whose Member has a Link for the App
        - The requesting user has a Menu Item User Link set up
        """
        # The Menu Item is public or the requesting user is from Member 1
        if not obj.public and request.user.member['id'] != 1:

            # The requesting user is an admin whose Member has a Link for the App
            if request.user.administrator:
                # Check Member Link
                link = MemberLink.objects.filter(
                    app=obj.app,
                    member_id=request.user.member['id'],
                )
                if not link.exists():
                    return Http403(error_code='app_manager_menu_item_read_201')
            # The requesting user has a Menu Item User Link set up
            else:
                # Check User Link
                link = MenuItemUserLink.objects.filter(
                    user_id=request.user.id,
                    menu_item=obj,
                )
                if not link.exists():
                    return Http403(error_code='app_manager_menu_item_read_202')

        return None

    @staticmethod
    def update(request: Request):
        """
        The request to update a Menu Item is valid if;
        - The requesting User's Member is Member 1
        """
        # The requesting User's Member is Member 1
        if request.user.member['id'] != 1:
            return Http403(error_code='app_manager_menu_item_update_201')
        return None

    @staticmethod
    def delete(request: Request):
        """
        The request to delete a Menu Item is valid if;
        - The requesting User's Member is Member 1
        """
        # The requesting User's Member is Member 1
        if request.user.member['id'] != 1:
            return Http403(error_code='app_manager_menu_item_delete_201')
        return None
