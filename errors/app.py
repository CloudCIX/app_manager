"""
Error Codes for all of the Methods in the App Service
"""

# List
app_manager_app_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
app_manager_app_create_101 = 'The "action" parameter is invalid. "action" cannot be longer than 8000 characters.'
app_manager_app_create_102 = 'The "icon_url" parameter is invalid. "icon_url" is required and must be a string.'
app_manager_app_create_103 = 'The "icon_url" parameter is invalid. "icon_url" cannot be longer than 8000 characters.'
app_manager_app_create_104 = 'The "name" parameter is invalid. "name" is required and must be a string.'
app_manager_app_create_105 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
app_manager_app_create_106 = 'The "name" parameter is invalid. An App already exists with this name.'
app_manager_app_create_107 = 'The "online" parameter is invalid. "online" must be a boolean.'
app_manager_app_create_108 = 'The "in_app_store" parameter is invalid. "in_app_store" must be a boolean.'
app_manager_app_create_109 = 'The "private" parameter is invalid. "private" must be a boolean.'
app_manager_app_create_110 = 'The "maintenance" parameter is invalid. "maintenance" must be a boolean.'
app_manager_app_create_111 = 'The "extra" parameter is invalid. "extra" must be a dictionary.'
app_manager_app_create_201 = (
    'You do not have permission to make this request. Only the owners of this cloud can create Apps.'
)

# Read
app_manager_app_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid App record.'
app_manager_app_read_201 = (
    'You do not have permission to make this request. Your Member must have a Member Link set up for this App.'
)

# Update
app_manager_app_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid App record.'
app_manager_app_update_101 = 'The "action" parameter is invalid. "action" cannot be longer than 8000 characters.'
app_manager_app_update_102 = 'The "icon_url" parameter is invalid. "icon_url" is required and must be a string.'
app_manager_app_update_103 = 'The "icon_url" parameter is invalid. "icon_url" cannot be longer than 8000 characters.'
app_manager_app_update_104 = 'The "name" parameter is invalid. "name" is required and must be a string.'
app_manager_app_update_105 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
app_manager_app_update_106 = 'The "name" parameter is invalid. An App already exists with this name.'
app_manager_app_update_107 = 'The "online" parameter is invalid. "online" must be a boolean.'
app_manager_app_update_108 = 'The "in_app_store" parameter is invalid. "in_app_store" must be a boolean.'
app_manager_app_update_109 = 'The "private" parameter is invalid. "private" must be a boolean.'
app_manager_app_update_110 = 'The "maintenance" parameter is invalid. "maintenance" must be a boolean.'
app_manager_app_update_111 = 'The "extra" parameter is invalid. "extra" must be a dictionary.'
app_manager_app_update_201 = (
    'You do not have permission to make this request. Only the owners of this cloud can update Apps.'
)

# Delete
app_manager_app_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid App record.'
app_manager_app_delete_201 = (
    'You do not have permission to make this request. Only the owners of this cloud can delete Apps.'
)
