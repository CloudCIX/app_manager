"""
Management for Menu Item User Links
"""

# libs
from cloudcix_rest.exceptions import Http400
from cloudcix_rest.views import BaseView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from app_manager.controllers.menu_item_user_link import (
    MenuItemUserLinkListController,
    MenuItemUserLinkUpdateController,
)
from app_manager.models import MemberLink, MenuItem, MenuItemUserLink
from app_manager.permissions.menu_item_user_link import Permissions
from app_manager.serializers.menu_item import MenuItemSerializer


__all__ = [
    'MenuItemUserLinkCollection',
]


class MenuItemUserLinkCollection(BaseView):
    """
    Handles methods regarding Menu Item User Link records that do not require an id to be specified, i.e. list, update
    """

    serializer_class = MenuItemSerializer

    def get(self, request: Request, user_id: int) -> Response:
        """
        summary: Retrieve a list of Menu Item records that a User can access

        description: |
            Retrieve a list of Menu Item records where there are Menu Item User Links set up for the given User id

        path_params:
            user_id:
                description: The id of the User to list Menu Items for
                type: integer

        responses:
            200:
                description: A list of Menu Item records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.list(request, user_id)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MenuItemUserLinkListController(data=request.GET, request=request, span=span)
            # By validating the controller we generate the search filters
            controller.is_valid()

        with tracer.start_span('setting_search_filters', child_of=request.span):
            kw = controller.cleaned_data['search']

            # Limit the results to the the Menu Items that user_id has access to
            links = set(MenuItemUserLink.objects.filter(
                user_id=user_id,
            ).values_list(
                'menu_item_id',
                flat=True,
            ).distinct())

            if 'id__in' in kw:
                id_set = {int(i) for i in kw['id__in']}
                kw['id__in'] = id_set & links
            else:
                kw['id__in'] = links

            # Limit the results to Apps where a Member Link exists for the User
            apps = MemberLink.objects.filter(
                member_id=request.user.member['id'],
            ).values_list(
                'app_id',
                flat=True,
            )
            kw['app_id__in'] = apps

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = MenuItem.objects.filter(
                    **kw,
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='app_manager_menu_item_user_link_list_001')

        with tracer.start_span('gathering_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            metadata = {
                'page': page,
                'limit': limit,
                'order': controller.cleaned_data['order'],
                'total_records': total_records,
            }
            objs = objs[page * limit: (page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = MenuItemSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def put(self, request: Request, user_id: int, partial: bool = False) -> Response:
        """
        summary: Update the Menu Item Links for a User

        description: |
            Update the details of a Menu Item User Link with data provided by the User

        path_params:
            user_id:
                description: The id of the User to list Menu Items for
                type: integer

        responses:
            200:
                description: A list of Menu Item records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request, user_id)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MenuItemUserLinkUpdateController(
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            controller.kwargs = {'user_id': user_id}
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('updating_user_links', child_of=request.span):
            menu_item_ids = controller.cleaned_data['menu_item_ids']
            # Delete the Menu Items that were not requested by the user
            MenuItemUserLink.objects.filter(
                user_id=user_id,
            ).exclude(
                menu_item_id__in=menu_item_ids,
            ).delete()

            # Create any User Links that are in the requesting User's list but that don't exist yet
            existing = MenuItemUserLink.objects.filter(
                user_id=user_id,
                menu_item__deleted__isnull=True,
            ).values_list(
                'menu_item_id',
                flat=True,
            )
            to_create = MenuItem.objects.filter(
                id__in=menu_item_ids,
            ).exclude(
                id__in=existing,
            )
            new_links = list()
            for c in to_create:
                new_links.append(
                    MenuItemUserLink(
                        user_id=user_id,
                        menu_item=c,
                    ),
                )
            MenuItemUserLink.objects.bulk_create(new_links)

        return Response(status=status.HTTP_204_NO_CONTENT)
