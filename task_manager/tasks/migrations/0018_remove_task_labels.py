# Generated by Django 4.1.2 on 2022-11-14 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0017_auto_20221114_1721"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="labels",
        ),
    ]
