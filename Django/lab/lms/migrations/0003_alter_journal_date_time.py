# Generated by Django 4.1.5 on 2023-02-12 15:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_alter_client_options_alter_journal_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]