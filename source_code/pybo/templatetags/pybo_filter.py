from django import template
from django.utils.safestring import mark_safe
from html import escape
import markdown
import re

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def mark(value):
    extensions = ['nl2br', 'fenced_code']
    html = markdown.markdown(value, extensions=extensions)
    html = re.sub(
        r'<pre><code class="language-([^"]+)">(.*?)</code></pre>',
        _code_block_with_label,
        html,
        flags=re.DOTALL,
    )
    return mark_safe(html)


def _code_block_with_label(match):
    language = escape(match.group(1))
    code = match.group(2)
    return (
        '<div class="code-section">'
        '<div class="code-section-label">{}</div>'
        '<pre><code class="language-{}">{}</code></pre>'
        '</div>'
    ).format(language, language, code)
