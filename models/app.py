# stdlib
from datetime import datetime
# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse


__all__ = [
    'App',
]


class App(BaseModel):
    """
    An App record controls information and access to CloudCIX Apps while using the UI
    """
    action = models.CharField(max_length=8000, null=True)
    description = models.TextField(null=True)
    icon_url = models.CharField(max_length=8000, null=True)
    in_app_store = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    online = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    class Meta:
        """
        Metadata about the model for django to use in whatever way it sees fit
        """
        db_table = 'app'
        indexes = [
            # Indexing everything in the `search_fields` map in List Controller
            models.Index(fields=['id'], name='app_id'),
            models.Index(fields=['created'], name='app_created'),
            models.Index(fields=['in_app_store'], name='app_in_app_store'),
            models.Index(fields=['maintenance'], name='app_maintenance'),
            models.Index(fields=['name'], name='app_name'),
            models.Index(fields=['private'], name='app_private'),
            models.Index(fields=['updated'], name='app_updated'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the AppResource view for this App record
        :return: A URL that corresponds to the views for this App record
        """
        return reverse('app_resource', kwargs={'pk': self.pk})

    def set_deleted(self):
        """
        Set the deleted field for the App and its Menu Items
        """
        deleted = datetime.utcnow()
        self.deleted = deleted
        self.save()
        for m in self.menu_items.all():
            m.deleted = deleted
            m.save()
        return self
