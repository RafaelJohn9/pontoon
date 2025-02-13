import pytest

from django.core.exceptions import ValidationError

from pontoon.actionlog import utils
from pontoon.actionlog.models import ActionLog
from pontoon.test.factories import TranslationMemoryFactory


@pytest.mark.django_db
def test_log_action_missing_arg(user_a, entity_a, locale_a):
    # No translation nor (entity and locale) pair.
    with pytest.raises(ValidationError):
        utils.log_action(ActionLog.ActionType.TRANSLATION_CREATED, user_a)

    # Missing locale.
    with pytest.raises(ValidationError):
        utils.log_action(
            ActionLog.ActionType.TRANSLATION_DELETED, user_a, entity=entity_a
        )

    # Missing entity.
    with pytest.raises(ValidationError):
        utils.log_action(
            ActionLog.ActionType.TRANSLATION_DELETED, user_a, locale=locale_a
        )


@pytest.mark.django_db
def test_log_action_unknown_action_type(user_a, translation_a):
    # We send an unsupported action type.
    with pytest.raises(ValidationError):
        utils.log_action(
            "test:unknown",
            user_a,
            translation=translation_a,
        )


@pytest.mark.django_db
def test_log_action_deleted_wrong_keys(user_a, translation_a):
    # We send the wrong parameters for the "deleted" action.
    with pytest.raises(ValidationError):
        utils.log_action(
            ActionLog.ActionType.TRANSLATION_DELETED,
            user_a,
            translation=translation_a,
        )


@pytest.mark.django_db
def test_log_action_non_deleted_wrong_keys(user_a, entity_a, locale_a):
    # We send the wrong parameters for a non-"deleted" action.
    with pytest.raises(ValidationError):
        utils.log_action(
            ActionLog.ActionType.TRANSLATION_APPROVED,
            user_a,
            entity=entity_a,
            locale=locale_a,
        )


@pytest.mark.django_db
def test_log_action_valid_with_translation(user_a, translation_a):
    utils.log_action(
        ActionLog.ActionType.TRANSLATION_CREATED,
        user_a,
        translation=translation_a,
    )

    log = ActionLog.objects.filter(performed_by=user_a, translation=translation_a)
    assert len(log) == 1
    assert log[0].action_type == ActionLog.ActionType.TRANSLATION_CREATED


@pytest.mark.django_db
def test_log_action_valid_with_entity_locale(user_a, entity_a, locale_a):
    utils.log_action(
        ActionLog.ActionType.TRANSLATION_DELETED,
        user_a,
        entity=entity_a,
        locale=locale_a,
    )

    log = ActionLog.objects.filter(
        performed_by=user_a,
        entity=entity_a,
        locale=locale_a,
    )
    assert len(log) == 1
    assert log[0].action_type == ActionLog.ActionType.TRANSLATION_DELETED


@pytest.mark.django_db
def test_log_action_valid_with_tm_entry_deleted(user_a, entity_a, locale_a):
    utils.log_action(
        ActionLog.ActionType.TM_ENTRY_DELETED,
        user_a,
        entity=entity_a,
        locale=locale_a,
    )

    log = ActionLog.objects.filter(
        performed_by=user_a,
        entity=entity_a,
        locale=locale_a,
    )
    assert len(log) == 1
    assert log[0].action_type == ActionLog.ActionType.TM_ENTRY_DELETED


@pytest.mark.django_db
def test_log_action_valid_with_tm_entries_edited(user_a, entity_a, locale_a):
    tm_entry = TranslationMemoryFactory.create(
        entity=entity_a,
        source=entity_a.string,
        target="tm_translation",
        locale=locale_a,
    )

    utils.log_action(
        ActionLog.ActionType.TM_ENTRIES_EDITED,
        user_a,
        tm_entries=[tm_entry],
    )

    log = ActionLog.objects.filter(
        performed_by=user_a,
        tm_entries=tm_entry.pk,
    )
    assert len(log) == 1
    assert log[0].action_type == ActionLog.ActionType.TM_ENTRIES_EDITED
