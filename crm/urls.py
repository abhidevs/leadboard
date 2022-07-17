from django.contrib import admin
from django.urls import include, path


from leads.views import LandingPageView, landing_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('leads/', include('leads.urls', namespace="leads")),
]
