from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class TranslationJSONField(JSONField):
    description = _('A JSON object with translations')

    def __init__(self, base_field, langs=None, **kwargs):
        super().__init__(**kwargs)
        self.base_field = base_field
        self.langs = langs or []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['base_field'] = self.base_field
        if self.langs is not None:
            kwargs['langs'] = self.langs
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        # TODO: convert to a func that's called when the value is read, not when it's loaded from db
        # TODO: normalize the language code to a common format
        lang = get_language()
        if lang is None:
            raise ImproperlyConfigured('Enable translations to use TranslationJSONField.')

        if value is None:
            return value

        if lang in value:
            return value.get(lang)
        else:
            default_lang = settings.LANGUAGE_CODE
            return value.get(default_lang)
