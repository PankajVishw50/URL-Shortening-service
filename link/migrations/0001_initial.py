# Generated by Django 5.1.1 on 2024-09-18 08:07

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('unique_identifier', models.CharField(max_length=16)),
                ('visits', models.IntegerField(default=0)),
                ('allowed_visits', models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000000000)])),
                ('expiration_datetime', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_datetime', models.DateTimeField(auto_now_add=True)),
                ('user_agent', models.CharField(blank=True, max_length=256, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('referrer', models.CharField(blank=True, max_length=256, null=True)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='link.url')),
            ],
        ),
    ]
