from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('list', views.index, name='index'),
    path('<int:epid>/downXlsx', views.downXlsx, name="downXlsx"),
    path('<str:epid>/<str:test>/test', views.test, name="test"),
    path('xlsxbymonth', views.xlsxbymonth, name="xlsxbymonth"),
    path('xlsxbydate', views.xlsxbydate, name="xlsxbydate"),
]