# Re-export everything so urls.py `from resume import views` still works unchanged.
from .auth import registration, login, logout
from .profile import viewprofile, updateprofile, updatepic
from .search import searchUsers
from .notifications import addnotification, getnotifications, deletenotification
from .download import download
