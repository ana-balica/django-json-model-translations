from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _


class TranslationJSONField(JSONField):
    description = _('A JSON object with translations')

    def __init__(self, base_field, langs=None, **kwargs):
        super().__init__(**kwargs)
        self.base_field = base_field
        self.langs = langs or []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.langs is not None:
            kwargs['langs'] = self.langs
        return name, path, args, kwargs
