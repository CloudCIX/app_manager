"""
Management for Member Links
"""

# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import BaseView
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from app_manager.controllers.member_link import MemberLinkCreateController
from app_manager.models import App, MemberLink
from app_manager.permissions.member_link import Permissions


__all__ = [
    'MemberLinkCollection',
]


class MemberLinkCollection(BaseView):
    """
    Handles methods regarding Member Link records that do not require an id to be specified, i.e. create, delete
    """

    def post(self, request: Request, app_id: int) -> Response:
        """
        summary: Create a Member Link record

        description: |
            Create a Member Link record using data supplied by the User

        path_params:
            app_id:
              description: The id of the App that a Member Link will be created for
              type: integer

        responses:
            200:
                description: Member Link record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MemberLinkCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = App.objects.get(id=app_id)
            except App.DoesNotExist:
                return Http404(error_code='app_manager_member_link_create_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request, obj, controller.cleaned_data['member_id'])
            if err is not None:
                return err

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.app = obj
            controller.instance.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, app_id: int) -> Response:
        """
        summary: Delete a Member Link record

        description: |
            Delete the specified Member Link record, returning a 404 if it doesn't exist

        path_params:
            app_id:
              description: The id of the App that the Member no longer uses
              type: integer

        responses:
            200:
                description: Member Link record was deleted successfully
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = MemberLink.objects.get(
                    member_id=request.user.member['id'],
                    app_id=app_id,
                )
            except MemberLink.DoesNotExist:
                return Http404(error_code='app_manager_member_link_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        with tracer.start_span('setting_deleted_field', child_of=request.span):
            obj.deleted = datetime.utcnow()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
