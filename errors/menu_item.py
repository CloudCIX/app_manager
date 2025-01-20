"""
Error Codes for all of the Methods in the Member Link Service
"""

# List
app_manager_menu_item_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
app_manager_menu_item_create_001 = (
    'The "app_id" path parameter is invalid. "app_id" must belong to a valid App record.'
)
app_manager_menu_item_create_101 = (
    'The "administrator_only" parameter is invalid. "administrator_only" must be a boolean'
)
app_manager_menu_item_create_102 = 'The "predecessor_id" parameter is invalid. "predecessor_id" must be an integer.'
app_manager_menu_item_create_103 = (
    'The "predecessor_id" parameter is invalid. "predecessor_id" must belong to a Menu Item.'
)
app_manager_menu_item_create_104 = 'The "sequence" is invalid. "sequence" is required and must be an integer.'
app_manager_menu_item_create_105 = (
    'The "sequence" parameter is invalid. This "sequence" number is already in use by another Menu Item with the given'
    ' "predecessor_id".'
)
app_manager_menu_item_create_106 = 'The "public" parameter is invalid. "public" must be a boolean.'
app_manager_menu_item_create_107 = 'The "action" parameter is invalid. "action" cannot be longer than 150 characters.'
app_manager_menu_item_create_108 = 'The "name" parameter is invalid. "name" is required and must be string.'
app_manager_menu_item_create_109 = 'The "name" parameter is invalid. "name" cannot be longer than 150 characters.'
app_manager_menu_item_create_110 = (
    'The "name" parameter is invalid. This "name" is already in use by another Menu Item with the given '
    '"predecessor_id".'
)
app_manager_menu_item_create_111 = 'The "self_managed" parameter is invalid. "self_managed" must be a boolean.'
app_manager_menu_item_create_201 = (
    'You do not have permission to make this request. Only the owners of this cloud can create Menu Items.'
)

# Read
app_manager_menu_item_read_001 = (
    'The "app_id" and/or "pk" path parameters are invalid. "app_id" must belong to a valid App record, and "pk" must '
    'belong to a valid Menu Item in that App.'
)
app_manager_menu_item_read_201 = (
    "You do not have permission to make this request. You're Member must have a Link set up for this Menu Item App."
)
app_manager_menu_item_read_202 = (
    'You do not have permission to make this request. You must have a User Link set up for this Menu Item.'
)

# Update
app_manager_menu_item_update_001 = (
    'The "app_id" and/or "pk" path parameters are invalid. "app_id" must belong to a valid App record, and "pk" must '
    'belong to a valid Menu Item in that App.'
)
app_manager_menu_item_update_101 = (
    'The "administrator_only" parameter is invalid. "administrator_only" must be a boolean'
)
app_manager_menu_item_update_102 = 'The "predecessor_id" parameter is invalid. "predecessor_id" must be an integer.'
app_manager_menu_item_update_103 = (
    'The "predecessor_id" parameter is invalid. "predecessor_id" must belong to a Menu Item.'
)
app_manager_menu_item_update_104 = 'The "sequence" is invalid. "sequence" is required and must be an integer.'
app_manager_menu_item_update_105 = (
    'The "sequence" parameter is invalid. This "sequence" number is already in use by another Menu Item with the given'
    ' "predecessor_id".'
)
app_manager_menu_item_update_106 = 'The "public" parameter is invalid. "public" must be a boolean.'
app_manager_menu_item_update_107 = 'The "action" parameter is invalid. "action" cannot be longer than 150 characters.'
app_manager_menu_item_update_108 = 'The "name" parameter is invalid. "name" is required and must be string.'
app_manager_menu_item_update_109 = 'The "name" parameter is invalid. "name" cannot be longer than 150 characters.'
app_manager_menu_item_update_110 = (
    'The "name" parameter is invalid. This "name" is already in use by another Menu Item with the given '
    '"predecessor_id".'
)
app_manager_menu_item_update_111 = 'The "self_managed" parameter is invalid. "self_managed" must be a boolean.'
app_manager_menu_item_update_201 = (
    'You do not have permission to make this request. Only the owners of this cloud can update Menu Items.'
)

# Delete
app_manager_menu_item_delete_001 = (
    'The "app_id" and/or "pk" path parameters are invalid. "app_id" must belong to a valid App record, and "pk" must '
    'belong to a valid Menu Item in that App.'
)
app_manager_menu_item_delete_201 = (
    'You do not have permission to make this request. Only the owners of this cloud can delete Menu Items.'
)
