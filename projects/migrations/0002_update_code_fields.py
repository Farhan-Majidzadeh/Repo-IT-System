# Generated manually to update code field in projects model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
    ]
