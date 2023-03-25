# Generated by Django 4.0.5 on 2022-06-26 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0019_alter_blog_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(default=uuid.UUID('7fd41869-0cb0-40bd-801a-d8c69fcf4720'), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog', to=settings.AUTH_USER_MODEL, unique=True, verbose_name='User'),
        ),
    ]