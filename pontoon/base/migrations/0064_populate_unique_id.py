# Generated by Django 4.2.11 on 2024-05-22 12:25

import uuid

from django.db import migrations


def populate_unique_id(apps, schema_editor):
    UserProfile = apps.get_model("base", "UserProfile")
    for profile in UserProfile.objects.all():
        profile.unique_id = uuid.uuid4()
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0063_userprofile_unique_id"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_unique_id,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
