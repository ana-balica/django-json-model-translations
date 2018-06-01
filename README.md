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

If you want to restrict your translations to a limited number of languages, set [`LANGUAGES`](https://docs.djangoproject.com/en/2.0/ref/settings/#languages) Django setting. 
It is recommended to configure this list, as it allows `TranslationJSONField` to pick up on the list of languages 
without providing and maintaining them for each field separately.

If you add new languages to `LANGUAGES` (which will innevitably happen), 
newly added language codes will not appear as keys in `TranslationJSONField` for existing objects.
However the full list will be used when creating new objects.
If you want to re-populate existing objects with new values, you will need to write a custom data migration.

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

If you try to read from a language that's missing, the field will **fallback to default language** ([`LANGUAGE_CODE`](https://docs.djangoproject.com/en/2.0/ref/settings/#language-code)):

```python
with override('ru_ru'):
    print(vanilla_ice_cream.name)  # vanilla
```

Writting to a new language key is possible and will create this new JSON key-value pair.

### Filtering 

When filtering by a translatable field, make sure to use the default language value.

```python
>>> IceCreamFlavour.objects.filter(name='vanilla')
<IceCreamFlavour: IceCreamFlavour object>
>>> IceCreamFlavour.objects.filter(name='vanille')
None
```

You can always use the `JSONField` querying syntax to filter via a specific key:

```python
>>> IceCreamFlavour.objects.filter(name__fr_fr='vanille')
<IceCreamFlavour: IceCreamFlavour object>
```
