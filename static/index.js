/**
 * Created by mitch on 12/15/15.
 */

(function () {
    var quotes = [];

    function extractName(imageSrc) {
        var pathParts = imageSrc.split('/');
        var filename = pathParts[pathParts.length - 1];
        var celebrityName = filename.split('.')[0];
        return celebrityName.replace(/_/g, ' ');
    }

    function setQuoteWithData(data) {
        var $quoteImage = $('#celebrityImage');
        var text = '"' + data.quote.trim() + '" - ' + extractName(data.image);
        $quoteImage.css('background-image', 'url(' + data.image + ')');
        $quoteImage.find('.overlayText').text(text);
    }

    function refresh() {
        $.get('/generate', function (data) {
            quotes.push(data);
            setQuoteWithData(data);
        });
    }

    $(document).ready(function () {
        $('#refreshButton').click(refresh);
        $(document).keypress(function (e) {
            if (e.which == 98) { // back
                if (quotes.length > 0) {
                    var quote = quotes.splice(quotes.length - 1, 1)[0];
                    setQuoteWithData(quote);
                }
            } else if (e.which == 32) { // space
                refresh();
            }
        });
        refresh();
    });
})();

