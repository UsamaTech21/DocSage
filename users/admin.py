from django.contrib import admin
from django.db import IntegrityError
from django.contrib import messages
from .models import User, DoctorApplication


@admin.register(DoctorApplication)
class DoctorApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'specialization', 'is_approved', 'submitted_at')
    list_filter = ('is_approved',)
    search_fields = ('full_name', 'email', 'pmdc_number', 'specialization')
    actions = ['approve_application', 'reject_application']

    def save_model(self, request, obj, form, change):
        try:
            # Validate that the user exists before saving
            if not obj.user:
                messages.error(request, f"Cannot save application: No associated user found for {obj.full_name}.")
                return

            super().save_model(request, obj, form, change)
        except IntegrityError as e:
            messages.error(request, f"Error saving application {obj.full_name}: {e}")

    def approve_application(self, request, queryset):
        for application in queryset:
            try:
                if not application.user:
                    messages.error(
                        request,
                        f"Cannot approve application {application.full_name}: No associated user found.",
                    )
                    continue

                if not application.is_approved:
                    application.is_approved = True
                    application.save()
                    application.user.is_doctor = True
                    application.user.save()
                    messages.success(
                        request, f"Application for {application.full_name} approved successfully."
                    )
                else:
                    messages.warning(
                        request, f"Application for {application.full_name} is already approved."
                    )
            except IntegrityError as e:
                messages.error(
                    request,
                    f"Error approving application {application.full_name}: {e}",
                )

    approve_application.short_description = "Approve selected applications"

    def reject_application(self, request, queryset):
        for application in queryset:
            try:
                if application.is_approved:
                    application.is_approved = False
                    application.save()
                    if application.user:
                        application.user.is_doctor = False
                        application.user.save()
                    messages.success(
                        request, f"Application for {application.full_name} rejected successfully."
                    )
                else:
                    messages.warning(
                        request, f"Application for {application.full_name} is already rejected."
                    )
            except IntegrityError as e:
                messages.error(
                    request,
                    f"Error rejecting application {application.full_name}: {e}",
                )

    reject_application.short_description = "Reject selected applications"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_doctor', 'is_staff', 'is_superuser')
    list_filter = ('is_doctor', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
