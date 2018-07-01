from django.db.models.base import ModelBase
from .fields import TranslationJSONField, TranslationJSONFieldDescriptor


class AlreadyRegistered(Exception):
    pass


class Translator(object):

    def __init__(self):
        self._registry = []

    def register(self, model_or_iterable, **options):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            # Can this work if the model is abstract
            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            self._patch_translation_fields(model)
            self._registry.append(model)

    def _patch_translation_fields(self, model):
        fields = model._meta.get_fields()
        for field in fields:
            if isinstance(field, TranslationJSONField):
                descriptor = TranslationJSONFieldDescriptor(field)
                setattr(model, field.name, descriptor)


translator = Translator()
