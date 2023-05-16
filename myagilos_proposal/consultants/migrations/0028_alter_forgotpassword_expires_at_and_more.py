# Generated by Django 4.1.7 on 2023-05-04 13:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("consultants", "0027_remove_forgotpassword_token_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forgotpassword",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 4, 14, 21, 8, 334014, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="forgotpassword",
            name="salt_and_hash",
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
    ]
