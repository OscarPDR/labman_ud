$('#expand-form-btn').click(function() {
    $(this).removeClass('hover');
    var buttonIcon = $(this).children('i');
    if(buttonIcon.hasClass('fa-plus')) {
        buttonIcon.removeClass('fa-plus').addClass('fa-minus');
        $('#extended-form-title, #extended-form-tabs, #extended-form').fadeIn();
    } else {
        buttonIcon.removeClass('fa-minus').addClass('fa-plus');
        $('#extended-form-title, #extended-form-tabs, #extended-form').fadeOut();
    }
});

$('#all-tab').click(function() {
    $('#extended-form-tabs li.active').removeClass('active');
    $(this).parent().addClass('active');
    $('.tab-pane').addClass('active');
});