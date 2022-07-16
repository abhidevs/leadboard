from django.contrib import admin
from django.urls import include, path


from leads.views import landing_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('leads/', include('leads.urls', namespace="leads")),
]
