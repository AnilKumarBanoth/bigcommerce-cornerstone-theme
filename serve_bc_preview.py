import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

PORT = 8099

PRODUCTS = [
    {
        "id": 101,
        "name": "Womens Knit Cardigan",
        "price": "$205.40",
        "url": "/womens-knit-cardigan/",
        "brand": "Apparel Co",
        "swatches": [
            {"id": "s1", "label": "Natural White", "color": "f5f5dc", "image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=500&q=80"},
            {"id": "s2", "label": "Sage Green", "color": "a2b9a0", "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=500&q=80"},
            {"id": "s3", "label": "Baby Blue", "color": "9bb7d4", "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=500&q=80"},
            {"id": "s4", "label": "Dusty Rose", "color": "d4a5a5", "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=500&q=80"}
        ]
    },
    {
        "id": 102,
        "name": "Classic Oxford Button-Down",
        "price": "$68.00",
        "url": "/classic-oxford-shirt/",
        "brand": "Cornerstone Outfitters",
        "swatches": [
            {"id": "s5", "label": "Sky Blue", "color": "87ceeb", "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=500&q=80"},
            {"id": "s6", "label": "Crisp White", "color": "ffffff", "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=500&q=80"},
            {"id": "s7", "label": "French Navy", "color": "1e293b", "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=500&q=80"}
        ]
    },
    {
        "id": 103,
        "name": "Everyday Slim Chino Pants",
        "price": "$85.00",
        "url": "/everyday-slim-chino/",
        "brand": "Cornerstone Outfitters",
        "swatches": [
            {"id": "s8", "label": "Khaki Tan", "color": "c2b280", "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=500&q=80"},
            {"id": "s9", "label": "Olive Drab", "color": "556b2f", "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=500&q=80"},
            {"id": "s10", "label": "Charcoal Grey", "color": "36454f", "image": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=500&q=80"}
        ]
    },
    {
        "id": 104,
        "name": "Canvas Low-Top Sneaker",
        "price": "$55.00",
        "url": "/canvas-low-top-sneaker/",
        "brand": "Apparel Co",
        "swatches": [
            {"id": "s11", "label": "Triple White", "color": "f8f8f8", "image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=500&q=80"},
            {"id": "s12", "label": "Burgundy Red", "color": "800020", "image": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=500&q=80"},
            {"id": "s13", "label": "Jet Black", "color": "111111", "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=500&q=80"}
        ]
    }
]

def render_html():
    cards_html = ""
    for p in PRODUCTS:
        first_img = p['swatches'][0]['image']
        swatches_html = "".join([
            f'<button type="button" class="card-swatch-option{" is-active" if i == 0 else ""}" '
            f'data-product-id="{p["id"]}" data-swatch-id="{s["id"]}" data-swatch-label="{s["label"]}" '
            f'data-image="{s["image"]}" title="{s["label"]}" style="background-color: #{s["color"]};">'
            f'</button>'
            for i, s in enumerate(p['swatches'])
        ])

        cards_html += f"""
        <article class="card" data-entity-id="{p['id']}">
            <figure class="card-figure">
                <a href="{p['url']}" class="card-figure__link">
                    <div class="card-img-container">
                        <img class="card-image" id="img_{p['id']}" src="{first_img}" alt="{p['name']}">
                    </div>
                </a>
            </figure>
            <div class="card-body">
                <p class="card-text card-brand">{p['brand']}</p>
                <h3 class="card-title">
                    <a href="{p['url']}">{p['name']}</a>
                </h3>
                <div class="card-text card-price">{p['price']}</div>

                <!-- Stencil Util-API Swatches Container -->
                <div class="card-swatches-container" data-card-swatches data-product-id="{p['id']}">
                    <div class="card-swatches">
                        {swatches_html}
                    </div>
                </div>

                <div class="card-actions">
                    <button class="button button--small button--primary">Choose Options</button>
                </div>
            </div>
        </article>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shop All – cttest-anilkumar | BigCommerce Cornerstone Theme</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karla:wght@400;700&family=Montserrat:wght@400;600;700&display=swap">
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Karla', Arial, Helvetica, sans-serif;
      margin: 0;
      background: #fff;
      color: #333;
    }}
    .announcement-bar {{
      background: #333;
      color: #fff;
      text-align: center;
      padding: 10px;
      font-size: 13px;
    }}
    .header {{
      border-bottom: 1px solid #e5e5e5;
      padding: 20px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .header-logo {{
      font-family: 'Montserrat', sans-serif;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
    }}
    .header-nav a {{
      color: #555;
      text-decoration: none;
      margin-left: 24px;
      font-size: 14px;
      font-weight: 600;
    }}
    .header-nav a.active {{
      color: #4b7189;
      border-bottom: 2px solid #4b7189;
      padding-bottom: 4px;
    }}
    .page-container {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 40px 24px 80px;
    }}
    .category-header {{
      margin-bottom: 30px;
      text-align: center;
    }}
    .category-header h1 {{
      font-family: 'Montserrat', sans-serif;
      font-size: 32px;
      margin: 0 0 10px;
      font-weight: 700;
    }}
    .category-header p {{
      color: #666;
      font-size: 15px;
      margin: 0 auto;
      max-width: 600px;
    }}
    .status-badge {{
      display: inline-block;
      background: #e0f2fe;
      color: #0369a1;
      padding: 4px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    .productGrid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 30px;
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    @media (max-width: 1024px) {{
      .productGrid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 600px) {{
      .productGrid {{ grid-template-columns: 1fr; }}
    }}
    .card {{
      border: 1px solid #e5e5e5;
      border-radius: 4px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      background: #fff;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .card:hover {{
      border-color: #4b7189;
      box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }}
    .card-figure {{
      margin: 0;
      position: relative;
      background: #f4f4f4;
      aspect-ratio: 1/1;
      overflow: hidden;
    }}
    .card-img-container {{
      width: 100%;
      height: 100%;
    }}
    .card-image {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.3s ease, opacity 0.2s ease;
    }}
    .card:hover .card-image {{
      transform: scale(1.05);
    }}
    .card-body {{
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }}
    .card-brand {{
      color: #888;
      font-size: 12px;
      margin: 0 0 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .card-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 15px;
      margin: 0 0 8px;
      font-weight: 600;
      line-height: 1.35;
    }}
    .card-title a {{
      color: #333;
      text-decoration: none;
    }}
    .card-title a:hover {{
      color: #4b7189;
    }}
    .card-price {{
      font-weight: 700;
      font-size: 16px;
      color: #222;
      margin-bottom: 12px;
    }}
    /* Card Swatches Styling matching BigCommerce Cornerstone */
    .card-swatches-container {{
      margin-top: 4px;
      margin-bottom: 14px;
      min-height: 26px;
    }}
    .card-swatches {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }}
    .card-swatch-option {{
      width: 22px;
      height: 22px;
      border-radius: 50%;
      border: 1px solid #ccc;
      cursor: pointer;
      padding: 0;
      background-size: cover;
      background-position: center;
      transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
      outline: none;
    }}
    .card-swatch-option:hover {{
      transform: scale(1.25);
      border-color: #333;
    }}
    .card-swatch-option.is-active {{
      border: 2px solid #333;
      box-shadow: 0 0 0 2px #fff inset;
    }}
    .card-actions {{
      margin-top: auto;
    }}
    .button {{
      display: block;
      width: 100%;
      text-align: center;
      padding: 9px 16px;
      font-size: 13px;
      font-weight: 600;
      border: 1px solid #4b7189;
      background: #4b7189;
      color: #fff;
      border-radius: 3px;
      cursor: pointer;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      transition: background 0.2s;
    }}
    .button:hover {{
      background: #3a576a;
    }}
  </style>
</head>
<body>
  <div class="announcement-bar">
    BigCommerce Cornerstone Light Theme &bull; Stencil Util-API Product Color Swatches Demo
  </div>

  <header class="header">
    <div class="header-logo">Cornerstone</div>
    <nav class="header-nav">
      <a href="/">Home</a>
      <a href="/shop-all/" class="active">Shop All (/shop-all/)</a>
      <a href="/apparel/">Apparel</a>
    </nav>
  </header>

  <main class="page-container">
    <div class="category-header">
      <div class="status-badge">Stencil Util-API Active</div>
      <h1>Shop All Apparel</h1>
      <p>Product color swatches loaded on listing pages via Stencil Util-API. Click or hover any color swatch to dynamically swap the product picture.</p>
    </div>

    <div class="productGrid">
      {cards_html}
    </div>
  </main>

  <script>
    // Stencil Util-API Swatch Interaction Handler
    document.querySelectorAll('.card-swatch-option').forEach(function(swatch) {{
      swatch.addEventListener('click', function(e) {{
        e.preventDefault();
        var productId = this.getAttribute('data-product-id');
        var newImg = this.getAttribute('data-image');
        var colorLabel = this.getAttribute('data-swatch-label');
        
        // Toggle active class among siblings
        var siblings = this.parentElement.querySelectorAll('.card-swatch-option');
        siblings.forEach(function(s) {{ s.classList.remove('is-active'); }});
        this.classList.add('is-active');

        // Dynamically update product card image
        var imgEl = document.getElementById('img_' + productId);
        if (imgEl && newImg) {{
          imgEl.style.opacity = '0.5';
          setTimeout(function() {{
            imgEl.src = newImg;
            imgEl.style.opacity = '1';
          }}, 150);
        }}
      }});
    }});
  </script>
</body>
</html>
"""

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        html = render_html()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), RequestHandler)
    print(f"BigCommerce Stencil Preview Server running at http://127.0.0.1:{PORT}/shop-all/")
    server.serve_forever()
