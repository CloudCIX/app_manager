# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from app_manager.models.app import App


__all__ = [
    'MenuItem',
]


class MenuItemManager(BaseManager):
    """
    Manager for Menu Items which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'app',
        )


class MenuItem(BaseModel):
    """
    Menu Items are used for organising, and navigating through, the structure of an App
    """
    action = models.CharField(max_length=150, null=True)
    administrator_only = models.BooleanField(default=False)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='menu_items')
    help = models.TextField(default='No help for this menu item', null=True)
    name = models.CharField(max_length=150)
    predecessor = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, related_name='children')
    public = models.BooleanField(default=False)
    self_managed = models.BooleanField(default=True)
    sequence = models.IntegerField()

    objects = MenuItemManager()

    class Meta:
        """
        Metadata about the model for django to use in whatever way it sees fit
        """
        db_table = 'menu_item'

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the MenuItemResource view for this Menu Item record
        :return: A URL that corresponds to the views for this Menu Item record
        """
        return reverse('menu_item_resource', kwargs={'app_id': self.app_id, 'pk': self.id})
