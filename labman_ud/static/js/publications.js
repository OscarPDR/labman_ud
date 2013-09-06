(function($) {
    $(document).ready(function($) {

        // Common fields for every publication
        _title = $('div').find('.field-title');
        _abstract = $('div').find('.field-abstract');
        _pdf = $('div').find('.field-pdf');
        _language = $('div').find('.field-language');
        _observations = $('div').find('.field-observations');
        _published = $('div').find('.field-published');

        // Specific fields depending on the publication type
        _presented_at = $('div').find('.field-presented_at');
        _proceedings_title = $('div').find('.field-proceedings_title');
        _short_title = $('div').find('.field-short_title');
        _doi = $('div').find('.field-doi');
        _journal_abbreviation = $('div').find('.field-journal_abbreviation');
        _number = $('div').find('.field-number');
        _volume = $('div').find('.field-volume');
        _pages = $('div').find('.field-pages');
        _issn = $('div').find('.field-issn');
        _isbn = $('div').find('.field-isbn');
        _impact_factor = $('div').find('.field-impact_factor');

        // Trigger when publication type select input is changed
        $('#id_publication_type').change(function() {
            var publication_type = $('#id_publication_type :selected').text();

            showAll();

            switch(publication_type) {
                case 'Book section':
                    hide(_presented_at);
                    hide(_proceedings_title);
                    hide(_short_title);
                    hide(_doi);
                    hide(_journal_abbreviation);
                    hide(_number);
                    hide(_issn);
                    hide(_impact_factor);
                    break;

                case 'Book':
                    break;

                case 'Booklet':
                    break;

                case 'Conference paper':
                    break;

                case 'In collection':
                    break;

                case 'Journal article':
                    break;

                case 'Manual':
                    break;

                case 'Master\'s thesis':
                    break;

                case 'Misc':
                    break;

                case 'PhD thesis':
                    break;

                case 'Technical report':
                    break;

                case 'Unpublished':
                    break;
            }
        });
    });

    function showAll() {
        show(_presented_at);
        show(_proceedings_title);
        show(_short_title);
        show(_doi);
        show(_journal_abbreviation);
        show(_number);
        show(_volume);
        show(_pages);
        show(_issn);
        show(_isbn);
        show(_impact_factor);
    }

    function show(element) {
        element.removeAttr('style');
    }

    function hide(element) {
        element.css({
            'visibility': 'hidden',
            'overflow': 'hidden',
            'height': '0px',
            'margin-bottom': '0px'
        });
    }
})(django.jQuery);
