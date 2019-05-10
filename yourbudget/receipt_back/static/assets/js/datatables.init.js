function format (d) {
    // `d` is the original data object for the row
    d = d.list_of_purchases;

    var res = '<table class="display table table-striped table-bordered">';

    res = '<div class="card">' + res;

    res = res + '<tr>'
    + '<td>' + 'Product name' + '</td>'
    + '<td>' + 'Price' + '</td>'
    + '</tr>'
    var len = d.length;
    for (var i = 0; i < len; i++) {
        var x = d[i];
        res = res + '<tr>'
        + '<td>' + d[i].name_of_product + '</td>'
        + '<td>' + d[i].price + '</td>'
        + '</tr>';
    }
    res = res + '</table>';
    res = res + '</div>'
    return res;
}

$(document).ready(function() {
    var table = $('#table1').DataTable(
    {
            "ajax": 'all_trips_data',
            "columns": [
                {
                    "className":      'details-control',
                    "orderable":      false,
                    "data":           null,
                    "defaultContent": ''
                },
                {"data":"name_of_shop"},
                {"data":"trip_date"},
                {"data":"receipt_amount"},
                {"data":"receipt_discount"},
                {"data":"address"},
                {"data":"category"}
            ],
            "order": [[1, 'asc']]
    }
    );
     $('#table1 tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);


        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');

            // TODO fix button


//            var td = tr.children().first();
//
//
//            var i = document.createElement("i");
//            i.class = "lni-menu";
//            td.child(i).show();
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');

//            var td = tr.children().first();
//
//            var i = document.createElement("i");
//            i.class = "lni-menu";
//            td.appendChild(i);
        }
    } );
} );