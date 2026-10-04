from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_ADMIN = 'ADMIN'
    ROLE_QUALITY_MANAGER = 'QUALITY_MANAGER'
    ROLE_REVIEWER = 'REVIEWER'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_QUALITY_MANAGER, 'Quality Manager'),
        (ROLE_REVIEWER, 'Reviewer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_REVIEWER)
    department = models.CharField(max_length=100, blank=True, default='Quality Assurance')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.user.is_superuser

    @property
    def is_quality_manager(self):
        return self.role == self.ROLE_QUALITY_MANAGER or self.is_admin

    @property
    def is_reviewer(self):
        return self.role == self.ROLE_REVIEWER or self.is_quality_manager


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
