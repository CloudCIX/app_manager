# libs
import serpy


__all__ = [
    'AppSerializer',
]


class AppSerializer(serpy.Serializer):
    """
    action:
        description: What the App does when used in a UI
        type: string
    created:
        description: The date that the record was created
        type: string
    description:
        description: A short explanation of the App
        type: string
    extra:
        description: Any other miscellaneous about the App
        type: json
    icon_url:
        description: The url where the icon for the app can be found
        type: string
    id:
        description: The unique id of the App record
        type: integer
    in_app_store:
        description: A flag stating if this App can be installed through the CloudCIX app store
        type: boolean
    maintenance:
        description: A flag stating if this App is unavailable due to maintenance
        type: boolean
    name:
        description: The name of the App
        type: string
    online:
        description: A flag stating if this App is accessible
        type: boolean
    private:
        description: A flag stating if this App is private and only available to select Members
        type: boolean
    updated:
        description: The date that the record was last updated
        type: string
    uri:
        description: The absolute URL of the App that can be used to perform `Read` and `Update` operations on it
        type: string
    """
    action = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    description = serpy.Field()
    extra = serpy.Field()
    icon_url = serpy.Field()
    id = serpy.Field()
    in_app_store = serpy.BoolField()
    maintenance = serpy.BoolField()
    name = serpy.Field()
    online = serpy.Field()
    private = serpy.BoolField()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_icon_url = serpy.Field(attr='icon_url', label='iconURL')
    old_in_app_store = serpy.Field(attr='in_app_store', label='inAppStore')
