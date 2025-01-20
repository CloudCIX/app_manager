"""
Dummy serializer for Member Link
"""

# libs
import serpy
# local
from .app import AppSerializer


__all__ = [
    'MemberLinkSerializer',
]


class MemberLinkSerializer(serpy.Serializer):
    """
    app:
        $ref: '#/components/schemas/App'
    member_id:
        description: The id of the Member that owns the Link
        type: integer
    """
    app = AppSerializer()
    member_id = serpy.Field()
