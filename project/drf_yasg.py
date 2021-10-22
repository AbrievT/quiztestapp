from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_swagger.views import get_swagger_view # new

API_TITLE = 'Quiz app Project Docs"'
API_DESCRIPTION = 'Quiz app Project Docs'
yasg_schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jurabekabriev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

schema_view = get_swagger_view(title=API_TITLE) # new


