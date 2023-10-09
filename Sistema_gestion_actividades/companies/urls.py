from django.urls import re_path
from rest_framework.routers import DefaultRouter


from companies.views import LoginViewSet, CompanyViewSet, DepartmentViewSet, UserViewSet, UserRolViewSet, ChangePasswordViewSet, LogoutView

router = DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'departament', DepartmentViewSet)
#router.register(r'users', UserViewSet)
router.register(r'rol', UserRolViewSet)

urlpatterns = [
    #re_path(r'^login/$', LoginViewSet, name='login'),
    re_path(r'^login/', LoginViewSet.as_view(), name='login'),
    re_path(r'^users/', UserViewSet.as_view(), name='users'),
    re_path(r'^change_password/', ChangePasswordViewSet.as_view(), name='change_password'),
    re_path(r'^logout/(?P<id>[0-9]+)/', LogoutView.as_view(), name='logout'),
    # re_path(r'^user_offline/$', UserOfflineViewSet.as_view(), name='user_offline'),
    # re_path(r'^blocked_user/(?P<pk>[0-9]+)/$', Blocked_UserViewSet.as_view(), name='blocked_user'),
]

urlpatterns += router.urls