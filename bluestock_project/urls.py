from django.contrib import admin
from django.urls import path
from dashboard.views import executive_overview, company_deep_dive

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', executive_overview, name='home'),
    path('deep-dive/', company_deep_dive, name='deep_dive'),
]