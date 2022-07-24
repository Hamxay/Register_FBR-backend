from django.urls import path

from .views import AddCnic, ChangePasswordView, CheckCNIC, GetAllFBR, GetByCninFBR, GetById, GetCurrentUserFIR, GetUserDetail ,RegisterUserByFrontend ,AddFBR, UpdateisSeen
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="FBR API",
        default_version='v1',
        description="Test description",
        license=openapi.License(name="Test License"),
    ),
    public=True,
)


urlpatterns = [
    path('docs', schema_view.with_ui('swagger',
                                     cache_timeout=0), name='schema-swagger-ui'),
    path("get_All",GetAllFBR.as_view()),
    path("ger_fir_by_cnic/<str:pk>",GetByCninFBR.as_view()),
    path("register",RegisterUserByFrontend.as_view()),
    path("addfir",AddFBR.as_view()),
    path("user_Read_me",GetUserDetail.as_view()),
    path("get_by_id/<str:pk>",GetById.as_view()),
    path("update_password",ChangePasswordView.as_view()),
    path("add_cnic",AddCnic.as_view()),
    path('login', obtain_auth_token, name="Get Token"),
    path("is_seen_update/<str:pk>",UpdateisSeen.as_view()),
    path("get_current_fir/<str:pk>",GetCurrentUserFIR.as_view()),
    path("get_cnic",CheckCNIC.as_view()),
]
