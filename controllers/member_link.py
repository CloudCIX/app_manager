# stdlib
from typing import cast, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
from cloudcix.api.membership import Membership
# local
from app_manager.models.member_link import MemberLink


__all__ = [
    'MemberLinkCreateController',
]


class MemberLinkCreateController(ControllerBase):
    """
    Validates User data used to create a new Member Link record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = MemberLink
        validation_order = (
            'member_id',
        )

    def validate_member_id(self, member_id: Optional[int]) -> Optional[str]:
        """
        description: The id of a Member that wants to use an App
        type: integer
        """
        try:
            member_id = int(cast(int, member_id))
        except (TypeError, ValueError):
            return 'app_manager_member_link_create_101'

        if member_id != self.request.user.member['id']:
            if self.request.user.id != 1:
                return 'app_manager_member_link_create_102'
            response = Membership.member.read(
                token=self.request.user.token,
                pk=member_id,
            )
            if response.status_code != 200:
                return 'app_manager_member_link_create_103'

        self.cleaned_data['member_id'] = member_id
        return None
