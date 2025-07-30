from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import Book, Order, OrderItem
from django.contrib import messages # type: ignore
from django.contrib.auth import login, authenticate, logout # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from django.urls import reverse # type: ignore

def index(request):
    books = Book.objects.all()
    return render(request, "index.html", {'books': books})

def loginUser(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Invalid credentials")
    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        cp = request.POST.get('confirmpassword')
        if p != cp:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')
        user = User.objects.create_user(username=u, email=e, password=p)
        login(request, user)
        return redirect('home')
    return render(request, "signup.html")

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        return render(request, "login_required.html", {'message': "Login required"})
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', {})
    cart[str(book_id)] = cart.get(str(book_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items, total_price = [], 0
    for bid, qty in cart.items():
        book = get_object_or_404(Book, id=bid)
        total = book.price * qty
        cart_items.append({'book': book, 'quantity': qty, 'total': total})
        total_price += total
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def product_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'product_details.html', {'book': book})

@login_required
def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})
    book_id_str = str(book_id)
    if book_id_str in cart:
        del cart[book_id_str]
        request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def place_order(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        if not (full_name and address and phone):
            return render(request, 'order_form.html', {'book': book, 'error': 'All fields are required'})

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            status='Placed',
        )

        OrderItem.objects.create(
            order=order,
            book=book,
            quantity=1,
            price=book.price
        )

        return render(request, 'success.html', {'order': order})

    return render(request, 'order_form.html', {'book': book})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.status = 'Cancelled'
        order.save()
    return redirect('my_orders')

def login_required_prompt(request):
    return render(request, "login_required.html")
