from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal
import datetime

from .models import QualityReview, ReviewAuditLog
from apps.suppliers.models import Supplier


@login_required
def review_list_view(request):
    tab = request.GET.get('tab', 'all')
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    reviews = QualityReview.objects.select_related('supplier', 'reviewer').all()

    if tab == 'pending':
        reviews = reviews.filter(status__in=[QualityReview.STATUS_PENDING_REVIEW, QualityReview.STATUS_UNDER_REVIEW])
    elif tab == 'my':
        reviews = reviews.filter(reviewer=request.user)
    elif tab == 'approved':
        reviews = reviews.filter(status=QualityReview.STATUS_APPROVED)
    elif tab == 'rejected':
        reviews = reviews.filter(status=QualityReview.STATUS_REJECTED)

    if query:
        reviews = reviews.filter(
            Q(review_id__icontains=query) |
            Q(supplier__name__icontains=query) |
            Q(reviewer__username__icontains=query)
        )

    if status_filter and tab == 'all':
        reviews = reviews.filter(status=status_filter)

    paginator = Paginator(reviews, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    counts = {
        'all': QualityReview.objects.count(),
        'pending': QualityReview.objects.filter(status__in=[QualityReview.STATUS_PENDING_REVIEW, QualityReview.STATUS_UNDER_REVIEW]).count(),
        'my': QualityReview.objects.filter(reviewer=request.user).count(),
        'approved': QualityReview.objects.filter(status=QualityReview.STATUS_APPROVED).count(),
        'rejected': QualityReview.objects.filter(status=QualityReview.STATUS_REJECTED).count(),
    }

    context = {
        'page_obj': page_obj,
        'current_tab': tab,
        'query': query,
        'counts': counts,
        'statuses': [s[0] for s in QualityReview.STATUS_CHOICES],
        'selected_status': status_filter,
    }
    return render(request, 'reviews/review_list.html', context)


@login_required
def review_detail_view(request, pk):
    review = get_object_or_404(
        QualityReview.objects.select_related('supplier', 'reviewer', 'reviewed_by_manager'),
        pk=pk
    )
    audit_logs = review.audit_logs.select_related('actor').order_by('-timestamp')

    user_role = getattr(request.user.profile, 'role', 'REVIEWER') if hasattr(request.user, 'profile') else 'REVIEWER'
    if request.user.is_superuser:
        user_role = 'ADMIN'

    can_submit = (review.status == QualityReview.STATUS_DRAFT) and (review.reviewer == request.user or user_role in ['ADMIN', 'QUALITY_MANAGER'])
    can_evaluate = (review.status in [QualityReview.STATUS_PENDING_REVIEW, QualityReview.STATUS_UNDER_REVIEW]) and (user_role in ['ADMIN', 'QUALITY_MANAGER'])
    can_edit = (review.status == QualityReview.STATUS_DRAFT) and (review.reviewer == request.user or user_role == 'ADMIN')

    context = {
        'review': review,
        'audit_logs': audit_logs,
        'can_submit': can_submit,
        'can_evaluate': can_evaluate,
        'can_edit': can_edit,
        'user_role': user_role,
    }
    return render(request, 'reviews/review_detail.html', context)


@login_required
def review_create_view(request):
    suppliers = Supplier.objects.filter(status=Supplier.STATUS_ACTIVE).order_by('name')

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        review_date = request.POST.get('review_date') or datetime.date.today().isoformat()
        defect_count = int(request.POST.get('defect_count') or 0)
        compliance_score = Decimal(request.POST.get('compliance_score') or '0.00')
        delivery_score = Decimal(request.POST.get('delivery_score') or '0.00')
        product_quality_score = Decimal(request.POST.get('product_quality_score') or '0.00')
        comments = request.POST.get('comments', '').strip()
        submit_action = request.POST.get('action', 'save_draft')

        supplier = get_object_or_404(Supplier, pk=supplier_id)

        # Generate unique review ID
        timestamp_suffix = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        review_id = f"QR-{supplier.code}-{timestamp_suffix}"

        review = QualityReview.objects.create(
            review_id=review_id,
            supplier=supplier,
            reviewer=request.user,
            review_date=review_date,
            defect_count=defect_count,
            compliance_score=compliance_score,
            delivery_score=delivery_score,
            product_quality_score=product_quality_score,
            status=QualityReview.STATUS_DRAFT,
            comments=comments,
        )

        ReviewAuditLog.objects.create(
            review=review,
            actor=request.user,
            action=ReviewAuditLog.ACTION_CREATED,
            old_status='',
            new_status=QualityReview.STATUS_DRAFT,
            notes='Initial review draft created.'
        )

        if submit_action == 'submit_for_review':
            review.status = QualityReview.STATUS_PENDING_REVIEW
            review.save()
            ReviewAuditLog.objects.create(
                review=review,
                actor=request.user,
                action=ReviewAuditLog.ACTION_SUBMITTED,
                old_status=QualityReview.STATUS_DRAFT,
                new_status=QualityReview.STATUS_PENDING_REVIEW,
                notes='Submitted directly upon creation.'
            )
            messages.success(request, f"Review '{review.review_id}' submitted for Quality Manager approval.")
        else:
            messages.success(request, f"Review draft '{review.review_id}' saved successfully.")

        return redirect('review-detail', pk=review.pk)

    context = {
        'suppliers': suppliers,
        'today': datetime.date.today().isoformat(),
        'is_edit': False,
    }
    return render(request, 'reviews/review_form.html', context)


@login_required
def review_update_view(request, pk):
    review = get_object_or_404(QualityReview, pk=pk)

    user_role = getattr(request.user.profile, 'role', 'REVIEWER') if hasattr(request.user, 'profile') else 'REVIEWER'
    if not (request.user.is_superuser or user_role == 'ADMIN' or review.reviewer == request.user):
        messages.error(request, "Permission denied. You can only edit your own reviews.")
        return redirect('review-detail', pk=review.pk)

    if review.status != QualityReview.STATUS_DRAFT and not (request.user.is_superuser or user_role == 'ADMIN'):
        messages.error(request, "Only reviews in Draft status can be edited.")
        return redirect('review-detail', pk=review.pk)

    if request.method == 'POST':
        review.defect_count = int(request.POST.get('defect_count') or 0)
        review.compliance_score = Decimal(request.POST.get('compliance_score') or '0.00')
        review.delivery_score = Decimal(request.POST.get('delivery_score') or '0.00')
        review.product_quality_score = Decimal(request.POST.get('product_quality_score') or '0.00')
        review.comments = request.POST.get('comments', '').strip()

        review.save()

        ReviewAuditLog.objects.create(
            review=review,
            actor=request.user,
            action=ReviewAuditLog.ACTION_UPDATED,
            old_status=review.status,
            new_status=review.status,
            notes='Review updated by reviewer.'
        )

        messages.success(request, f"Review '{review.review_id}' updated successfully.")
        return redirect('review-detail', pk=review.pk)

    context = {
        'review': review,
        'suppliers': Supplier.objects.filter(status=Supplier.STATUS_ACTIVE),
        'is_edit': True,
    }
    return render(request, 'reviews/review_form.html', context)


@login_required
def review_transition_view(request, pk):
    review = get_object_or_404(QualityReview, pk=pk)
    target_action = request.POST.get('action')
    remarks = request.POST.get('remarks', '').strip()
    user = request.user

    user_role = getattr(user.profile, 'role', 'REVIEWER') if hasattr(user, 'profile') else 'REVIEWER'
    if user.is_superuser:
        user_role = 'ADMIN'

    old_status = review.status

    if target_action == 'submit':
        if review.status != QualityReview.STATUS_DRAFT:
            messages.error(request, "Only draft reviews can be submitted.")
            return redirect('review-detail', pk=review.pk)
        review.status = QualityReview.STATUS_PENDING_REVIEW
        review.save()
        ReviewAuditLog.objects.create(
            review=review,
            actor=user,
            action=ReviewAuditLog.ACTION_SUBMITTED,
            old_status=old_status,
            new_status=review.status,
            notes=remarks or 'Review submitted for Manager approval.'
        )
        messages.success(request, "Review submitted to Quality Manager.")

    elif target_action == 'approve':
        if user_role not in ['ADMIN', 'QUALITY_MANAGER']:
            messages.error(request, "Access Denied: Only Quality Managers or Admins can approve reviews.")
            return redirect('review-detail', pk=review.pk)
        review.status = QualityReview.STATUS_APPROVED
        review.manager_remarks = remarks or 'Approved by Quality Manager.'
        review.reviewed_by_manager = user
        review.save()
        ReviewAuditLog.objects.create(
            review=review,
            actor=user,
            action=ReviewAuditLog.ACTION_APPROVED,
            old_status=old_status,
            new_status=review.status,
            notes=remarks or 'Review officially approved.'
        )
        messages.success(request, f"Review '{review.review_id}' has been approved!")

    elif target_action == 'reject':
        if user_role not in ['ADMIN', 'QUALITY_MANAGER']:
            messages.error(request, "Access Denied: Only Quality Managers or Admins can reject reviews.")
            return redirect('review-detail', pk=review.pk)
        review.status = QualityReview.STATUS_REJECTED
        review.manager_remarks = remarks or 'Rejected due to quality audit issues.'
        review.reviewed_by_manager = user
        review.save()
        ReviewAuditLog.objects.create(
            review=review,
            actor=user,
            action=ReviewAuditLog.ACTION_REJECTED,
            old_status=old_status,
            new_status=review.status,
            notes=remarks or 'Review rejected.'
        )
        messages.warning(request, f"Review '{review.review_id}' has been rejected.")

    return redirect('review-detail', pk=review.pk)
