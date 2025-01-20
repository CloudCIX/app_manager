# stdlib
from typing import cast, List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from app_manager.models import (
    MemberLink,
    MenuItem,
    MenuItemUserLink,
)


__all__ = [
    'MenuItemUserLinkListController',
    'MenuItemUserLinkUpdateController',
]


class MenuItemUserLinkListController(ControllerBase):
    """
    Validates User data used to filter a list of Menu Item User Links records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'app_id',
            'id',
            'name',
        )
        search_fields = {
            'app_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'public': (),
            'self_managed': (),
        }


class MenuItemUserLinkUpdateController(ControllerBase):
    """
    Validates User data used to update Menu Item User Links records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = MenuItemUserLink
        validation_order = (
            'menu_item_ids',
        )

    def validate_menu_item_ids(self, menu_item_ids: Optional[List[int]]) -> Optional[str]:
        """
        description: A list of Menu Item ids that a User should have access to
        type: array
        items:
            type: integer
        """
        if not isinstance(menu_item_ids, list):
            return 'app_manager_menu_item_user_link_update_101'

        try:
            for index, menu_item in enumerate(menu_item_ids):
                menu_item_ids[index] = int(cast(int, menu_item))
        except (TypeError, ValueError):
            return 'app_manager_menu_item_user_link_update_102'

        linked_apps = MemberLink.objects.filter(
            member_id=self.request.user.member['id'],
        ).values_list(
            'app_id',
            flat=True,
        )
        menu_items = MenuItem.objects.filter(
            id__in=menu_item_ids,
            app_id__in=linked_apps,
        )
        if len(menu_item_ids) != menu_items.count():
            return 'app_manager_menu_item_user_link_update_103'
        self.cleaned_data['menu_item_ids'] = menu_item_ids
        return None
