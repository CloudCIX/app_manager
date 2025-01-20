# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
# local
from app_manager.models.menu_item import MenuItem


__all__ = [
    'MenuItemUserLink',
]


class MenuItemUserLinkManager(BaseManager):
    """
    Manager for Menu Item User Links which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'menu_item',
            'menu_item__app',
        )


class MenuItemUserLink(BaseModel):
    user_id = models.IntegerField()
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='user_links')

    objects = MenuItemUserLinkManager()

    class Meta:
        """
        Metadata about the model for django to use in whatever way it sees fit
        """
        db_table = 'menu_item_user_link'
        unique_together = ('user_id', 'menu_item')
