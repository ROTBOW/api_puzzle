# Generated by Django 5.0.7 on 2024-08-05 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("breaker", "0002_completion_gate"),
    ]

    operations = [
        migrations.AddField(
            model_name="attempt",
            name="curr_ans",
            field=models.TextField(default="seagull", max_length=255),
        ),
    ]
