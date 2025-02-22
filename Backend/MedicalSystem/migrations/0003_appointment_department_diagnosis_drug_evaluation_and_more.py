# Generated by Django 5.1.2 on 2024-10-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MedicalSystem", "0002_admin_doctor_rename_userdata_user_familymember"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "appointment_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("relationship", models.CharField(max_length=10)),
                ("schedule_id", models.CharField(max_length=8)),
                ("student_id", models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "department_id",
                    models.CharField(max_length=3, primary_key=True, serialize=False),
                ),
                ("department_name", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Diagnosis",
            fields=[
                (
                    "diagnosis_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("examination", models.TextField()),
                ("examination_result", models.TextField()),
                ("reference_range", models.TextField()),
                ("clinical_diagnosis", models.TextField()),
                ("prescription_id", models.CharField(max_length=8)),
                ("diagnosis_time", models.DateTimeField()),
                ("patient_id_number", models.CharField(max_length=18)),
                ("appointment_id", models.CharField(max_length=8)),
                ("staff_id", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="Drug",
            fields=[
                (
                    "drug_id",
                    models.CharField(max_length=9, primary_key=True, serialize=False),
                ),
                ("drug_name", models.CharField(max_length=20)),
                ("price", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Evaluation",
            fields=[
                (
                    "evaluation_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("evaluation_text", models.TextField()),
                ("evaluation_time", models.DateTimeField()),
                ("evaluator_student_id", models.CharField(max_length=8)),
                ("evaluated_staff_id", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="ExaminationArrangement",
            fields=[
                (
                    "examination_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("examination_text", models.TextField()),
                ("examination_date", models.DateField()),
                ("staff_id", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="ExaminationInfo",
            fields=[
                (
                    "exam_appointment_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("examination_id", models.CharField(max_length=8)),
                ("examination_result", models.TextField(blank=True, null=True)),
                ("student_id", models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "image_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("image_path", models.CharField(max_length=255)),
                (
                    "evaluation_id",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                (
                    "notification_id",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                ("drug_id", models.CharField(blank=True, max_length=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "notification_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("notification_text", models.TextField()),
                ("notification_time", models.DateTimeField()),
                ("recipient_student_id", models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name="Pharmacy",
            fields=[
                (
                    "pharmacy_id",
                    models.CharField(max_length=2, primary_key=True, serialize=False),
                ),
                ("pharmacy_name", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Prescription",
            fields=[
                (
                    "prescription_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("diagnosis_id", models.CharField(max_length=8)),
                ("drug_id", models.CharField(max_length=9)),
                ("drug_amount", models.IntegerField()),
                ("usage", models.TextField()),
                ("precautions", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "schedule_id",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("staff_id", models.CharField(max_length=5)),
                ("department_id", models.CharField(max_length=3)),
                ("schedule_time", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="DrugInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("drug_id", models.CharField(max_length=9)),
                ("drug_amount", models.IntegerField()),
                ("pharmacy_id", models.CharField(max_length=2)),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("drug_id", "pharmacy_id"), name="unique_drug_pharmacy"
                    )
                ],
            },
        ),
    ]
