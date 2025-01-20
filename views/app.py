"""
Management for Apps
"""

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
from app_manager.controllers import (
    AppCreateController,
    AppListController,
    AppUpdateController,
)
from app_manager.models import App, MemberLink, MenuItem, MenuItemUserLink
from app_manager.permissions.app import Permissions
from app_manager.serializers.app import AppSerializer


__all__ = [
    'AppCollection',
    'AppResource',
]


class AppCollection(BaseView):
    """
    Handles methods regarding App records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of App records

        description: |
            Retrieve a list of App records that the requesting User is linked to.

        responses:
            200:
                description: A list of App records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('', child_of=request.span) as span:
            controller = AppListController(data=request.GET, request=request, span=span)
            # By validating the controller we generate the search filters
            controller.is_valid()

        with tracer.start_span('ensure_default_apps', child_of=request.span):
            if request.user.id != 1:
                member_links = MemberLink.objects.filter(
                    member_id__in=[0, request.user.member['id']],
                )
                default_app_ids = set()
                user_app_ids = set()
                for link in member_links:
                    if link.member_id == 0:
                        default_app_ids.add(link.app_id)
                    else:
                        user_app_ids.add(link.app_id)

                new_links = list()
                for missing_app_id in (default_app_ids - user_app_ids):
                    new_links.append(MemberLink(
                        app_id=missing_app_id,
                        member_id=request.user.member['id'],
                    ))
                if len(new_links) > 0:
                    MemberLink.objects.bulk_create(new_links)

        with tracer.start_span('setting_search_filters', child_of=request.span):
            kw = controller.cleaned_data['search']
            if request.user.id != 1:
                # Limit the Apps to those that the User's Member is linked to
                kw.update({
                    'member_links__member_id': request.user.member['id'],
                    'member_links__deleted__isnull': True,
                    'online': True,
                })

            if not request.user.administrator:
                # Limit the user to apps that they have a UserLink with
                links = set(MenuItemUserLink.objects.filter(
                    user_id=request.user.id,
                    menu_item__deleted__isnull=True,
                ).values_list(
                    'menu_item__app_id',
                    flat=True,
                ))
                if kw.get('id__in', False):
                    id_set = {int(i) for i in kw['id__in']}
                    kw['id__in'] = id_set & links
                else:
                    kw['id__in'] = links

        with tracer.start_span('get_objects', child_of=request.span):
            kw['deleted__isnull'] = True
            public_app_ids = MenuItem.objects.filter(public=True).values_list('app_id')
            is_public = Q(id__in=public_app_ids)
            try:
                objs = App.objects.filter(
                    Q(**kw) | is_public,
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                ).distinct()
            except (ValueError, ValidationError):
                return Http400(error_code='app_manager_app_list_001')

        with tracer.start_span('gathering_metadata', child_of=request.span):
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            total_records = objs.count()
            metadata = {
                'page': page,
                'limit': limit,
                'order': controller.cleaned_data['order'],
                'total_records': total_records,
            }
            objs = objs[page * limit: (page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = AppSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create an App record

        description: |
            Create an App record using data supplied by the User

        responses:
            201:
                description: App record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AppCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AppSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class AppResource(BaseView):
    """
    Handles methods regarding App records that require an id to be specified, i.e. read, update, delete
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified App record

        description: |
            Attempt to read an App record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the App record to be read
                type: integer

        responses:
            200:
                description: App record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = App.objects.get(id=pk)
            except App.DoesNotExist:
                return Http404(error_code='app_manager_app_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AppSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update an App record

        description: |
            Attempt to update an App record by the given `pk`, returning a 404 if it does not exist.

        path_params:
            pk:
                description: The id of the App record to be read
                type: integer

        responses:
            200:
                description: App record was updated successfully
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
                obj = App.objects.get(id=pk)
            except App.DoesNotExist:
                return Http404(error_code='app_manager_app_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AppUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AppSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update an App record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int) -> Response:
        """
        summary: Delete a specified App record

        description: |
            Attempt to delete a App record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the App record to delete
                type: integer

        responses:
            204:
                description: App record was deleted successfully
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
                obj = App.objects.get(id=pk)
            except App.DoesNotExist:
                return Http404(error_code='app_manager_app_delete_001')

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.set_deleted()

        return Response(status=status.HTTP_204_NO_CONTENT)
