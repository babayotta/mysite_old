$(document).ready(function () {

    $.ajax({
        url: 'api/',
        type: 'GET',
        data: {},
        success: function (table) {
            $('#table').html(table);
        }
    });

});
