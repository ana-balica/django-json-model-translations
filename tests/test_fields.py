import pytest

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.utils.translation import override

from djjmt.fields import TranslationJSONFieldDescriptor


@pytest.fixture
def translation_descriptor():
    descriptor = TranslationJSONFieldDescriptor(field_name='foo')
    descriptor.json_value = {'en-gb': 'hello', 'fr-fr': 'salut'}
    return descriptor


def test_get_default_translation(translation_descriptor):
    with override('de-de'):
        assert translation_descriptor.__get__(None, None) == 'hello'


def test_get_translation_based_on_active_language(translation_descriptor):
    with override('fr_FR'):
        assert translation_descriptor.__get__(None, None) == 'salut'


@override_settings(LANGUAGE_CODE='de-de')
def test_get_missing_translation_for_default_lang(translation_descriptor):
    with override('ro-ro'):
        assert translation_descriptor.__get__(None, None) is None


@override_settings(LANGUAGE_CODE=None)
def test_get_translation_when_no_language(translation_descriptor):
    with pytest.raises(ImproperlyConfigured) as exc:
        translation_descriptor.__get__(None, None)

    assert 'Enable translations to use TranslationJSONField.' == str(exc.value)
