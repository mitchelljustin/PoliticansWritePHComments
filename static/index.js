/**
 * Created by mitch on 12/15/15.
 */

function extractName(imageSrc) {
    var pathParts = imageSrc.split('/');
    var filename = pathParts[pathParts.length - 1];
    var celebrityName = filename.split('.')[0];
    return celebrityName.replace(/_/g, ' ');
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
    $(document).keypress(refresh);
    refresh();
});