import pytest

from django.utils.translation import override

from djjmt.utils import get_normalised_language, normalise_language_code


@pytest.mark.parametrize('lang,expected', [
    ('', ''),
    ('jpn', 'jpn'),
    ('JPN', 'jpn'),
    ('de-de', 'de-de'),
    ('DE-DE', 'de-de'),
    ('DE_DE', 'de-de'),
    ('en_US', 'en-us'),
    ('en-US', 'en-us'),
])
def test_normalise_language_code(lang, expected):
    assert normalise_language_code(lang) == expected


def test_get_normalised_language():
    with override('en-US'):
        assert get_normalised_language() == 'en-us'
