# Generated manually to update code fields in warehouse models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='code',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='code',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
    ]
