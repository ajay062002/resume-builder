# This file is kept for backwards compatibility.
# All API view logic has been moved to resume/api/ package.
from resume.api import (  # noqa: F401
    api_csrf, api_login, api_logout, api_register,
    api_profile, api_update_profile, api_upload_pic, api_download_pdf,
    api_search,
    api_notifications, api_add_notification, api_delete_notification,
)
