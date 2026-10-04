with open('sections/main-product.liquid', 'r') as f:
    text = f.read()

import re
text = re.sub(r'{\s*\"type\":\s*\"color\",\s*\"id\":\s*\"background_color\",\s*\"label\":\s*\"Background Color\"\s*},', '''{
          "type": "color",
          "id": "background_color_day",
          "label": "Background Color (Day)"
        },
        {
          "type": "color",
          "id": "background_color_night",
          "label": "Background Color (Night)"
        },''', text)

text = re.sub(r'{\s*\"type\":\s*\"color\",\s*\"id\":\s*\"header_color\",\s*\"label\":\s*\"Header Text Color\"\s*},', '''{
          "type": "color",
          "id": "header_color_day",
          "label": "Header Text Color (Day)"
        },
        {
          "type": "color",
          "id": "header_color_night",
          "label": "Header Text Color (Night)"
        },''', text)

with open('sections/main-product.liquid', 'w') as f:
    f.write(text)
print('Done!')
