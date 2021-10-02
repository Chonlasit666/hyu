# Generated by Django 3.1 on 2020-09-06 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_enrollment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='seats',
            new_name='max_seats',
        ),
        migrations.AddField(
            model_name='course',
            name='avalible_seats',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]