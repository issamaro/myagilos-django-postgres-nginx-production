# Generated by Django 4.1.7 on 2023-04-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("consultants", "0009_consultants_target"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultants",
            name="first",
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AddField(
            model_name="consultants",
            name="last",
            field=models.CharField(default=None, max_length=30),
        ),
    ]
