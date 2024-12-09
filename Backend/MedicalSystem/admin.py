'''from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'password', 'name', 'gender', 'birth', 'id_number', 'user_type', 'phone')
    search_fields = ('user_id', 'name')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'password', 'name', 'gender','image', 'title')
    search_fields = ('doctor_id', 'name')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'password', 'name')
    search_fields = ('admin_id', 'name')


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('family_id', 'user', 'relationship', 'name', 'gender', 'birth', 'id_number')
    search_fields = ('family_id', 'user', 'name')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name')
    search_fields = ('department_id', 'department_name')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_id', 'doctor', 'department', 'schedule_time')
    search_fields = ('schedule_id',)


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('pharmacy_id', 'pharmacy_name')
    search_fields = ('pharmacy_id', 'pharmacy_name')


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('drug_id', 'drug_name', 'image', 'price')
    search_fields = ('drug_id', 'drug_name')


@admin.register(DrugInventory)
class DrugInventoryAdmin(admin.ModelAdmin):
    list_display = ('drug_id', 'drug_amount', 'pharmacy_id')
    search_fields = ('drug_id', 'pharmacy_id')


@admin.register(ExaminationArrangement)
class ExaminationArrangementAdmin(admin.ModelAdmin):
    list_display = ('examination_id', 'examination_date', 'doctor')
    search_fields = ('examination_id',)


@admin.register(ExaminationInfo)
class ExaminationInfoAdmin(admin.ModelAdmin):
    list_display = ('exam_appointment_id', 'examination_arrangement', 'examination_result', 'user')
    search_fields = ('exam_appointment_id',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'relationship', 'schedule', 'user')
    search_fields = ('appointment_id',)


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'diagnosis_id', 'examination', 'examination_result', 'reference', 'clinical_diagnosis', 'prescription_id',
        'diagnosis_time', 'id_number', 'appointment_id', 'doctor_id')
    search_fields = ('diagnosis_id',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'diagnosis_id', 'drug_id', 'drug_amount', 'usage', 'precautions')
    search_fields = ('prescription_id',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'notification', 'notification_time', 'user_id')
    search_fields = ('notification_id',)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('evaluation_id', 'evaluation', 'evaluation_time', 'user_id', 'doctor_id')
    search_fields = ('evaluation_id',)

'''