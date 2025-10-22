from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css):
    """
    Usage: {{ form.username|add_class:"input is-medium" }}
    Adds/extends the CSS class on a form field widget without removing existing ones.
    """
    try:
        existing = field.field.widget.attrs.get("class", "")
        new_class = f"{existing} {css}".strip()
        attrs = field.field.widget.attrs.copy()
        attrs["class"] = new_class
        return field.as_widget(attrs=attrs)
    except Exception:
        # If anything fails, gracefully return the field as-is
        return field


@register.filter(name="add_attr")
def add_attr(field, arg):
    """
    Usage: {{ form.username|add_attr:"placeholder:Your username" }}
    Adds/overrides a single attribute (key:value) on the field widget.
    """
    try:
        key, value = arg.split(":", 1)
        attrs = field.field.widget.attrs.copy()
        attrs[key] = value
        return field.as_widget(attrs=attrs)
    except Exception:
        return field
