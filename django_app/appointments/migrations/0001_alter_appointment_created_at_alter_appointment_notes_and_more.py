# Generated by Django 5.0.4 on 2024-07-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', 'create__appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='notes',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]