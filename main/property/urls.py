from django.urls import path

from property.domain.views import ProductSearchView

urlpatterns = [
    path('search/', ProductSearchView.as_view(), name='product-search'),

]
