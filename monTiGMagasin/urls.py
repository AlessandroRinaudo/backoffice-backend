from django.urls import path
from monTiGMagasin import views

urlpatterns = [
    path('infoproducts/', views.InfoProductList.as_view()),
    path('infoproduct/<int:tig_id>/', views.InfoProductDetail.as_view()),
    path('incrementStock/<int:tig_id>/<int:number>/', views.ProductIncrementStock.as_view()),
    path('decrementStock/<int:tig_id>/<int:number>/', views.ProductDecrementStock.as_view())
]
