"""Custom template helpers for the Velora storefront."""
from django import template

register = template.Library()


@register.filter(name="image_url")
def image_url(value):
    """Return the URL of an ImageFieldFile, or an empty string if no file is set.

    Using ``{{ product.image.url }}`` directly raises ``ValueError`` when a
    product has no uploaded image (the ``ImageFieldFile`` accessor checks for
    an associated file).  Templates should use ``{{ product|image_url }}`` and
    then default to the placeholder image.
    """
    if not value:
        return ""
    try:
        return value.url
    except (ValueError, AttributeError):
        return ""