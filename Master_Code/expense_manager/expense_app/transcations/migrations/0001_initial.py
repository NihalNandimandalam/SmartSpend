# Generated by Django 5.0.3 on 2024-04-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transcation",
            fields=[
                ("transcation_id", models.AutoField(primary_key=True, serialize=False)),
                ("transcation_date", models.DateField()),
                ("transcation_description", models.CharField(max_length=200)),
                ("amount", models.FloatField()),
                ("balance", models.FloatField()),
            ],
            options={
                "db_table": "transcation",
            },
        ),
    ]