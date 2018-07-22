# -*- coding: utf-8 -*-
import pytest

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.utils.translation import override

from djjmt.fields import TranslationJSONFieldDescriptor


@pytest.fixture
def field_descriptor():
    descriptor = TranslationJSONFieldDescriptor(field_name='foo')
    descriptor.json_value = {'en-gb': 'hello', 'fr-fr': 'salut'}
    return descriptor


def test_get_default_translation(field_descriptor):
    with override('de-de'):
        assert field_descriptor.__get__(None, None) == 'hello'


def test_get_translation_by_lang(field_descriptor):
    with override('fr_FR'):
        assert field_descriptor.__get__(None, None) == 'salut'


@override_settings(LANGUAGE_CODE='de-de')
def test_get_missing_translation_for_default_lang(field_descriptor):
    with override('ro-ro'):
        assert field_descriptor.__get__(None, None) is None


@override_settings(LANGUAGE_CODE=None)
def test_get_translation_when_no_lang(field_descriptor):
    with pytest.raises(ImproperlyConfigured) as exc:
        field_descriptor.__get__(None, None)

    assert 'Enable translations to use TranslationJSONField.' == str(exc.value)


def test_set_translation_json():
    field_descriptor = TranslationJSONFieldDescriptor(field_name='foo')
    assert field_descriptor.json_value is None

    field_descriptor.__set__(None, {})
    assert field_descriptor.json_value == {}

    field_descriptor.__set__(None, {'en': 'Foo', 'de': 'Bar'})
    assert field_descriptor.json_value == {'en': 'Foo', 'de': 'Bar'}


def test_set_translated_value_by_lang(field_descriptor):
    with override('fr_FR'):
        field_descriptor.__set__(None, 'New french value')
        assert field_descriptor.__get__(None, None) == 'New french value'
        assert field_descriptor.json_value == {'en-gb': 'hello', 'fr-fr': 'New french value'}


def test_set_translated_value_for_new_lang(field_descriptor):
    with override('ru-RU'):
        field_descriptor.__set__(None, 'привет')
        assert field_descriptor.__get__(None, None) == 'привет'
        assert field_descriptor.json_value == {'en-gb': 'hello', 'fr-fr': 'salut', 'ru-ru': 'привет'}


@override_settings(LANGUAGE_CODE=None)
def test_set_translation_when_no_lang(field_descriptor):
    with pytest.raises(ImproperlyConfigured) as exc:
        field_descriptor.__set__(None, 'value')

    assert 'Enable translations to use TranslationJSONField.' == str(exc.value)
