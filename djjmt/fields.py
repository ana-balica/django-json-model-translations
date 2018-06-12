from django.db import models


class TranslationJSONField(models.JSONField):

    def __init__(self, verbose_name=None, name=None, encoder=None, **kwargs):
        super().__init__(verbose_name, name, encoder, **kwargs)
        self.base_field = kwargs.get('base_field')
        self.langs = kwargs.get('langs', [])

        if not self.base_field:
            raise ValueError('The base_field parameter must be provided.')
