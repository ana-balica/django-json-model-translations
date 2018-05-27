# Django JSON Model Translations

DJJMT (for short) tries to solve the problem of having multiple translations for Django model fields
and loading these translations using Django localisation framework.
This is achieved using JSON fields which can hold an arbitrary number of translations.
Hence this package can only be used with PostgreSQL.

## How it works

First create translatable fields as `TranslationJSONField`:

```python
from django.db import models
from django.utils.translation import ugettext as _

from djjmt.fields import TranslationJSONField


class IceCreamFlavour(models.Model):
    name = TranslationJSONField(models.CharField(max_length=127), default_langs=['en_gb', 'fr_fr', 'nl_nl'])
    shop = TranslationJSONField(
        models.CharField(max_length=255), 
        default_langs=['en_gb', 'fr_fr', 'nl_nl'],
        default=_('Your favourite ice-cream shop'),
    )
    price_per_pound = models.DecimalField()
```
