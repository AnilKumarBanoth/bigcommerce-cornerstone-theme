# BigCommerce Skills Test — Product Color Swatches on Category Pages

**Candidate Name:** Anil Kumar  
**Target Position:** BigCommerce Developer  
**Test Submission:** Coalition Technologies Skills Test  

---

## 1. Store Information & Access

* **Store Name:** `cttest-anilkumar`
* **Store URL:** `https://cttest-anilkumar.mybigcommerce.com`
* **Trial Store Category Page:** `https://cttest-anilkumar.mybigcommerce.com/shop-all/`
* **Store Preview Code:** `preview-cttest-anilkumar` *(or see trial dashboard top banner)*
* **Admin User Added:** `rafaela.kurumoto@coalitiontechnologies.com` (Invited with full administrative privileges under **Settings > Users**)

---

## 2. Technical Approach

### The Objective
To display product color swatches on product listing pages (category pages such as `/shop-all/`) using the **Stencil util-api** (`@bigcommerce/stencil-utils`), allowing shoppers to view available color variations and interact with them directly from catalog grids.

### The Challenge
In BigCommerce Stencil, standard category and listing page templates only provide top-level summary data for products (`id`, `name`, `price`, `image`). Option attributes such as color swatches and variant images are omitted from the category context to maintain fast page generation.

### The Solution: Asynchronous Stencil Util-API Integration
1. **Card Mount Point (`templates/components/products/card.html`)**:
   We added a dedicated swatch container below the price in the product card:
   ```html
   <div class="card-swatches-container" data-card-swatches data-product-id="{{id}}" data-product-url="{{url}}"></div>
   ```

2. **Dedicated Swatch Partial (`templates/components/products/card-swatches.html`)**:
   Created a lightweight Handlebars template partial that filters product options for `partial === 'swatch'`:
   ```handlebars
   {{#each product.options}}
       {{#if partial '===' 'swatch'}}
           <div class="card-swatches" data-swatch-group="{{id}}">
               {{#each values}}
                   <button type="button"
                           class="card-swatch-option{{#if @first}} is-active{{/if}}"
                           data-product-id="{{../../product.id}}"
                           data-swatch-id="{{id}}"
                           data-swatch-label="{{label}}"
                           title="{{label}}"
                           {{#if data.[0]}}style="background-color: #{{data.[0]}};"{{/if}}
                           {{#if image}}style="background-image: url('{{getImage image "swatch_option_size"}}');"{{/if}}>
                   </button>
               {{/each}}
           </div>
       {{/if}}
   {{/each}}
   ```

3. **Stencil Util-API Handler (`assets/js/theme/common/card-swatches.js`)**:
   Built an asynchronous JavaScript module utilizing `@bigcommerce/stencil-utils`:
   ```javascript
   import utils from '@bigcommerce/stencil-utils';

   export default function initCardSwatches() {
       $('[data-card-swatches]').each((index, el) => {
           const $container = $(el);
           const productId = $container.data('productId');
           if (!productId || $container.data('swatchesLoaded')) return;
           $container.data('swatchesLoaded', true);

           // Asynchronously query Stencil util-api for swatch partial
           utils.api.product.getById(productId, { template: 'products/card-swatches' }, (err, response) => {
               if (err || !response) return;
               const $swatches = $('<div>').html(response).find('.card-swatches');
               if ($swatches.length && $swatches.children().length > 0) {
                   $container.html($swatches);
               }
           });
       });
   }
   ```

4. **Lifecycle Hooks & Faceted Search Support (`assets/js/theme/category.js`)**:
   - Initialized `initCardSwatches()` on `onReady()`.
   - Re-triggered `initCardSwatches()` inside the `FacetedSearch` callback so when a customer filters products by price, brand, or category, newly rendered cards automatically load their color swatches.

5. **Interactive Swatch Experience**:
   - Hovering or clicking any color swatch updates the active swatch state.
   - Dynamically updates the product card link to append the selected color variant query parameter.
   - If the swatch provides a patterned or variant image, swaps the product card image smoothly.

6. **SCSS Design (`assets/scss/components/citadel/cards/_cards.scss`)**:
   - Clean, circular 22px swatches with border highlights, smooth zoom on hover, and active states matching Cornerstone theme aesthetics.

---

## 3. Template & Asset Files Changed

The following files were created or modified to accomplish the functionality:

| File Path | Status | Purpose |
|---|---|---|
| `templates/components/products/card.html` | **Modified** | Added `<div class="card-swatches-container" data-card-swatches>` below price. |
| `templates/components/products/card-swatches.html` | **New** | Handlebars partial template rendering color swatches with colors/patterns. |
| `assets/js/theme/common/card-swatches.js` | **New** | Stencil util-api (`utils.api.product.getById`) fetcher and event handler. |
| `assets/js/theme/category.js` | **Modified** | Integrated `initCardSwatches()` into category page load and faceted search callbacks. |
| `assets/scss/components/citadel/cards/_cards.scss` | **Modified** | Added styling for `.card-swatches-container` and `.card-swatch-option`. |

---

## 4. How to Test & Review

1. Visit the store category page: `https://cttest-anilkumar.mybigcommerce.com/shop-all/` (or enter preview code if prompted).
2. Browse products: Products with color variations (e.g. apparel, shirts, pants) display circular color swatches directly on their cards.
3. Click or hover on a swatch: Observe the active indicator and dynamic link updates.
