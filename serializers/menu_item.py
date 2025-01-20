# stdlib
from copy import copy
# libs
import serpy
# local
from .app import AppSerializer
from app_manager.models.menu_item import MenuItem


__all__ = [
    'MenuItemSerializer',
]


class MenuItemSerializer(serpy.Serializer):
    """
    action:
        description: A url that a the Menu Item will redirect to
        type: string
    administrator_only:
        description: A flag stating if only Admins have access to this Menu Item
        type: boolean
    app:
        $ref: '#/components/schemas/App'
    created:
        description: The date that the Menu Item was created
        type: string
    help:
        description: Help text describing what the Menu Item is used for
        type: string
    id:
        description: The id of the Menu Item
        type: int
    name:
        description: The name of the Menu Item
        type: string
    predecessor:
        description: A parent Menu Item that this Menu Item resides in, similar to a folder and sub-folder relation
        type: object
    predecessor_id:
        description: The id of the parent Menu Item
        type: int
    public:
        description: A flag stating if every User should have access to this Menu Item
        type: bool
    self_managed:
        description: A flag stating if User's must be in self-managed members in order to view the Menu Item
        type: bool
    sequence:
        description: The position of this Menu Item in relation to other Menu Items in the current level
        type: integer
    updated:
        description: The date that the Menu Item was last updated
        type: string
    uri:
        description: The absolute URL of the Menu Item that can be used to perform `Read` and `Update` operations on it
        type: string
    """
    action = serpy.Field()
    administrator_only = serpy.Field()
    app = AppSerializer()
    created = serpy.Field(attr='created.isoformat', call=True)
    help = serpy.Field()
    id = serpy.Field()
    name = serpy.Field()
    predecessor = serpy.MethodField()
    predecessor_id = serpy.Field()
    public = serpy.Field()
    self_managed = serpy.Field()
    sequence = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)

    def __init__(self, *args, **kwargs):
        super(MenuItemSerializer, self).__init__(*args, **kwargs)
        self.context = kwargs.get('context', dict())
        self.context.setdefault('initial', True)

    def get_predecessor(self, obj: MenuItem):
        """
        Serialize the first preceeding Menu Item
        :param obj: The Menu Item being serialized
        :return: The preceeding Menu Item
        """
        if self.context['initial'] and obj.predecessor is not None:  # pragma: no cover
            context = copy(self.context)
            context['initial'] = False
            return MenuItemSerializer(instance=obj.predecessor, context=context).data
        return None
