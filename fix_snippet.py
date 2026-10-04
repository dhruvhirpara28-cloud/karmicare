with open('snippets/product-info-card.liquid', 'r') as f:
    text = f.read()

import re

# Update background color
text = re.sub(r'{% if block\.settings\.background_color != blank %}.*?{% endif %}',
              '''{% if block.settings.background_color_day != blank %}
      background-color: {{ block.settings.background_color_day }};
    {% endif %}''', text, flags=re.DOTALL)

# Add night mode override for background color
text = re.sub(r'(#ProductInfoCard-{{ block\.id }} {[\s\S]*?})',
              r'\1\n\n  body.night-mode #ProductInfoCard-{{ block.id }} {\n    {% if block.settings.background_color_night != blank %}background-color: {{ block.settings.background_color_night }};{% endif %}\n  }', text)

# Update header color
text = re.sub(r'color: {{ block\.settings\.header_color }};',
              'color: {{ block.settings.header_color_day }};', text)

# Add night mode override for header color
text = re.sub(r'(#ProductInfoCard-{{ block\.id }} \.product-info-card__header {[\s\S]*?})',
              r'\1\n\n  body.night-mode #ProductInfoCard-{{ block.id }} .product-info-card__header {\n    {% if block.settings.header_color_night != blank %}color: {{ block.settings.header_color_night }};{% endif %}\n  }', text)

with open('snippets/product-info-card.liquid', 'w') as f:
    f.write(text)
print('Done!')
