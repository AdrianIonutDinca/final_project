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
from .models import Cerere, Preturi
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import sqlite3
from viewer.models import SelectedData
from viewer.models import SavedPrices
from django.contrib.auth import logout
from django.template.loader import render_to_string
from django.contrib.auth import logout
from django.db.models import Q
from django.utils.timezone import localtime





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
    }

    return render(request, 'selected_products.html', context)



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

# @login_required
# @user_passes_test(is_client)
# def select_products(request):
#     # Logica pentru pagina select-products
#     return render(request, 'SelectProductsView.as_view()/select_products.html')
#     # return render(request, 'viewer/select_products.html')

@login_required
@user_passes_test(is_client)
def select_products(request):
    products = Produs.objects.all()  # Obține toate produsele
    stores = Magazin.objects.all()  # Obține toate magazinele
    return render(request, 'select_products.html', {'products': products, 'stores': stores})



@login_required
@user_passes_test(is_client)
def selected_products(request):
    # Logica pentru pagina selected-products
    return render(request, 'selected_products.html')
    # return render(request, 'viewer/selected_products.html')


@login_required
@login_required
def operator_view(request):
    # Obține județul utilizatorului din profil
    user_judet = request.user.profile.judet
    magazine = Magazin.objects.filter(judet=user_judet) if user_judet else Magazin.objects.none()

    # Obține doar intrările din SelectedData fără preț
    data = SelectedData.objects.filter(store__in=magazine, price__isnull=True)

    if request.method == 'POST':
        # Salvează prețurile introduse de operator
        for entry in data:
            price_key = f'price_{entry.id}'
            price_value = request.POST.get(price_key)

            if price_value:  # Dacă un preț este introdus
                entry.price = price_value  # Actualizează câmpul preț
                entry.save()  # Salvează modificările în baza de date

        return render(request, 'success.html', {"message": "Prețurile au fost salvate!"})

    # Transmite doar intrările fără preț către șablon
    return render(request, 'operator_view.html', {
        'data': data,
        'user_judet': user_judet  # Transmitem județul pentru context
    })

@login_required
def operator_view(request):
    # Obține județul utilizatorului din profil
    user_judet = request.user.profile.judet
    magazine = Magazin.objects.filter(judet=user_judet) if user_judet else Magazin.objects.none()

    # Obține datele din SelectedData pentru produsele din magazinele din județul utilizatorului
    # data = SelectedData.objects.filter(store__in=magazine)
    data = SelectedData.objects.filter(store__in=magazine, price__isnull=True)


    if request.method == 'POST':
        # Salvează prețurile introduse de operator
        for entry in data:
            price_key = f'price_{entry.id}'
            price_value = request.POST.get(price_key)

            if price_value:  # Doar dacă un preț a fost introdus
                # Actualizează direct în SelectedData
                entry.price = price_value
                entry.save()




            # if price_value:  # Doar dacă un preț a fost introdus
            #     # Salvăm în tabela SavedPrices
            #     SavedPrices.objects.create(
            #         product=entry.product,
            #         store=entry.store,
            #         price=price_value,
            #         operator=request.user  # Utilizatorul care a salvat prețul
            #     )

        return render(request, 'success.html', {"message": "Prețurile au fost salvate!"})

    # Transmite datele către șablon
    return render(request, 'operator_view.html', {
        'data': data,
        'user_judet': user_judet  # Transmitem județul pentru context
    })


@login_required
def redirect_after_login(request):
    if request.user.groups.filter(name='Client').exists():
        return redirect('select_products')  # Redirecționează la select_products
    # elif request.user.groups.filter(name='Operator').exists():
    #     return redirect('operator-view')  # Redirecționează la operator_view
    else:
        # return redirect('home')  # Redirecționează la pagina principală implicită
        return redirect('operator-view')  # Redirecționează la operator_view


@csrf_exempt
def save_selected(request):
    if request.method == 'POST':
        # Preluăm combinațiile selectate
        selected_combinations = request.POST.getlist('selected_combinations')

        # Ștergem datele anterioare (opțional)
        # SelectedData.objects.all().delete()

        # Salvăm combinațiile selectate
        for combination in selected_combinations:
            product_id, store_id = combination.split("-")
            product = Produs.objects.get(id=product_id)
            store = Magazin.objects.get(id=store_id)
            user = request.user
            # SelectedData.objects.create(product=product, store=store, user=user)
            SelectedData.objects.create(
                product=product,
                store=store,
                user=request.user,  # Salvează utilizatorul conectat
                price = None  # Inițial NULL
            )
            html_content = render_to_string('save_success.html')
            return HttpResponse(html_content)

        return HttpResponse('Invalid request method.', status=400)

        # return HttpResponse('Selected products and stores saved successfully!')

    # return HttpResponse('Invalid request method.', status=400)

def view_selected(request):
    data = SelectedData.objects.all()
    return render(request, 'view_selected.html', {'data': data})

def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def view_results(request):
    user = request.user
    products = Produs.objects.all()
    stores = Magazin.objects.all()

    selected_products = request.GET.getlist('products')
    selected_stores = request.GET.getlist('stores')

    # Filtrăm datele pentru utilizator
    data = SelectedData.objects.filter(user=user)

    if selected_products:
        data = data.filter(product__id__in=selected_products)
    if selected_stores:
        data = data.filter(store__id__in=selected_stores)

    # Construim chart_data pentru template
    chart_data = {}
    for entry in data:
        product_name = entry.product.denumire
        store_name = entry.store.magazin
        if product_name not in chart_data:
            chart_data[product_name] = {}
        if store_name not in chart_data[product_name]:
            chart_data[product_name][store_name] = []

        chart_data[product_name][store_name].append({
            'date': entry.created_at.strftime('%Y-%m-%d'),
            'price': float(entry.price) if entry.price else None,
        })

    # Debugging: printăm datele în consolă
    print(json.dumps(chart_data, indent=4))

    context = {
        'products': products,
        'stores': stores,
        'chart_data': chart_data,  # Datele pentru template
    }
    return render(request, 'view_results.html', context)