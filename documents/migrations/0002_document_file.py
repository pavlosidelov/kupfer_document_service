# Generated by Django 2.0.5 on 2018-05-16 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True,
                                   upload_to='documents'),
        ),
    ]