# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from app_manager.models.app import App
from app_manager.models.member_link import MemberLink


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
            return Http403(error_code='app_manager_app_create_201')
        return None

    @staticmethod
    def read(request: Request, obj: App):
        """
        The request to read an App is valid if:
        - The requesting User's Member is member 1
        - The requesting User's Member has a Member Link for the App
        """
        if request.user.member['id'] == 1:
            return None

        link = MemberLink.objects.filter(
            app=obj,
            member_id=request.user.member['id'],
        )
        if not link.exists():
            return Http403(error_code='app_manager_app_read_201')

        return None

    @staticmethod
    def update(request: Request):
        """
        The request to read an App is valid if:
        - The requesting User's Member is member 1
        """
        if request.user.member['id'] != 1:
            return Http403(error_code='app_manager_app_update_201')

        return None

    @staticmethod
    def delete(request: Request):
        """
        The request to delete an App is valid if:
        - The requesting User's Member is member 1
        """
        if request.user.member['id'] != 1:
            return Http403(error_code='app_manager_app_delete_201')

        return None
