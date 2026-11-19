import utils from '@bigcommerce/stencil-utils';

/**
 * Initializes color swatches on product listing cards using Stencil utils.api.product.getById
 */
export default function initCardSwatches() {
    const $swatchContainers = $('[data-card-swatches]');

    $swatchContainers.each((index, el) => {
        const $container = $(el);
        const productId = $container.data('productId');

        if (!productId || $container.data('swatchesLoaded')) {
            return;
        }

        $container.data('swatchesLoaded', true);

        // Fetch product options using Stencil utils API
        utils.api.product.getById(productId, { template: 'products/card-swatches' }, (err, response) => {
            if (err || !response) {
                return;
            }

            const $parsed = $('<div>').html(response);
            const $swatches = $parsed.find('.card-swatches');

            if ($swatches.length && $swatches.children().length > 0) {
                $container.html($swatches);
            }
        });
    });

    // Delegate swatch click event
    $('body').off('click', '.card-swatch-option').on('click', '.card-swatch-option', function (e) {
        e.preventDefault();
        e.stopPropagation();

        const $swatch = $(this);
        const $card = $swatch.closest('.card');
        const productId = $swatch.data('productId');
        const swatchId = $swatch.data('swatchId');
        const swatchLabel = $swatch.data('swatchLabel');

        $swatch.siblings().removeClass('is-active');
        $swatch.addClass('is-active');

        // Update product card link with selected attribute
        const $cardLink = $card.find('.card-figure__link, .card-title a');
        if ($cardLink.length) {
            const originalUrl = $card.find('[data-card-swatches]').data('productUrl') || $cardLink.first().attr('href');
            const separator = originalUrl.indexOf('?') !== -1 ? '&' : '?';
            $cardLink.attr('href', `${originalUrl}${separator}color=${encodeURIComponent(swatchLabel)}`);
        }

        // If swatch has background image pattern or variant image, swap card image
        const bgImage = $swatch.css('background-image');
        if (bgImage && bgImage !== 'none') {
            const cleanUrl = bgImage.replace(/^url\(["']?/, '').replace(/["']?\)$/, '');
            const $cardImg = $card.find('.card-image');
            if ($cardImg.length) {
                $cardImg.attr('src', cleanUrl);
                $cardImg.attr('srcset', cleanUrl);
            }
        }
    });
}
