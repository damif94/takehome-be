from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import HomeList
# TODO: Create your routers and urls here
router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('home-listings/', HomeList.as_view())
]
