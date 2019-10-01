$(document).ready(function () {

    $.get( 'api/', function (data) {
        $('#profits_total').append(data.profits_total);
        $('#previous_total_sum').append(data.previous_total_sum);
        $.each(data.profits, function (key, profit) {
            $.each(profit.transactions, function (key1, transaction) {
                $('#profits').append(
                    '<tr>'+
                    '<td>'+ profit.date +'</td>'+
                    '<td>'+ transaction.description +'</td>'+
                    '<td>'+ transaction.cash +'</td>'+
                    '</tr>'
                );
            });
        });
        $('#taxes_total').append(data.taxes_total);
        $.each(data.taxes, function (key, tax) {
            $.each(tax.transactions, function (key1, transaction) {
                $('#taxes').append(
                    '<tr>'+
                    '<td>'+ tax.date +'</td>'+
                    '<td>'+ transaction.description +'</td>'+
                    '<td>'+ transaction.cash +'</td>'+
                    '</tr>'
                );
            });
        });
        $('#buys_total').append(data.buys_total);
        $.each(data.buys, function (key, buy) {
            $.each(buy.transactions, function (key1, transaction) {
                $('#buys').append(
                    '<tr>'+
                    '<td>'+ buy.date +'</td>'+
                    '<td>'+ transaction.description +'</td>'+
                    '<td>'+ transaction.cash +'</td>'+
                    '<td>'+ buy.budget_for_day +'</td>'+
                    '<td>'+ buy.balance_for_day +'</td>'+
                    '</tr>'
                );
            });
        });
    });

});
