"""
URL configuration for Colectare_date project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from viewer import views
from viewer.views import SelectProductsView, SelectedProductsView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('produse/', views.lista_produse, name='lista_produse'),
    path('magazine/', views.lista_magazine, name='lista_magazine'),
    path('select-products/', SelectProductsView.as_view(), name='select_products'),
    path('selected-products/', SelectedProductsView.as_view(), name='selected_products'),
]
