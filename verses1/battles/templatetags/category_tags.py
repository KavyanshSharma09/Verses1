from django import template
from django.utils.safestring import mark_safe

register = template.Library()

CATEGORY_ICONS = {
    'arrays': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="3" y="3" width="5" height="5" rx="1"/>
        <rect x="10" y="3" width="5" height="5" rx="1"/>
        <rect x="17" y="3" width="5" height="5" rx="1"/>
    </svg>''',
    
    'strings': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M4 7V4h16v3"/>
        <path d="M9 20h6"/>
        <path d="M12 4v16"/>
    </svg>''',
    
    'math': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M4 12h6"/>
        <path d="M7 9v6"/>
        <path d="M14 9l6 6"/>
        <path d="M20 9l-6 6"/>
    </svg>''',
    
    'dynamic-programming': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="3" y="3" width="7" height="7" rx="1"/>
        <rect x="14" y="3" width="7" height="7" rx="1"/>
        <rect x="3" y="14" width="7" height="7" rx="1"/>
        <rect x="14" y="14" width="7" height="7" rx="1"/>
        <path d="M10 6.5h4" stroke-dasharray="2 2"/>
        <path d="M6.5 10v4" stroke-dasharray="2 2"/>
        <path d="M17.5 10v4" stroke-dasharray="2 2"/>
        <path d="M10 17.5h4" stroke-dasharray="2 2"/>
    </svg>''',
    
    'trees': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <circle cx="12" cy="5" r="3"/>
        <circle cx="6" cy="17" r="3"/>
        <circle cx="18" cy="17" r="3"/>
        <path d="M12 8v4"/>
        <path d="M12 12l-6 5"/>
        <path d="M12 12l6 5"/>
    </svg>''',
    
    'graphs': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <circle cx="5" cy="6" r="3"/>
        <circle cx="19" cy="6" r="3"/>
        <circle cx="5" cy="18" r="3"/>
        <circle cx="19" cy="18" r="3"/>
        <path d="M8 6h8"/>
        <path d="M5 9v6"/>
        <path d="M19 9v6"/>
        <path d="M8 18h8"/>
        <path d="M7 8l10 8"/>
    </svg>''',
    
    'linked-lists': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="2" y="9" width="5" height="6" rx="1"/>
        <rect x="10" y="9" width="5" height="6" rx="1"/>
        <rect x="18" y="9" width="5" height="6" rx="1"/>
        <path d="M7 12h3" marker-end="url(#arrow)"/>
        <path d="M15 12h3"/>
        <polygon points="9,10 11,12 9,14" fill="{color}"/>
        <polygon points="17,10 19,12 17,14" fill="{color}"/>
    </svg>''',
    
    'stack-queue': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="6" y="4" width="12" height="4" rx="1"/>
        <rect x="6" y="10" width="12" height="4" rx="1"/>
        <rect x="6" y="16" width="12" height="4" rx="1"/>
    </svg>''',
    
    'hash-table': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M4 9h16"/>
        <path d="M4 15h16"/>
        <path d="M10 3l-2 18"/>
        <path d="M16 3l-2 18"/>
    </svg>''',
    
    'recursion': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <path d="M12 3a9 9 0 1 0 9 9"/>
        <path d="M12 3a5 5 0 1 0 5 5"/>
        <polygon points="21,10 21,3 14,3" fill="{color}"/>
    </svg>''',
    
    'sorting': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="4" y="15" width="3" height="6" fill="{color}" opacity="0.3"/>
        <rect x="9" y="11" width="3" height="10" fill="{color}" opacity="0.3"/>
        <rect x="14" y="7" width="3" height="14" fill="{color}" opacity="0.3"/>
        <rect x="19" y="3" width="3" height="18" fill="{color}" opacity="0.3"/>
        <rect x="4" y="15" width="3" height="6" rx="0.5"/>
        <rect x="9" y="11" width="3" height="10" rx="0.5"/>
        <rect x="14" y="7" width="3" height="14" rx="0.5"/>
        <rect x="19" y="3" width="3" height="18" rx="0.5"/>
    </svg>''',
    
    'binary-search': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="2" y="10" width="20" height="4" rx="1"/>
        <path d="M12 6v4"/>
        <polygon points="10,6 12,3 14,6" fill="{color}"/>
        <path d="M12 14v4"/>
        <polygon points="10,18 12,21 14,18" fill="{color}"/>
        <line x1="7" y1="10" x2="7" y2="14" stroke-dasharray="0"/>
        <line x1="17" y1="10" x2="17" y2="14" stroke-dasharray="0"/>
    </svg>''',
    
    'two-pointers': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <rect x="2" y="10" width="20" height="4" rx="1"/>
        <polygon points="5,6 3,9 7,9" fill="{color}"/>
        <path d="M5 6v4"/>
        <polygon points="19,6 17,9 21,9" fill="{color}"/>
        <path d="M19 6v4"/>
        <path d="M8 12h2" stroke-dasharray="2 2"/>
        <path d="M14 12h2" stroke-dasharray="2 2"/>
    </svg>''',
    
    'greedy': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <circle cx="12" cy="12" r="9"/>
        <path d="M12 6v6l4 2"/>
        <circle cx="12" cy="12" r="2" fill="{color}"/>
    </svg>''',
    
    'bit-manipulation': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
        <text x="3" y="10" font-family="monospace" font-size="8" font-weight="bold" fill="{color}">1</text>
        <text x="9" y="10" font-family="monospace" font-size="8" font-weight="bold" fill="{color}">0</text>
        <text x="15" y="10" font-family="monospace" font-size="8" font-weight="bold" fill="{color}">1</text>
        <text x="3" y="18" font-family="monospace" font-size="8" font-weight="bold" fill="{color}">0</text>
        <text x="9" y="18" font-family="monospace" font-size="8" font-weight="bold" fill="{color}">1</text>
        <text x="15" y="18" font-family="monospace" font-size="8" font-weight="bold" fill="{color}">1</text>
        <path d="M20 7l-3 5 3 5"/>
    </svg>''',
}

# Default icon for unknown categories
DEFAULT_ICON = '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2">
    <circle cx="12" cy="12" r="10"/>
    <path d="M12 16v-4"/>
    <path d="M12 8h.01"/>
</svg>'''


@register.simple_tag
def category_icon(icon_name, size=18, color="currentColor"):
    """
    Render an SVG icon for a category.
    Usage: {% category_icon category.icon %} or {% category_icon category.icon size=24 color="#fff" %}
    """
    icon_template = CATEGORY_ICONS.get(icon_name, DEFAULT_ICON)
    svg = icon_template.format(size=size, color=color)
    return mark_safe(svg)


@register.inclusion_tag('battles/components/category_badge.html')
def category_badge(category, show_name=True, size=16):
    """
    Render a complete category badge with icon and optional name.
    Usage: {% category_badge category %} or {% category_badge category show_name=False %}
    """
    return {
        'category': category,
        'show_name': show_name,
        'size': size,
        'icon_svg': CATEGORY_ICONS.get(category.icon, DEFAULT_ICON).format(size=size, color=category.color)
    }
