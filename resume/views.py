# This file is kept for backwards compatibility.
# All view logic has been moved to resume/views/ package.
from resume.views import (  # noqa: F401
    registration, login, logout,
    viewprofile, updateprofile, updatepic,
    searchUsers,
    addnotification, getnotifications, deletenotification,
    download,
)
