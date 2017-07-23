$(document).ready(function () {

    $('.btn-toggle-up').click(function () {
        if($(this).attr('class').search('collapsed') === -1) {
            $(this).css("transform", "rotate(180deg)");
        } else {
            $(this).css("transform", "rotate(360deg)");
        }
    });

    $('div.list').click(function () {
        $(this).prev().children().click();
    });

});
