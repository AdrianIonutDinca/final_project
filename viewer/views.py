from django.shortcuts import render
from django.views import View

from viewer.models import Produs, Magazin
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Produs, Magazin
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime




def lista_produse(request):
    produse = Produs.objects.all()  # Preia toate produsele
    return render(request, 'produse.html', {'produse': produse})



def lista_magazine(request):
    magazine = Magazin.objects.all()  # Preia toate magazinele
    return render(request, 'magazine.html', {'magazine': magazine})

def get_data(request):
    stores = list(Magazin.objects.values('id', 'magazin'))
    products = list(Produs.objects.values('id', 'denumire'))
    return JsonResponse({'stores': stores, 'products': products})

@csrf_exempt
def submit_selection(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['selected_products'] = data.get('products', [])
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid request'}, status=400)

def selected_products(request):
    selected_ids = request.session.get('selected_products', [])
    products = Produs.objects.filter(id__in=selected_ids)

    context = {
        'products': products,
        'username': request.user.username,  # Numele utilizatorului autentificat
        'current_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Data și ora curentă
    }

    return render(request, 'selected_products.html', context)


    # return render(request, 'selected_products.html', {'products': products})

class SelectProductsView(View):
    def get(self, request):
        products = Produs.objects.all()
        stores = Magazin.objects.all()
        return render(request, 'select_products.html', {'products': products, 'stores': stores})

    def post(self, request):
        def post(self, request):
            # Obține ID-urile produselor și magazinelor selectate
            selected_product_ids = request.POST.getlist('products')
            selected_store_ids = request.POST.getlist('stores')

            # Filtrează produsele și magazinele selectate
            selected_products = Produs.objects.filter(id__in=selected_product_ids)
            selected_stores = Magazin.objects.filter(id__in=selected_store_ids)

            # Trimite datele către șablon
            return render(request, 'selected_products.html', {
                'products': selected_products,
                'stores': selected_stores
            })


class SelectedProductsView(View):
    # def get(self, request):
    #     # Obține toate produsele și magazinele
    #     products = Produs.objects.all()
    #     stores = Magazin.objects.all()
    #
    #     # Transmite datele către șablon
    #     return render(request, 'select_products.html', {'products': products, 'stores': stores})

    def post(self, request):
        # Obține ID-urile produselor și magazinelor selectate
        selected_products_ids = request.POST.getlist('products')
        selected_stores_ids = request.POST.getlist('stores')

        # Filtrează produsele și magazinele selectate
        selected_products = Produs.objects.filter(id__in=selected_products_ids)
        selected_stores = Magazin.objects.filter(id__in=selected_stores_ids)

        # Creează combinațiile dintre produsele selectate și toate magazinele
        product_store_combinations = [
            f"{product.denumire} - {store.magazin}"
            for product in selected_products
            for store in selected_stores]

        # Trimite datele către șablon
        return render(request, 'selected_products.html', {
            'products': selected_products,
            'stores': selected_stores,
            'combinations': product_store_combinations,
        })




def is_client(user):
    return user.groups.filter(name='Client').exists()

@login_required
@user_passes_test(is_client)
def select_products(request):
    # Logica pentru pagina select-products
    return render(request, 'SelectProductsView.as_view()/select_products.html')
    # return render(request, 'viewer/select_products.html')

@login_required
@user_passes_test(is_client)
def selected_products(request):
    # Logica pentru pagina selected-products
    return render(request, 'SelectedProductsView.as_view()/selected_products.html')
    # return render(request, 'viewer/selected_products.html')


