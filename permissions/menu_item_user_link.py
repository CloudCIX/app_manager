# stdlib
from typing import Optional
# libs
from cloudcix.api.membership import Membership
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request


__all__ = [
    'Permissions',
]


class Permissions:

    @staticmethod
    def list(request: Request, user_id: int) -> Optional[Http403]:
        """
        The request to list a User's Menu Item Links is valid if;
        - The requesting User is reading their own links
        - The requesting User can read the other User's data from Membership
        - The requesting User is reading the Links of a User in the same Member
        """
        # The requesting User is reading their own links
        if request.user.id != user_id:

            # The requesting User can read the other User's data from Membership
            response = Membership.user.read(
                token=request.user.token,
                pk=user_id,
            )
            if response.status_code != 200:
                return Http403(error_code='app_manager_menu_item_user_link_list_201')

            # The requesting User is reading the Links of a User in the same Member
            user = response.json()['content']
            if user['member']['id'] != request.user.member['id']:
                return Http403(error_code='app_manager_menu_item_user_link_list_202')

        return None

    @staticmethod
    def update(request: Request, user_id: int) -> Optional[Http403]:
        """
        The request to list a User's Menu Item Links is valid if;
        - The requesting User is an administrator
        - The requesting User's Member is self-managed
        - The requesting User can read the User's details from Membership
        """
        # The requesting User is an administrator
        if not request.user.administrator:
            return Http403(error_code='app_manager_menu_item_user_link_update_201')

        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='app_manager_menu_item_user_link_update_202')

        # The requesting User can read the User's details from Membership
        if request.user.id != user_id:
            response = Membership.user.read(
                token=request.user.token,
                pk=user_id,
            )
            if response.status_code != 200:
                return Http403(error_code='app_manager_menu_item_user_link_update_203')

        return None
