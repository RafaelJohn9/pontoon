# Generated by Django 4.2.11 on 2024-08-16 10:45

import datetime

from django.db import migrations
from django.db.models import Q


def migrate_translation_to_actionlog(apps, schema_editor):
    Translation = apps.get_model("base", "Translation")
    ActionLog = apps.get_model("actionlog", "ActionLog")

    traslation_info = {
        "date": ActionLog.ActionType.TRANSLATION_CREATED,
        "approved_date": ActionLog.ActionType.TRANSLATION_APPROVED,
        "unapproved_date": ActionLog.ActionType.TRANSLATION_UNAPPROVED,
        "rejected_date": ActionLog.ActionType.TRANSLATION_REJECTED,
        "unrejected_date": ActionLog.ActionType.TRANSLATION_UNREJECTED,
    }

    # date to end migration
    end_date = datetime.datetime(
        2020, 1, 7, 9, 25, 11, 829125, tzinfo=datetime.timezone.utc
    )

    actions_to_log = []

    translations = Translation.objects.filter(
        Q(date__lt=end_date)
        | Q(approved_date__lt=end_date)
        | Q(unapproved_date__lt=end_date)
        | Q(rejected_date__lt=end_date)
        | Q(unrejected_date__lt=end_date)
    )

    for translation in translations:
        for attr, action_type in traslation_info.items():
            if getattr(translation, attr) is not None:
                actions_to_log.append(
                    ActionLog(
                        action_type=action_type,
                        created_at=translation.date,
                        performed_by_id=translation.user_id,
                        translation_id=translation.id,
                    )
                )
    ActionLog.objects.bulk_create(actions_to_log)


class Migration(migrations.Migration):
    dependencies = [
        ("actionlog", "0003_existing_pretranslation_action"),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_translation_to_actionlog,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
