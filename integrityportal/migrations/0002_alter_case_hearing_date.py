# Generated by Django 5.0.6 on 2024-05-25 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrityportal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='hearing_date',
            field=models.TextField(),
        ),
    ]
