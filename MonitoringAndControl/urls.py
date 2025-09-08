from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('getData',views.getData,name='getData'),
    path('displayWest',views.displayWest,name='displayWest'),
    path('displayEast',views.displayEast,name='displayEast'),
    path('videoFeedWest/',views.videoFeedWest,name = 'videoFeedWest'),
    path('videoFeedEast/',views.videoFeedEast,name = 'videoFeedEast'),

    path('displayNorth',views.displayNorth,name='displayNorth'),
    path('displaySouth',views.displaySouth,name='displaySouth'),
    path('videoFeedNorth/',views.videoFeedNorth,name = 'videoFeedNorth'),
    path('videoFeedSouth/',views.videoFeedSouth,name = 'videoFeedSouth'),

    path('getDisplayData',views.getDisplayData,name='getDisplayData'),
]