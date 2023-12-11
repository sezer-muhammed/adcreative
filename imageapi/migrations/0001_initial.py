# Generated by Django 4.2.7 on 2023-12-11 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageGeneration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='original_images/')),
                ('processed_image', models.ImageField(blank=True, null=True, upload_to='processed_images/')),
                ('color_hex', models.CharField(max_length=7)),
                ('color_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertisementTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='logos/')),
                ('punchline', models.TextField()),
                ('button_text', models.TextField()),
                ('color_hex', models.CharField(max_length=7)),
                ('advertisement_image', models.ImageField(blank=True, null=True, upload_to='advertisements/')),
                ('generated_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imageapi.imagegeneration')),
            ],
        ),
    ]
