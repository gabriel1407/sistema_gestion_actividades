from django.urls import re_path
from rest_framework.routers import DefaultRouter


from companies.views import LoginViewSet, CompanyViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'departament', DepartmentViewSet)

urlpatterns = [
    #re_path(r'^login/$', LoginViewSet, name='login'),
    re_path(r'^login/', LoginViewSet.as_view(), name='login'),
    #re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    # re_path(r'^user_offline/$', UserOfflineViewSet.as_view(), name='user_offline'),
    # re_path(r'^blocked_user/(?P<pk>[0-9]+)/$', Blocked_UserViewSet.as_view(), name='blocked_user'),
]

urlpatterns += router.urls