# Generated by Django 5.0.4 on 2024-06-18 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_create__service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(default=None),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(default=None, unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
