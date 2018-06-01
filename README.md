# Django JSON Model Translations

DJJMT (for short) tries to solve the problem of having multiple translations for Django model fields
and loading these translations using Django localisation framework.
This is achieved using JSON fields which can hold an arbitrary number of translations.
Hence this package can only be used with PostgreSQL.

## How it works

### Models

First create translatable fields as `TranslationJSONField`:

```python
from django.db import models
from django.utils.translation import ugettext as _

from djjmt.fields import TranslationJSONField


class IceCreamFlavour(models.Model):
    name = TranslationJSONField(models.CharField(max_length=127), langs=['en_gb', 'fr_fr', 'nl_nl'])
    origin = TranslationJSONField(models.CharField(max_length=127, default=_('Homemade'))
    shop = TranslationJSONField(
        models.CharField(max_length=255), 
        langs=['en_gb', 'fr_fr', 'nl_nl'],
        default=_('Your favourite ice-cream shop'),
    )
    price_per_pound = models.DecimalField()
```

### Settings

If you want to restrict your translations to a limited number of languages, set [LANGUAGES](https://docs.djangoproject.com/en/2.0/ref/settings/#languages) Django setting. 
It is recommended to configure this list, as it allows `TranslationJSONField` to pick up on the list of languages 
without providing and maintaining them for each field separately.

### Reads & writes

```python
from django.utils.translation import activate, override

activate('en_gb')

vanilla_ice_cream = IceCreamFlavour.objects.create(name={'en_gb': 'vanilla', 'fr_fr': 'vanille'}, price_per_pound=50)

# Read the values
print(vanilla_ice_cream.name)  # vanilla
with override('fr_fr'):
    print(vanilla_ice_cream.name)  # vanille
    
with override('nl_nl'):
    print(vanilla_ice_cream.name)  # <empty string>

# Write new values
vanilla_ice_cream.name = 'Best vanilla'
print(vanilla_ice_cream.name)  # New vanilla

with override('fr_fr'):
    vanilla_ice_cream.name = 'Best vanille in French'
    print(vanilla_ice_cream.name)  # Best vanille in French
    
# Dump all values of name
print(vanilla_ice_cream.name__raw)  # {'en_gb': 'New vanilla', 'fr_fr': 'Best vanille in French', 'nl_nl': ''}
```
