"""
Error Codes for all of the Methods in the Menu Item User Link Service
"""

# List
app_manager_menu_item_user_link_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)
app_manager_menu_item_user_link_list_201 = (
    'You do not have permission to make this request. There is no User in Membership with the given "user_id".'
)
app_manager_menu_item_user_link_list_202 = (
    'You do not have permission to make this request. You can only read the User Links of a User in a your Member.'
)

# Update
app_manager_menu_item_user_link_update_101 = (
    'The "menu_item_ids" parameter is invalid. "menu_item_ids" is required and must be a list of integers.'
)
app_manager_menu_item_user_link_update_102 = (
    'The "menu_item_ids" parameter is invalid. Not every item in "menu_item_ids" was an integer.'
)
app_manager_menu_item_user_link_update_103 = (
    'The "menu_item_ids" parameter is invalid. Not all of the given ids belong to valid Menu Items, or they belong to '
    'Apps that your Member is not using.'
)
app_manager_menu_item_user_link_update_201 = (
    'You do not have permission to make this request. You must be an admin to update Menu Item User Links.'
)
app_manager_menu_item_user_link_update_202 = (
    'You do not have permission to make this request. You must be in a self-managed Member to update Menu Item User '
    'Links.'
)
app_manager_menu_item_user_link_update_203 = (
    'You do not have permission to make this request. You cannot read the User record for the given "user_id" if it '
    'exists'
)
