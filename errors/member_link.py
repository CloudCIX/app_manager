"""
Error Codes for all of the Methods in the Member Link Service
"""

# Create
app_manager_member_link_create_001 = (
    'The "app_id" path parameter is invalid. "app_id" must belong to a valid App record.'
)
app_manager_member_link_create_101 = (
    'The "member_id" parameter is invalid. "member_id" is required and must be an integer.'
)
app_manager_member_link_create_102 = (
    'The "member_id" parameter is invalid. You cannot create Member Links to an App for other Members.'
)
app_manager_member_link_create_103 = (
    'The "member_id" parameter is invalid. You must be linked to the Member that you are setting up a Member Link for.'
)
app_manager_member_link_create_201 = (
    'You do not have permission to make this request. You must be an administrator to create a Member Link.'
)
app_manager_member_link_create_202 = 'You do not have permission to make this request. This App is private.'
app_manager_member_link_create_203 = (
    'You do not have permission to make this request. A Link already exists between the given App and Member.'
)

# Delete
app_manager_member_link_delete_001 = (
    'The "app_id" path parameter is invalid. There is no Link between your Member and the App specified by "app_id".'
)
app_manager_member_link_delete_201 = (
    'You do not have permission to make this request. You must be an administrator to delete a Member Link.'
)
app_manager_member_link_delete_202 = 'You do not have permission to make this request. This App is private.'
