# stdlib
from typing import cast, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from app_manager.models.menu_item import MenuItem


__all__ = [
    'MenuItemListController',
    'MenuItemCreateController',
    'MenuItemUpdateController',
]


class MenuItemListController(ControllerBase):
    """
    Validates User data used to filter a list of Menu Item records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'id',
            'name',
        )
        search_fields = {
            'app_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'public': (),
            'self_managed': (),
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class MenuItemCreateController(ControllerBase):
    """
    Validates User data used to create a new Menu Item record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = MenuItem
        validation_order = (
            'administrator_only',
            'predecessor_id',
            'sequence',
            'public',
            'help',
            'action',
            'name',
            'self_managed',
        )

    def validate_administrator_only(self, administrator_only: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if User's must be an admin
        type: boolean
        required: false
        """
        if administrator_only is None:
            administrator_only = False
        if not isinstance(administrator_only, bool):
            return 'app_manager_menu_item_create_101'
        self.cleaned_data['administrator_only'] = administrator_only
        return None

    def validate_predecessor_id(self, predecessor_id: Optional[int]) -> Optional[str]:
        """
        description: Another Menu Item that this new Menu Item will exist under
        type: integer
        required: false
        """
        if predecessor_id is None:
            return None
        try:
            predecessor = MenuItem.objects.get(
                pk=int(cast(int, predecessor_id)),
                app_id=self.kwargs['app_id'],
            )
        except (TypeError, ValueError):
            return 'app_manager_menu_item_create_102'
        except MenuItem.DoesNotExist:
            return 'app_manager_menu_item_create_103'
        self.cleaned_data['predecessor'] = predecessor
        return None

    def validate_sequence(self, sequence: Optional[int]) -> Optional[str]:
        """
        description: Determines the order of Menu Items with the same predecessor
        type: integer
        """
        try:
            sequence = int(cast(int, sequence))
        except (TypeError, ValueError):
            return 'app_manager_menu_item_create_104'

        if 'predecessor_id' in self.errors:
            return None

        predecessor = self.cleaned_data.get('predecessor')
        if MenuItem.objects.filter(
            sequence=sequence,
            app_id=self.kwargs['app_id'],
            predecessor=predecessor,
        ).exists():
            return 'app_manager_menu_item_create_105'
        self.cleaned_data['sequence'] = sequence
        return None

    def validate_public(self, public: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if all Users have access to this Menu Item
        type: boolean
        required: false
        """
        if public is None:
            public = True
        if not isinstance(public, bool):
            return 'app_manager_menu_item_create_106'
        self.cleaned_data['public'] = public
        return None

    def validate_help(self, help: Optional[str]) -> Optional[str]:
        """
        description: Help text describing what the Menu Item is used for
        type: string
        required: false
        """
        if help is None:
            help = ''
        self.cleaned_data['help'] = help
        return None

    def validate_action(self, action: Optional[str]) -> Optional[str]:
        """
        description: A url that a the Menu Item will redirect to
        type: string
        required: false
        """
        if action is None:
            action = ''
        action = str(action).strip()
        if len(action) > self.get_field('action').max_length:
            return 'app_manager_menu_item_create_107'
        self.cleaned_data['action'] = action
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Menu Item
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'app_manager_menu_item_create_108'
        if len(name) > self.get_field('name').max_length:
            return 'app_manager_menu_item_create_109'

        if 'predecessor_id' in self.errors:
            return None

        predecessor = self.cleaned_data.get('predecessor')
        if MenuItem.objects.filter(
            name=name,
            app_id=self.kwargs['app_id'],
            predecessor=predecessor,
        ).exists():
            return 'app_manager_menu_item_create_110'

        self.cleaned_data['name'] = name
        return None

    def validate_self_managed(self, self_managed: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if User's must be in self-managed members in order to view the Menu Item
        type: boolean
        required: false
        """
        if self_managed is None:
            self_managed = True
        if not isinstance(self_managed, bool):
            return 'app_manager_menu_item_create_111'
        self.cleaned_data['self_managed'] = self_managed
        return None


class MenuItemUpdateController(ControllerBase):
    """
    Validates User data used to update a new Menu Item record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = MenuItem
        validation_order = (
            'administrator_only',
            'predecessor_id',
            'sequence',
            'public',
            'help',
            'action',
            'name',
            'self_managed',
        )

    def validate_administrator_only(self, administrator_only: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if User's must be an admin
        type: boolean
        required: false
        """
        if administrator_only is None:
            administrator_only = False
        if not isinstance(administrator_only, bool):
            return 'app_manager_menu_item_update_101'
        self.cleaned_data['administrator_only'] = administrator_only
        return None

    def validate_predecessor_id(self, predecessor_id: Optional[int]) -> Optional[str]:
        """
        description: Another Menu Item that this new Menu Item will exist under
        type: integer
        required: false
        """
        if predecessor_id is None:
            self.cleaned_data['predecessor'] = None
            return None
        try:
            predecessor = MenuItem.objects.exclude(
                id=self._instance.pk,
            ).get(
                pk=int(cast(int, predecessor_id)),
                app_id=self.kwargs['app_id'],
            )
        except (TypeError, ValueError):
            return 'app_manager_menu_item_update_102'
        except MenuItem.DoesNotExist:
            return 'app_manager_menu_item_update_103'
        self.cleaned_data['predecessor'] = predecessor
        return None

    def validate_sequence(self, sequence: Optional[int]) -> Optional[str]:
        """
        description: Determines the order of Menu Items with the same predecessor
        type: integer
        """
        try:
            sequence = int(cast(int, sequence))
        except (TypeError, ValueError):
            return 'app_manager_menu_item_update_104'

        if 'predecessor_id' in self.errors:
            return None

        predecessor = self.cleaned_data.get('predecessor')
        if MenuItem.objects.filter(
            sequence=sequence,
            app_id=self.kwargs['app_id'],
            predecessor=predecessor,
        ).exclude(
            pk=self._instance.pk,
        ).exists():
            return 'app_manager_menu_item_update_105'
        self.cleaned_data['sequence'] = sequence
        return None

    def validate_public(self, public: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if all Users have access to this Menu Item
        type: boolean
        required: false
        """
        if public is None:
            public = True
        if not isinstance(public, bool):
            return 'app_manager_menu_item_update_106'
        self.cleaned_data['public'] = public
        return None

    def validate_help(self, help: Optional[str]) -> Optional[str]:
        """
        description: Help text describing what the Menu Item is used for
        type: string
        required: false
        """
        if help is None:
            help = ''
        self.cleaned_data['help'] = help
        return None

    def validate_action(self, action: Optional[str]) -> Optional[str]:
        """
        description: A url that a the Menu Item will redirect to
        type: string
        required: false
        """
        if action is None:
            action = ''
        action = str(action).strip()
        if len(action) > self.get_field('action').max_length:
            return 'app_manager_menu_item_update_107'
        self.cleaned_data['action'] = action
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Menu Item
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'app_manager_menu_item_update_108'
        if len(name) > self.get_field('name').max_length:
            return 'app_manager_menu_item_update_109'

        if 'predecessor_id' in self.errors:
            return None

        predecessor = self.cleaned_data.get('predecessor')
        if MenuItem.objects.filter(
            name=name,
            app_id=self.kwargs['app_id'],
            predecessor=predecessor,
        ).exclude(
            id=self._instance.pk,
        ).exists():
            return 'app_manager_menu_item_update_110'

        self.cleaned_data['name'] = name
        return None

    def validate_self_managed(self, self_managed: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if User's must be in self-managed members in order to view the Menu Item
        type: boolean
        required: false
        """
        if self_managed is None:
            self_managed = self._instance.self_managed
        if not isinstance(self_managed, bool):
            return 'app_manager_menu_item_update_111'
        self.cleaned_data['self_managed'] = self_managed
        return None
