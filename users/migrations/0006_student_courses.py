# Generated by Django 3.1 on 2020-09-06 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='courses', to='users.Course'),
        ),
    ]
