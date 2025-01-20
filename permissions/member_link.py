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
    def create(request: Request, app: App, member_id: int) -> Optional[Http403]:
        """
        The request to create an App is valid if;
        - The requesting User is an administrator
        - The App is private and the User is a superuser
        - A Member Link does not already exist
        """
        # The requesting User is an administrator
        if not request.user.administrator:
            return Http403(error_code='app_manager_member_link_create_201')

        # The App is private and the user is a superuser
        if app.private and request.user.id != 1:
            return Http403(error_code='app_manager_member_link_create_202')

        if MemberLink.objects.filter(
            app=app,
            member_id=member_id,
        ).exists():
            return Http403(error_code='app_manager_member_link_create_203')

        return None

    @staticmethod
    def delete(request: Request, link: MemberLink) -> Optional[Http403]:
        """
        The request to delete an App is valid if;
        - The requesting User is an administrator
        - The App is private and the User is a superuser
        """
        # The requesting User is an administrator
        if not request.user.administrator:
            return Http403(error_code='app_manager_member_link_delete_201')

        # The App is private and the user is a superuser
        if link.app.private and request.user.id != 1:
            return Http403(error_code='app_manager_member_link_delete_202')

        return None
