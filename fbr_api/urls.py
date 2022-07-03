from django.urls import path

from .views import GetAllFBR, GetByCninFBR, GetById, GetUserDetail ,RegisterUserByFrontend ,AddFBR
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
    path('', schema_view.with_ui('swagger',
                                     cache_timeout=0), name='schema-swagger-ui'),
    path("get_All",GetAllFBR.as_view()),
    path("cnic/<str:pk>",GetByCninFBR.as_view()),
    path("register",RegisterUserByFrontend.as_view()),
    path("addfbr",AddFBR.as_view()),
    path("user_Read_me",GetUserDetail.as_view()),
    path("get_by_id/<str:pk>",GetById.as_view()),
]
