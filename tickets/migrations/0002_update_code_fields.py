# Generated manually to update code fields in tickets models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketcategory',
            name='code',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='code',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
    ]
