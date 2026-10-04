from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Count, Sum
import csv
import datetime

from apps.suppliers.models import Supplier
from apps.reviews.models import QualityReview


@login_required
def reports_view(request):
    category_summary = (
        Supplier.objects.values('category')
        .annotate(
            supplier_count=Count('id'),
            avg_score=Avg('overall_quality_score')
        )
        .order_by('category')
    )

    defect_summary = (
        QualityReview.objects.values('supplier__name', 'supplier__code')
        .annotate(
            total_defects=Sum('defect_count'),
            review_count=Count('id'),
            avg_quality=Avg('product_quality_score')
        )
        .order_by('-total_defects')[:10]
    )

    context = {
        'category_summary': category_summary,
        'defect_summary': defect_summary,
    }
    return render(request, 'reports/reports_index.html', context)


@login_required
def export_suppliers_csv(request):
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="suppliers_report_{timestamp}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Supplier ID', 'Supplier Name', 'Supplier Code', 'Category',
        'Contact Person', 'Email', 'Phone', 'Status',
        'Overall Quality Score', 'Grade', 'Created Date'
    ])

    suppliers = Supplier.objects.all().order_by('name')
    for s in suppliers:
        writer.writerow([
            s.supplier_id, s.name, s.code, s.category,
            s.contact_person, s.email, s.phone, s.status,
            s.overall_quality_score, s.grade, s.created_at.strftime('%Y-%m-%d')
        ])

    return response


@login_required
def export_reviews_csv(request):
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="quality_reviews_report_{timestamp}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Review ID', 'Supplier', 'Reviewer', 'Review Date',
        'Defect Count', 'Compliance Score', 'Delivery Score',
        'Product Quality Score', 'Overall Score', 'Status',
        'Manager Remarks', 'Created Date'
    ])

    reviews = QualityReview.objects.select_related('supplier', 'reviewer').all().order_by('-review_date')
    for r in reviews:
        writer.writerow([
            r.review_id, r.supplier.name, r.reviewer.username, r.review_date.strftime('%Y-%m-%d'),
            r.defect_count, r.compliance_score, r.delivery_score,
            r.product_quality_score, r.overall_score, r.status,
            r.manager_remarks, r.created_at.strftime('%Y-%m-%d')
        ])

    return response
