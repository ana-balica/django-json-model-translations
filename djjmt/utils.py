from django.utils.translation import get_language


def normalise_language_code(lang_code):
    """
    For consistency always operate on language codes
    that are lowercase and use dashes as separators for
    composed language codes.

    Example: 'en_GB' -> 'en-gb'
    """
    return lang_code.lower().replace('_', '-')


def get_normalised_language():
    lang = get_language()
    if lang:
        return normalise_language_code(lang)
