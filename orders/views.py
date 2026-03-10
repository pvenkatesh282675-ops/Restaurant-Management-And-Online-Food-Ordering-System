from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from cart.models import Cart
from orders.models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return redirect("view_cart")

    total = sum(item.subtotal() for item in cart.items.all())

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity,
            price=item.food.price
        )

    cart.items.all().delete()
    return redirect("my_orders")


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by("-ordered_at")

    return render(request, "orders.html", {"orders": orders})


@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status="Delivered").count()
    pending_orders = Order.objects.filter(status="Pending").count()

    total_revenue = Order.objects.filter(
        status="Delivered"
    ).aggregate(
        Sum("total_price")
    )["total_price__sum"] or 0

    return render(request, "admin_dashboard.html", {
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "pending_orders": pending_orders,
        "total_revenue": total_revenue
    })


@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by("-ordered_at")
    return render(request, "manage_orders.html", {"orders": orders})


@staff_member_required
def update_status(request, order_id):
    if request.method == "POST":
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.status = request.POST.get("status")
            order.save()

    return redirect("manage_orders")