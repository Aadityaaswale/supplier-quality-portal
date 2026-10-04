from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.suppliers.models import Supplier
from apps.reviews.models import QualityReview, ReviewAuditLog
import datetime
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds realistic enterprise supplier and quality review demonstration data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Beginning database seeding...'))

        # 1. Create Users & Profiles
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@supplierportal.local',
                'password': 'Admin@12345',
                'first_name': 'Aaditya',
                'last_name': 'Aswale (Admin)',
                'role': UserProfile.ROLE_ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'department': 'Corporate Quality Leadership'
            },
            {
                'username': 'manager',
                'email': 'manager@supplierportal.local',
                'password': 'Manager@12345',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'role': UserProfile.ROLE_QUALITY_MANAGER,
                'is_staff': False,
                'is_superuser': False,
                'department': 'Supplier Quality Engineering'
            },
            {
                'username': 'reviewer',
                'email': 'reviewer@supplierportal.local',
                'password': 'Reviewer@12345',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'role': UserProfile.ROLE_REVIEWER,
                'is_staff': False,
                'is_superuser': False,
                'department': 'Incoming Inspection'
            },
        ]

        users = {}
        for udata in users_data:
            user, created = User.objects.get_or_create(username=udata['username'])
            user.email = udata['email']
            user.first_name = udata['first_name']
            user.last_name = udata['last_name']
            user.is_staff = udata['is_staff']
            user.is_superuser = udata['is_superuser']
            user.set_password(udata['password'])
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = udata['role']
            profile.department = udata['department']
            profile.save()
            users[udata['username']] = user
            self.stdout.write(f"User: {user.username} [{profile.role}] ready.")

        # 2. Create Suppliers
        suppliers_data = [
            {
                'supplier_id': 'SUP-2026-001',
                'name': 'Apex Components',
                'code': 'APEX-IND',
                'contact_person': 'David Reynolds',
                'email': 'david.reynolds@apexcomponents.com',
                'phone': '+1 (555) 234-5678',
                'address': '450 Technology Parkway, Austin, TX 78701',
                'category': Supplier.CATEGORY_ELECTRONICS,
                'status': Supplier.STATUS_ACTIVE,
            },
            {
                'supplier_id': 'SUP-2026-002',
                'name': 'Orion Manufacturing',
                'code': 'ORION-MFG',
                'contact_person': 'Elena Rostova',
                'email': 'elena.rostova@orionmfg.com',
                'phone': '+1 (555) 876-5432',
                'address': '1200 Industrial Boulevard, Detroit, MI 48201',
                'category': Supplier.CATEGORY_MECHANICAL,
                'status': Supplier.STATUS_ACTIVE,
            },
            {
                'supplier_id': 'SUP-2026-003',
                'name': 'Vertex Industrial',
                'code': 'VERTEX-IND',
                'contact_person': 'Robert Chen',
                'email': 'robert.chen@vertexindustrial.com',
                'phone': '+1 (555) 345-6789',
                'address': '78 Foundry Road, Cleveland, OH 44101',
                'category': Supplier.CATEGORY_RAW,
                'status': Supplier.STATUS_ACTIVE,
            },
            {
                'supplier_id': 'SUP-2026-004',
                'name': 'Nova Precision',
                'code': 'NOVA-PREC',
                'contact_person': 'Amara Okafor',
                'email': 'amara.okafor@novaprecision.com',
                'phone': '+1 (555) 456-7890',
                'address': '300 Machining Way, Indianapolis, IN 46201',
                'category': Supplier.CATEGORY_MECHANICAL,
                'status': Supplier.STATUS_UNDER_REVIEW,
            },
            {
                'supplier_id': 'SUP-2026-005',
                'name': 'Zenith Materials',
                'code': 'ZENITH-MAT',
                'contact_person': 'Liam Gallagher',
                'email': 'liam.gallagher@zenithmaterials.com',
                'phone': '+1 (555) 567-8901',
                'address': '89 Polymer Circle, Houston, TX 77001',
                'category': Supplier.CATEGORY_CHEMICALS,
                'status': Supplier.STATUS_ACTIVE,
            },
        ]

        suppliers = {}
        for sdata in suppliers_data:
            supplier, _ = Supplier.objects.get_or_create(
                supplier_id=sdata['supplier_id'],
                defaults=sdata
            )
            suppliers[supplier.code] = supplier
            self.stdout.write(f"Supplier: {supplier.name} ({supplier.code}) ready.")

        # 3. Create Realistic Quality Reviews
        reviews_data = [
            # Apex Components - 2 Reviews (Approved)
            {
                'review_id': 'QR-APEX-2026-01',
                'supplier': suppliers['APEX-IND'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 1, 15),
                'defect_count': 1,
                'product_quality_score': Decimal('95.00'),
                'compliance_score': Decimal('98.00'),
                'delivery_score': Decimal('92.00'),
                'status': QualityReview.STATUS_APPROVED,
                'comments': 'SMT component packaging and batch testing within 3-sigma tolerance.',
                'manager_remarks': 'High consistency. Lot approved for avionics assembly.',
                'manager': users['manager']
            },
            {
                'review_id': 'QR-APEX-2026-02',
                'supplier': suppliers['APEX-IND'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 2, 20),
                'defect_count': 0,
                'product_quality_score': Decimal('97.50'),
                'compliance_score': Decimal('96.00'),
                'delivery_score': Decimal('95.00'),
                'status': QualityReview.STATUS_APPROVED,
                'comments': 'Zero solder defects noted across 5,000 sampled units.',
                'manager_remarks': 'Exceptional performance. Supplier eligible for preferred status.',
                'manager': users['manager']
            },
            # Orion Manufacturing - 1 Approved, 1 Pending
            {
                'review_id': 'QR-ORION-2026-01',
                'supplier': suppliers['ORION-MFG'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 2, 10),
                'defect_count': 3,
                'product_quality_score': Decimal('88.00'),
                'compliance_score': Decimal('90.00'),
                'delivery_score': Decimal('85.00'),
                'status': QualityReview.STATUS_APPROVED,
                'comments': 'Castings exhibit minor surface roughness but meet structural tensile criteria.',
                'manager_remarks': 'Approved with note to monitor surface finishing tooling wear.',
                'manager': users['manager']
            },
            {
                'review_id': 'QR-ORION-2026-02',
                'supplier': suppliers['ORION-MFG'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 3, 1),
                'defect_count': 2,
                'product_quality_score': Decimal('89.00'),
                'compliance_score': Decimal('92.00'),
                'delivery_score': Decimal('88.00'),
                'status': QualityReview.STATUS_PENDING_REVIEW,
                'comments': 'Batch dimensional tolerance audit awaiting final manager certification.',
                'manager_remarks': '',
                'manager': None
            },
            # Vertex Industrial - 1 Approved
            {
                'review_id': 'QR-VERTEX-2026-01',
                'supplier': suppliers['VERTEX-IND'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 1, 28),
                'defect_count': 4,
                'product_quality_score': Decimal('82.00'),
                'compliance_score': Decimal('85.00'),
                'delivery_score': Decimal('78.00'),
                'status': QualityReview.STATUS_APPROVED,
                'comments': 'Alloy composition certificate verified. Delivery had 2 days transit delay.',
                'manager_remarks': 'Approved. Supplier cautioned regarding logistical lead times.',
                'manager': users['manager']
            },
            # Nova Precision - 1 Under Review
            {
                'review_id': 'QR-NOVA-2026-01',
                'supplier': suppliers['NOVA-PREC'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 3, 10),
                'defect_count': 6,
                'product_quality_score': Decimal('74.00'),
                'compliance_score': Decimal('80.00'),
                'delivery_score': Decimal('82.00'),
                'status': QualityReview.STATUS_UNDER_REVIEW,
                'comments': 'CNC milling tolerance deviations on Lot 48B. Remediation plan requested.',
                'manager_remarks': 'Under evaluation by Quality Manager.',
                'manager': None
            },
            # Zenith Materials - 1 Approved, 1 Draft
            {
                'review_id': 'QR-ZENITH-2026-01',
                'supplier': suppliers['ZENITH-MAT'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 2, 18),
                'defect_count': 1,
                'product_quality_score': Decimal('93.00'),
                'compliance_score': Decimal('95.00'),
                'delivery_score': Decimal('91.00'),
                'status': QualityReview.STATUS_APPROVED,
                'comments': 'Polymer viscosity index within target specifications.',
                'manager_remarks': 'Approved for chemical tank blending.',
                'manager': users['manager']
            },
            {
                'review_id': 'QR-ZENITH-2026-02',
                'supplier': suppliers['ZENITH-MAT'],
                'reviewer': users['reviewer'],
                'review_date': datetime.date(2026, 3, 22),
                'defect_count': 0,
                'product_quality_score': Decimal('94.00'),
                'compliance_score': Decimal('96.00'),
                'delivery_score': Decimal('92.00'),
                'status': QualityReview.STATUS_DRAFT,
                'comments': 'Draft audit notes in preparation.',
                'manager_remarks': '',
                'manager': None
            },
        ]

        for rdata in reviews_data:
            review, created = QualityReview.objects.get_or_create(
                review_id=rdata['review_id'],
                defaults={
                    'supplier': rdata['supplier'],
                    'reviewer': rdata['reviewer'],
                    'review_date': rdata['review_date'],
                    'defect_count': rdata['defect_count'],
                    'product_quality_score': rdata['product_quality_score'],
                    'compliance_score': rdata['compliance_score'],
                    'delivery_score': rdata['delivery_score'],
                    'status': rdata['status'],
                    'comments': rdata['comments'],
                    'manager_remarks': rdata['manager_remarks'],
                    'reviewed_by_manager': rdata['manager'],
                }
            )

            # Create audit log trail
            ReviewAuditLog.objects.get_or_create(
                review=review,
                action=ReviewAuditLog.ACTION_CREATED,
                defaults={
                    'actor': rdata['reviewer'],
                    'old_status': '',
                    'new_status': QualityReview.STATUS_DRAFT,
                    'notes': 'Initial inspection draft generated.'
                }
            )

            if rdata['status'] in [QualityReview.STATUS_PENDING_REVIEW, QualityReview.STATUS_UNDER_REVIEW, QualityReview.STATUS_APPROVED]:
                ReviewAuditLog.objects.get_or_create(
                    review=review,
                    action=ReviewAuditLog.ACTION_SUBMITTED,
                    defaults={
                        'actor': rdata['reviewer'],
                        'old_status': QualityReview.STATUS_DRAFT,
                        'new_status': QualityReview.STATUS_PENDING_REVIEW,
                        'notes': 'Submitted for managerial audit evaluation.'
                    }
                )

            if rdata['status'] == QualityReview.STATUS_APPROVED:
                ReviewAuditLog.objects.get_or_create(
                    review=review,
                    action=ReviewAuditLog.ACTION_APPROVED,
                    defaults={
                        'actor': rdata['manager'],
                        'old_status': QualityReview.STATUS_PENDING_REVIEW,
                        'new_status': QualityReview.STATUS_APPROVED,
                        'notes': rdata['manager_remarks']
                    }
                )

        # 4. Trigger recalculation of all supplier overall scores
        for s in Supplier.objects.all():
            s.recalculate_overall_score()
            self.stdout.write(f"Updated {s.name}: Score={s.overall_quality_score}%, Grade={s.grade}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with realistic enterprise data!'))
