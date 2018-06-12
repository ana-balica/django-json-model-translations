from django.db import models


class TranslationJSONField(models.JSONField):

    def __init__(self, base_field, langs=None, **kwargs):
        super().__init__(**kwargs)
        self.base_field = base_field
        self.langs = langs or []
