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

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Attach the custom translation descritor to the
        model attribute to control access to the field values.
        """
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, name, TranslationJSONFieldDescriptor(name))

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        # TODO: check if the keys are valid language codes


class TranslationJSONFieldDescriptor(object):
    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, instance, owner):
        print('Accessing the value via descriptor')
        return 'foo'
