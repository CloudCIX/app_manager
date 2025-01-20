"""
Management for Member Items
"""

# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import BaseView
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from app_manager.controllers.menu_item import (
    MenuItemCreateController,
    MenuItemListController,
    MenuItemUpdateController,
)
from app_manager.models import (
    App,
    MemberLink,
    MenuItem,
    MenuItemUserLink,
)
from app_manager.permissions.menu_item import Permissions
from app_manager.serializers.menu_item import MenuItemSerializer


__all__ = [
    'MenuItemCollection',
    'MenuItemResource',
]


class MenuItemCollection(BaseView):
    """
    Handles methods regarding Menu Item records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request, app_id: int) -> Response:
        """
        summary: List Menu Item records

        description: |
            Get a list of Menu Item records, filtered and ordered by the User

        path_params:
            app_id:
              description: The id of the App that the Menu Items should belong to
              type: integer

        responses:
            200:
                description: A list of Menu Items
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MenuItemListController(data=request.GET, request=request, span=span)
            # By validating the controller we generate the search filters
            controller.is_valid()

        with tracer.start_span('setting_search_filters', child_of=request.span):
            link = MemberLink.objects.filter(
                app_id=app_id,
                member_id=request.user.member['id'],
            )
            kw = controller.cleaned_data['search']
            search_filters = Q(
                public=True,
                app_id=app_id,
            )
            if request.user.id == 1 or link.exists():
                if not request.user.member['self_managed']:
                    kw['self_managed'] = False

                if not request.user.administrator:
                    kw['administrator_only'] = False
                    links = MenuItemUserLink.objects.filter(
                        user_id=request.user.id,
                    ).distinct().values_list(
                        'menu_item_id',
                        flat=True,
                    )
                    if 'id__in' in kw:
                        kw['id__in'] = set(kw['id__in']).intersection(links)
                    else:
                        kw['id__in'] = links
                search_filters |= Q(
                    app_id=app_id,
                    **kw,
                )

        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            order = controller.cleaned_data['order']
            try:
                objs = MenuItem.objects.filter(
                    search_filters,
                ).order_by(
                    order,
                ).distinct()
            except (ValueError, ValidationError):
                return Http400(error_code='app_manager_menu_item_list_001')

        with tracer.start_span('gathering_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            # Pagination
            objs = objs[page * limit:(page + 1) * limit]
            metadata = {
                'page': page,
                'limit': limit,
                'order': order,
                'total_records': total_records,
            }

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objs', len(objs))
            data = MenuItemSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request, app_id: int) -> Response:
        """
        summary: Create a Menu Item record

        description: |
            Create a Menu Item record using data supplied by the User

        path_params:
            app_id:
              description: The id of the App that the new Menu Item should belong to
              type: integer

        responses:
            201:
                description: Menu Item record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_app', child_of=request.span):
            try:
                app = App.objects.get(id=app_id)
            except App.DoesNotExist:
                return Http404(error_code='app_manager_menu_item_create_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MenuItemCreateController(data=request.data, request=request, span=span)
            controller.kwargs = {'app_id': app_id}
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.app = app
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = MenuItemSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class MenuItemResource(BaseView):
    """
    Handles methods regarding Menu Item records that require an id to be specified, i.e. read, update, delete
    """

    def get(self, request: Request, pk: int, app_id: int) -> Response:
        """
        summary: Read the details of a specified Menu Item record

        description: |
            Attempt to read a Menu Item record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Menu Item record to be read
                type: integer
            app_id:
                description: The id of the App that the Menu Item belongs to
                type: integer

        responses:
            200:
                description: Menu Item record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = MenuItem.objects.get(
                    id=pk,
                    app_id=app_id,
                )
            except MenuItem.DoesNotExist:
                return Http404(error_code='app_manager_menu_item_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = MenuItemSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, app_id: int, partial: bool = False) -> Response:
        """
        summary: Update an Menu Item record

        description: |
            Attempt to update an Menu Item record by the given `pk`, returning a 404 if it does not exist.

        path_params:
            pk:
                description: The id of the Menu Item record to be updated
                type: integer
            app_id:
                description: The id of the App that the Menu Item belongs to
                type: integer

        responses:
            200:
                description: Menu Item record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = MenuItem.objects.get(
                    id=pk,
                    app_id=app_id,
                )
            except MenuItem.DoesNotExist:
                return Http404(error_code='app_manager_menu_item_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MenuItemUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            controller.kwargs = {'app_id': app_id}
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = MenuItemSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int, app_id: int) -> Response:
        """
        Attempt to partially update an Menu Item record
        """
        return self.put(request, pk, app_id, True)

    def delete(self, request: Request, pk: int, app_id: int) -> Response:
        """
        summary: Delete a specified Menu Item record

        description: |
            Attempt to delete a Menu Item record by the given `pk` and `app_id`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Menu Item record to delete
                type: integer
            app_id:
                description: The id of the App that the Menu Item belongs to
                type: integer

        responses:
            204:
                description: Menu Item record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = MenuItem.objects.get(
                    id=pk,
                    app_id=app_id,
                )
            except MenuItem.DoesNotExist:
                return Http404(error_code='app_manager_menu_item_delete_001')

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.deleted = datetime.utcnow()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
