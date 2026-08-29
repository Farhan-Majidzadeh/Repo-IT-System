# Generated manually to add user field to Personnel

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='personnel_code',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='personnel',
            name='user',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='personnel_profile',
                to=settings.AUTH_USER_MODEL,
                verbose_name='حساب کاربری',
            ),
        ),
    ]
