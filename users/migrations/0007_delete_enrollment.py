# Generated by Django 3.1 on 2020-09-09 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_student_courses'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Enrollment',
        ),
    ]
