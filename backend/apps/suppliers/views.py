from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Supplier
import json


@login_required
def supplier_list_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    suppliers = Supplier.objects.all()

    if query:
        suppliers = suppliers.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(supplier_id__icontains=query) |
            Q(contact_person__icontains=query)
        )

    if category:
        suppliers = suppliers.filter(category=category)

    if status:
        suppliers = suppliers.filter(status=status)

    paginator = Paginator(suppliers, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = [c[0] for c in Supplier.CATEGORY_CHOICES]
    statuses = [s[0] for s in Supplier.STATUS_CHOICES]

    total_count = Supplier.objects.count()
    active_count = Supplier.objects.filter(status='Active').count()
    under_review_count = Supplier.objects.filter(status='Under Review').count()
    from django.db.models import Avg
    avg_score_res = Supplier.objects.filter(status='Active').aggregate(Avg('overall_quality_score'))['overall_quality_score__avg'] or 0.0

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'selected_status': status,
        'categories': categories,
        'statuses': statuses,
        'total_count': total_count,
        'active_count': active_count,
        'under_review_count': under_review_count,
        'avg_score': round(float(avg_score_res), 2),
    }
    return render(request, 'suppliers/supplier_list.html', context)


@login_required
def supplier_detail_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    reviews = supplier.reviews.select_related('reviewer').order_by('-review_date')

    # Prepare historical trend data for Chart.js
    chronological_reviews = reviews.filter(status='Approved').order_by('review_date')
    dates = [r.review_date.strftime('%b %d, %Y') for r in chronological_reviews]
    scores = [float(r.overall_score) for r in chronological_reviews]

    context = {
        'supplier': supplier,
        'reviews': reviews,
        'trend_dates_json': json.dumps(dates),
        'trend_scores_json': json.dumps(scores),
        'approved_count': reviews.filter(status='Approved').count(),
        'pending_count': reviews.filter(status__in=['Draft', 'Pending Review', 'Under Review']).count(),
    }
    return render(request, 'suppliers/supplier_detail.html', context)


@login_required
def supplier_create_view(request):
    # Enforce RBAC
    user_role = getattr(request.user.profile, 'role', 'REVIEWER') if hasattr(request.user, 'profile') else 'REVIEWER'
    if not (request.user.is_superuser or user_role in ['ADMIN', 'QUALITY_MANAGER']):
        messages.error(request, "Permission denied. Only Quality Managers or Admins can onboard new suppliers.")
        return redirect('supplier-list')

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id', '').strip()
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip().upper()
        contact_person = request.POST.get('contact_person', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        category = request.POST.get('category', '').strip()
        status = request.POST.get('status', Supplier.STATUS_ACTIVE).strip()

        # Validation
        if not (supplier_id and name and code and email and contact_person):
            messages.error(request, "All marked fields are required.")
            return render(request, 'suppliers/supplier_form.html', {'categories': Supplier.CATEGORY_CHOICES, 'statuses': Supplier.STATUS_CHOICES})

        if Supplier.objects.filter(supplier_id=supplier_id).exists():
            messages.error(request, f"Supplier ID '{supplier_id}' already exists.")
            return render(request, 'suppliers/supplier_form.html', {'categories': Supplier.CATEGORY_CHOICES, 'statuses': Supplier.STATUS_CHOICES})

        if Supplier.objects.filter(code=code).exists():
            messages.error(request, f"Supplier Code '{code}' already exists.")
            return render(request, 'suppliers/supplier_form.html', {'categories': Supplier.CATEGORY_CHOICES, 'statuses': Supplier.STATUS_CHOICES})

        supplier = Supplier.objects.create(
            supplier_id=supplier_id,
            name=name,
            code=code,
            contact_person=contact_person,
            email=email,
            phone=phone,
            address=address,
            category=category,
            status=status
        )
        messages.success(request, f"Supplier '{supplier.name}' created successfully!")
        return redirect('supplier-detail', pk=supplier.pk)

    context = {
        'categories': Supplier.CATEGORY_CHOICES,
        'statuses': Supplier.STATUS_CHOICES,
        'is_edit': False,
    }
    return render(request, 'suppliers/supplier_form.html', context)


@login_required
def supplier_update_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    # Enforce RBAC
    user_role = getattr(request.user.profile, 'role', 'REVIEWER') if hasattr(request.user, 'profile') else 'REVIEWER'
    if not (request.user.is_superuser or user_role in ['ADMIN', 'QUALITY_MANAGER']):
        messages.error(request, "Permission denied. Only Quality Managers or Admins can edit supplier information.")
        return redirect('supplier-detail', pk=supplier.pk)

    if request.method == 'POST':
        supplier.name = request.POST.get('name', '').strip()
        supplier.contact_person = request.POST.get('contact_person', '').strip()
        supplier.email = request.POST.get('email', '').strip()
        supplier.phone = request.POST.get('phone', '').strip()
        supplier.address = request.POST.get('address', '').strip()
        supplier.category = request.POST.get('category', '').strip()
        supplier.status = request.POST.get('status', '').strip()

        supplier.save()
        messages.success(request, f"Supplier '{supplier.name}' updated successfully.")
        return redirect('supplier-detail', pk=supplier.pk)

    context = {
        'supplier': supplier,
        'categories': Supplier.CATEGORY_CHOICES,
        'statuses': Supplier.STATUS_CHOICES,
        'is_edit': True,
    }
    return render(request, 'suppliers/supplier_form.html', context)


@login_required
def supplier_delete_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    user_role = getattr(request.user.profile, 'role', 'REVIEWER') if hasattr(request.user, 'profile') else 'REVIEWER'
    if not (request.user.is_superuser or user_role == 'ADMIN'):
        messages.error(request, "Access denied. Only Administrators can delete suppliers.")
        return redirect('supplier-detail', pk=supplier.pk)

    if request.method == 'POST':
        name = supplier.name
        supplier.delete()
        messages.success(request, f"Supplier '{name}' was deleted.")
        return redirect('supplier-list')

    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})
