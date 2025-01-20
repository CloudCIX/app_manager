# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
# local
from app_manager.models.app import App


__all__ = [
    'MemberLink',
]


class MemberLinkManager(BaseManager):
    """
    Manager for Member Links which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'app',
        )


class MemberLink(BaseModel):
    """
    A Member Link is used to control whether a Member is using an App
    """
    member_id = models.IntegerField()
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='member_links')

    objects = MemberLinkManager()

    class Meta:
        """
        Metadata about the model for django to use in whatever way it sees fit
        """
        db_table = 'member_link'
