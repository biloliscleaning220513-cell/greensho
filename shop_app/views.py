from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Order, Profil
from .forms import ProductForm, OrderForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'detail.html', {'product': product})

@login_required # Faqat login qilganlar mahsulot qo'shadi
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')
    return render(request, 'product_form.html', {'form': ProductForm()})

@login_required # Faqat login qilganlar buyurtma beradi
def place_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.customer = request.user
            order.save()
            return redirect('order_list')
    return render(request, 'place_order.html', {'form': OrderForm(), 'product': product})

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def confirm_delivery(request, pk):
    # Buyurtmani topamiz, agar u foydalanuvchiniki bo'lmasa 404 beradi
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    
    if request.method == 'POST':
        order.status = 'Yetkazildi'
        order.save()
        return redirect('order_list')
    
    return redirect('order_list')
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user) # Faqat egasi tahrirlay oladi
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'title': "Mahsulotni tahrirlash"})
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Ro'yxatdan o'tgach avtomatik login qilish
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
from .models import Category
from django import forms

# Kategoriya uchun oddiy forma
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_create') # Kategoriya qo'shilgach, yana mahsulot qo'shishga qaytadi
    else:
        form = CategoryForm()
    return render(request, 'product_form.html', {'form': form, 'title': "Yangi kategoriya qo'shish"})
@login_required
def profile_view(request):
    # Foydalanuvchining o'zi yuklagan mahsulotlari
    my_products = Product.objects.filter(seller=request.user).order_by('-created_at')
    # Foydalanuvchi bergan buyurtmalari
    my_orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'my_products': my_products,
        'my_orders': my_orders,
    }
    return render(request, 'profile.html', context)
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('profile') # O'chirilgach profilga qaytadi
    return render(request, 'product_confirm_delete.html', {'product': product})






@login_required
def profile_update(request):
    profile, created = Profil.objects.get_or_create(user=request.user)

    if request.method == 'POST':

        # 🔹 USER UPDATE
        if 'update_user' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(instance=profile)
            pass_form = PasswordChangeForm(request.user)

            if u_form.is_valid():
                u_form.save()
                return redirect('profile')

        # 🔹 AVATAR UPDATE
        elif 'update_avatar' in request.POST:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            pass_form = PasswordChangeForm(request.user)

            if p_form.is_valid():
                p_form.save()
                return redirect('profile')

        # 🔹 PASSWORD UPDATE
        elif 'update_password' in request.POST:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=profile)
            pass_form = PasswordChangeForm(request.user, request.POST)

            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        pass_form = PasswordChangeForm(request.user)

    return render(request, 'profile_update.html', {
        'u_form': u_form,
        'p_form': p_form,
        'pass_form': pass_form
    })
