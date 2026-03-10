from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from menu.models import FoodItem


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item = CartItem.objects.filter(cart=cart, food=food).first()
    if item:
        item.quantity += 1
        item.save()
    else:
        CartItem.objects.create(cart=cart, food=food, quantity=1)

    return redirect("view_cart")


@login_required
def decrease_quantity(request, item_id):
    item = CartItem.objects.filter(
        id=item_id,
        cart__user=request.user
    ).first()

    if item:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect("view_cart")


@login_required
def remove_item(request, item_id):
    CartItem.objects.filter(
        id=item_id,
        cart__user=request.user
    ).delete()

    return redirect("view_cart")


@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    total = sum(item.subtotal() for item in cart.items.all()) if cart else 0

    return render(request, "cart.html", {
        "cart": cart,
        "total": total
    })