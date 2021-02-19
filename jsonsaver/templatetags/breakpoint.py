from django import template

from django_jsonsaver.server_config import SERVER_NAME

register = template.Library()


@register.simple_tag(takes_context=True)
def set_breakpoint(context):
    """
    Set breakpoints in the template for easy examination of the context.

    Usage:
        {% load breakpoint %}
        {% set_breakpoint %}
    """

    if SERVER_NAME == 'dev':
        breakpoint()
