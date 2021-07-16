from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoreAPIView.as_view()),
    path('list', views.StoreListAPIView.as_view()),
    path('list/category/<int:category>/', views.StoresCategoryAPIView.as_view()),
    path('owner/', views.HasStoreListAPIView.as_view()),
    path('list1', views.StoreList1APIView.as_view()),
    path('<int:owner>/', views.StoreDetailAPIView.as_view()),
    path('id/<int:id>/', views.StoreDetailIdAPIView.as_view()),
]