# Generated by Django 4.1.5 on 2023-02-13 05:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_alter_journal_is_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='journal',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='date_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.CreateModel(
            name='Journal2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('client_name', models.CharField(max_length=255)),
                ('client_surname', models.CharField(max_length=255)),
                ('client_phone', models.IntegerField(blank=True, null=True)),
                ('analysis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.analysis')),
            ],
        ),
    ]