from django.urls import path, include

from .views import LoginView
from .views import LogoutView
from .views import CaptchaView
from .views import UserView
from .views import UserListView
from .views import ChangePasswordView
from .views import GroupView
from .views import GroupListView
from .views import RoleView
from .views import RoleListView
from .views import PermissionView
from .views import PermissionListView
from .views import MenuView
from .views import MenuListView
from .views import NotPermissionView

app_name = 'rms_auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('captcha/', CaptchaView.as_view(), name='captcha'),
    path('user/', UserView.as_view(), name='auth'),
    path('userlist/', UserListView.as_view(), name='authlist'),
    path('chpwd/', ChangePasswordView.as_view(), name='chpwd'),
    path('usergroup/', GroupView.as_view(), name='usergroup'),
    path('usergrouplist/', GroupListView.as_view(), name='usergrouplist'),
    path('role/', RoleView.as_view(), name='role'),
    path('rolelist/', RoleListView.as_view(), name='rolelist'),
    path('permission/', PermissionView.as_view(), name='permission'),
    path('notpermission/', NotPermissionView.as_view(), name='notpermission'),
    path('permissionlist/', PermissionListView.as_view(), name='permissionlist'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('menulist/', MenuListView.as_view(), name='menulist'),
]
