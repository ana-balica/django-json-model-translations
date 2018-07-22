from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from .utils import get_normalised_language, normalise_language_code


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

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Attach the custom translation descritor to the
        model attribute to control access to the field values.
        """
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, f'{name}__raw', TranslationJSONRawFieldDescriptor(name))
        setattr(cls, name, TranslationJSONFieldDescriptor())

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        # TODO: check if the keys are valid language codes


class TranslationJSONFieldDescriptor:
    def __init__(self):
        self.json_value = None

    def __get__(self, instance, owner, raw=False):
        """
        Controls read access to a TranslationJSONField.

        :param raw: if True, will return the whole dict
        :returns: value from the dict based on active language.
                  If the language key is missing, will return None.
        """
        if instance is None:
            return self

        if raw is True:
            return self.json_value

        lang = get_normalised_language()
        if lang is None:
            raise ImproperlyConfigured('Enable translations to use TranslationJSONField.')

        if lang not in self.json_value:
            lang = normalise_language_code(settings.LANGUAGE_CODE)

        return self.json_value.get(lang, None)

    def __set__(self, instance, value):
        """
        Controls write access to a TranslationJSONField.

        If the passed value is a dict, will treat it as the raw value of the field
        and store it as an attribute on the descriptor for later use.
        Otherwise will set the passed value on the dict based on the active language.
        """
        if isinstance(value, dict):
            self.json_value = value
        else:
            lang = get_normalised_language()
            if lang is None:
                raise ImproperlyConfigured('Enable translations to use TranslationJSONField.')

            self.json_value[lang] = value


class TranslationJSONRawFieldDescriptor:
    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, instance, owner):
        """
        Return the raw value of the TranslationJSONField
        by accessing and calling the field descriptor explicitly
        and passing the `raw` param.
        """
        descriptor = getattr(type(instance), self.field_name)
        return descriptor.__get__(instance, self, raw=True)

    def __set__(self, instance, value):
        setattr(instance, self.field_name, value)
