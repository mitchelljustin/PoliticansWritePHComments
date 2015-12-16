/**
 * Created by mitch on 12/15/15.
 */

function extractName(imageSrc) {
    var pathParts = imageSrc.split('/');

    return pathParts[pathParts.length - 1].split('.')[0].replace('_', ' ');
}

function refresh() {
    $.get('/image', function (imageSrc) {
        var $quoteImage = $('#celebrityImage');
        $quoteImage.css('background-image', 'url('+imageSrc+')');
        $.get('/gen_quote', function (quote) {
            var text = '"' + quote + '" - ' + extractName(imageSrc);
            $quoteImage.find('.overlayText').text(text);
        })
    });
}

$(document).ready(function () {
    $('#refreshButton').click(refresh);
    refresh();
});