from .forms import *


def custom_slugify(value, allow_unicode=False):
    import unicodedata, re

    """
    Modified from django.utils.text import slugify - so that uppercase are not converted to lowercase
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    DO NOT Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    #  The Regex removes any characters that are word characters (\w), whitespace characters (\s), or hyphens (-).
    # Then, it replaces any sequences of hyphens or whitespace characters with underscore.
    value = re.sub(r"[^\w\s&\-]", "", value).strip()
    return re.sub(r"[-\s]+", "_", value)
