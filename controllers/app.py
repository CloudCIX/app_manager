# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from app_manager.models import App


__all__ = [
    'AppListController',
    'AppCreateController',
    'AppUpdateController',
]


class AppListController(ControllerBase):
    """
    Validates User data used to filter a list of App records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'id',
            'member_links_id',
            'name',
        )
        search_fields = {
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'in_app_store': (),
            'maintenance': (),
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'private': (),
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class AppCreateController(ControllerBase):
    """
    Validates User data used to create a new App record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = App
        validation_order = (
            'action',
            'description',
            'icon_url',
            'name',
            'online',
            'in_app_store',
            'private',
            'maintenance',
            'extra',
        )

    def validate_action(self, action: Optional[str]) -> Optional[str]:
        """
        description: A url for the App's homepage
        type: string
        required: false
        """
        if action is None:
            return None
        action = str(action).strip()
        if len(action) > self.get_field('action').max_length:
            return 'app_manager_app_create_101'
        self.cleaned_data['action'] = action
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: A summary of what the App is used for
        type: string
        """
        if description is None:
            return None
        self.cleaned_data['description'] = str(description).strip()
        return None

    def validate_icon_url(self, icon_url: Optional[str]) -> Optional[str]:
        """
        description: The url where the App's display icon can be found
        type: string
        """
        if icon_url is None:
            icon_url = ''
        icon_url = str(icon_url).strip()
        if len(icon_url) == 0:
            return 'app_manager_app_create_102'
        if len(icon_url) > self.get_field('icon_url').max_length:
            return 'app_manager_app_create_103'
        self.cleaned_data['icon_url'] = icon_url
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the App
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'app_manager_app_create_104'
        if len(name) > self.get_field('name').max_length:
            return 'app_manager_app_create_105'
        if App.objects.filter(name__iexact=name).exists():
            return 'app_manager_app_create_106'
        self.cleaned_data['name'] = name
        return None

    def validate_online(self, online: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App is active and accessible
        type: boolean
        """
        if online is None:
            return None
        if not isinstance(online, bool):
            return 'app_manager_app_create_107'
        self.cleaned_data['online'] = online
        return None

    def validate_in_app_store(self, in_app_store: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App is available to install from the app store
        type: boolean
        """
        if in_app_store is None:
            return None
        if not isinstance(in_app_store, bool):
            return 'app_manager_app_create_108'
        self.cleaned_data['in_app_store'] = in_app_store
        return None

    def validate_private(self, private: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App can be seen by all Members or not
        type: boolean
        """
        if private is None:
            return None
        if not isinstance(private, bool):
            return 'app_manager_app_create_109'
        self.cleaned_data['private'] = private
        return None

    def validate_maintenance(self, maintenance: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App is temporarily unavailable to allow updates to be made
        type: boolean
        """
        if maintenance is None:
            return None
        if not isinstance(maintenance, bool):
            return 'app_manager_app_create_110'
        self.cleaned_data['maintenance'] = maintenance
        return None

    def validate_extra(self, extra: Optional[dict]) -> Optional[str]:
        """
        description: Any miscellaneous information to attach to this App
        type: boolean
        """
        if extra is None:
            return None
        if not isinstance(extra, dict):
            return 'app_manager_app_create_111'
        self.cleaned_data['extra'] = extra
        return None


class AppUpdateController(ControllerBase):
    """
    Validates User data used to update an App record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = App
        validation_order = (
            'action',
            'description',
            'icon_url',
            'name',
            'online',
            'in_app_store',
            'private',
            'maintenance',
            'extra',
        )

    def validate_action(self, action: Optional[str]) -> Optional[str]:
        """
        description: A url for the App's homepage
        type: string
        required: false
        """
        if action is None:
            return None
        action = str(action).strip()
        if len(action) > self.get_field('action').max_length:
            return 'app_manager_app_update_101'
        self.cleaned_data['action'] = action
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: A summary of what the App is used for
        type: string
        """
        if description is None:
            return None
        self.cleaned_data['description'] = str(description).strip()
        return None

    def validate_icon_url(self, icon_url: Optional[str]) -> Optional[str]:
        """
        description: The url where the App's display icon can be found
        type: string
        """
        if icon_url is None:
            icon_url = ''
        icon_url = str(icon_url).strip()
        if len(icon_url) == 0:
            return 'app_manager_app_update_102'
        if len(icon_url) > self.get_field('icon_url').max_length:
            return 'app_manager_app_update_103'
        self.cleaned_data['icon_url'] = icon_url
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the App
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'app_manager_app_update_104'
        if len(name) > self.get_field('name').max_length:
            return 'app_manager_app_update_105'
        if App.objects.filter(name__iexact=name).exclude(pk=self._instance.pk).exists():
            return 'app_manager_app_update_106'
        self.cleaned_data['name'] = name
        return None

    def validate_online(self, online: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App is active and accessible
        type: boolean
        """
        if online is None:
            return None
        if not isinstance(online, bool):
            return 'app_manager_app_update_107'
        self.cleaned_data['online'] = online
        return None

    def validate_in_app_store(self, in_app_store: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App is available to install from the app store
        type: boolean
        """
        if in_app_store is None:
            return None
        if not isinstance(in_app_store, bool):
            return 'app_manager_app_update_108'
        self.cleaned_data['in_app_store'] = in_app_store
        return None

    def validate_private(self, private: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App can be seen by all Members or not
        type: boolean
        """
        if private is None:
            return None
        if not isinstance(private, bool):
            return 'app_manager_app_update_109'
        self.cleaned_data['private'] = private
        return None

    def validate_maintenance(self, maintenance: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if the App is temporarily unavailable to allow updates to be made
        type: boolean
        """
        if maintenance is None:
            return None
        if not isinstance(maintenance, bool):
            return 'app_manager_app_update_110'
        self.cleaned_data['maintenance'] = maintenance
        return None

    def validate_extra(self, extra: Optional[dict]) -> Optional[str]:
        """
        description: Any miscellaneous information to attach to this App
        type: boolean
        """
        if extra is None:
            return None
        if not isinstance(extra, dict):
            return 'app_manager_app_update_111'
        self.cleaned_data['extra'] = extra
        return None
