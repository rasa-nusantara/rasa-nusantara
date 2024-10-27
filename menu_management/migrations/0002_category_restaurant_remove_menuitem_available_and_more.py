# Generated by Django 5.1.1 on 2024-10-26 16:40

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('average_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rating', models.FloatField()),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='available',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='description',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='price',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='menu_items', to='menu_management.category'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='menu_management.restaurant'),
        ),
    ]