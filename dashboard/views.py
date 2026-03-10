from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count


@login_required
def home(request):
    return render(request, 'home.html')

@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    pending_orders = Order.objects.filter(status='Pending').count()

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
    }
    return render(request, 'admin_dashboard.html', context)


@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-ordered_at')
    return render(request, 'manage_orders.html', {'orders': orders})


@staff_member_required
def update_status(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if request.method == "POST" and order:
        status = request.POST.get("status")
        order.status = status
        order.save()
    return redirect('manage_orders')