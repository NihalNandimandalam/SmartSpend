# Generated by Django 5.0.3 on 2024-04-10 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transcations", "0005_remove_balance_balance"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="balance",
            old_name="transcation_date",
            new_name="transaction_date",
        ),
        migrations.RenameField(
            model_name="balance",
            old_name="transcation_description",
            new_name="transaction_description",
        ),
        migrations.RenameField(
            model_name="balance",
            old_name="transcation_id",
            new_name="transaction_id",
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="balance",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="transcations.customer",
            ),
        ),
    ]
