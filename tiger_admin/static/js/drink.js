$(document).ready(function() {
    $('.mws-datatable-no-sort-first-column').dataTable({
        sPaginationType: 'full_numbers',
        aaSorting: [[1, "desc"]],
        aoColumnDefs: [
           { 'bSortable': false, 'aTargets': [0] }
       ]
    });
    
    $('.mws-datatable-sort-first-column').dataTable({
        sPaginationType: 'full_numbers',
        aaSorting: [[0, "desc"]]
    });

	$(".mws-dtpicker").datetimepicker({});

    $('thead input:checkbox').click(function(event) {
        var self = this;

        $('tbody input:checkbox').each(function() {
            this.checked = self.checked;
        });
    });
});

function getSelectedIds() {
    var checked_checkboxes = $('tbody input:checkbox:checked');

    var checked_ids = $.map(checked_checkboxes, function(checkbox) {
        return checkbox.value;
    });

    return checked_ids;
}

if (typeof drink_approve_ajax !== undefined) {

function approve() {
    var checked_ids = getSelectedIds();
    if (checked_ids.length == 0) {
        alert('No order is selected');
        return;
    };

    var params = {order_ids: checked_ids,
                  csrfmiddlewaretoken: $.cookie('csrftoken')
                  };
    $.post(drink_approve_ajax, params, function(data) {
        if (data) {
            alert(data);
        }
        else {
            location.reload(true);
        }
    });
}

}

if (typeof drink_reject_ajax !== undefined) {

function reject() {
    if (! confirm('Do you want to refund this order?')) {
        return;
    }

    var checked_ids = getSelectedIds();
    if (checked_ids.length == 0) {
        alert('No order is selected');
        return false;
    };

    var params = {order_ids: checked_ids,
                  csrfmiddlewaretoken: $.cookie('csrftoken')
                  };

    $.post(drink_reject_ajax, params, function(data) {
        if (data) {
            alert(data);
        }
        else {
            location.reload(true);
        }
    });
}

}

if (typeof drink_mark_delivered_ajax !== undefined) {

function mark_delivered() {
    var checked_ids = getSelectedIds();
    if (checked_ids.length == 0) {
        alert('No order is selected');
        return;
    };

    var params = {order_ids: checked_ids,
                  csrfmiddlewaretoken: $.cookie('csrftoken')
                  };
    $.post(drink_mark_delivered_ajax, params, function(data) {
        if (data) {
            alert(data);
        }
        else {
            location.reload(true);
        }
    });
}

}

if (typeof drink_cancel_ajax !== undefined) {

function cancel() {
    if (! confirm('Do you want to refund this order?')) {
        return;
    }

    var checked_ids = getSelectedIds();
    if (checked_ids.length == 0) {
        alert('No order is selected');
        return;
    };

    var params = {order_ids: checked_ids,
                  csrfmiddlewaretoken: $.cookie('csrftoken')
                  };
    $.post(drink_cancel_ajax, params, function(data) {
        if (data) {
            alert(data);
        }
        else {
            location.reload(true);
        }
    });
}

}

if (typeof drink_mark_processed_ajax !== undefined) {

function mark_processed() {
    var checked_ids = getSelectedIds();
    if (checked_ids.length == 0) {
        alert('No order is selected');
        return;
    };

    var params = {order_ids: checked_ids,
                  csrfmiddlewaretoken: $.cookie('csrftoken')
                  };
    $.post(drink_mark_processed_ajax, params, function(data) {
        if (data) {
            alert(data);
        }
        else {
            location.reload(true);
        }
    });
}

}

if (typeof new_ajax !== undefined) {

function load_new_orders_content(skip_push_state) {
    if (typeof skip_push_state === undefined) {
       skip_push_state = false;
    }

    $.get(new_ajax, function(data) {
        if (data) {
            $('div#mws-container div.container').html(data);
            if (! skip_push_state) {
                window.history.pushState('new', '', new_url);
                console.log('Push stage: new');
            }
        }
        else {
            alert('Not able to load!');
        }
    });
}

}

if (typeof processed_ajax !== undefined) {

function load_processed_content(skip_push_state) {
    if (typeof skip_push_state === undefined) {
       skip_push_state = false;
    }

    $.get(processed_ajax, function(data) {
        if (data) {
            $('div#mws-container div.container').html(data);
            if (! skip_push_state) {
                console.log('Push stage: processed');
                window.history.pushState('processed', '', processed_url);
            }
        }
        else {
            alert('Not able to load!');
        }
    });
}

}

if (typeof delivered_ajax !== undefined) {

function load_delivered_content(skip_push_state) {
    if (typeof skip_push_state === undefined) {
       skip_push_state = false;
    }

    $.get(delivered_ajax, function(data) {
        if (data) {
            $('div#mws-container div.container').html(data);
            if (! skip_push_state) {
                console.log('Push stage: delivered');
                window.history.pushState('delivered', '', delivered_url);
            }
        }
        else {
            alert('Not able to load!');
        }
    });
}

}

if (typeof refunded_ajax !== undefined) {

function load_refunded_content(skip_push_state) {
    if (typeof skip_push_state === undefined) {
       skip_push_state = false;
    }

    $.get(refunded_ajax, function(data) {
        if (data) {
            $('div#mws-container div.container').html(data);
            if (! skip_push_state) {
                console.log('Push stage: refunded');
                window.history.pushState('refunded', '', refunded_url);
            }
        }
        else {
            alert('Not able to load!');
        }
    });
}

}


window.onpopstate = function(event) {
    if (window.location.href.indexOf('new') > 0) {
        load_new_orders_content(true);
    }
    else if (window.location.href.indexOf('processed') > 0) {
        load_processed_content(true);
    }
    else if (window.location.href.indexOf('delivered') > 0) {
        load_delivered_content(true);
    }
    else if (window.location.href.indexOf('refunded') > 0) {
        load_refunded_content(true);
    }
};

if (typeof processed_csv_url !== undefined) {

function processed_csv() {
    var product = $('#order-search-form input[type=text]').eq(0).val();
    var from_date = $('#order-search-form input[type=text]').eq(1).val();
    var to_date = $('#order-search-form input[type=text]').eq(2).val();
    
    var csv_url = processed_csv_url + '?product=' +
                  encodeURIComponent(product) + '&from_date=' +
                  encodeURIComponent(from_date) + '&to_date=' +
                  encodeURIComponent(to_date);

    window.open(csv_url, '_blank');
}

}

if (typeof delivered_csv_url !== undefined) {

function delivered_csv() {
    var product = $('#order-search-form input[type=text]').eq(0).val();
    var from_date = $('#order-search-form input[type=text]').eq(1).val();
    var to_date = $('#order-search-form input[type=text]').eq(2).val();
    
    var csv_url = delivered_csv_url + '?product=' +
                  encodeURIComponent(product) + '&from_date=' +
                  encodeURIComponent(from_date) + '&to_date=' +
                  encodeURIComponent(to_date);

    window.open(csv_url, '_blank');
}

}

if (typeof processed_csv_for_deliverer_url !== undefined) {

function processed_csv_for_deliverer() {
    var product = $('#order-search-form input[type=text]').eq(0).val();
    var from_date = $('#order-search-form input[type=text]').eq(1).val();
    var to_date = $('#order-search-form input[type=text]').eq(2).val();
    
    var csv_url = processed_csv_for_deliverer_url + '?product=' +
                  encodeURIComponent(product) + '&from_date=' +
                  encodeURIComponent(from_date) + '&to_date=' +
                  encodeURIComponent(to_date);

    window.open(csv_url, '_blank');
}

}

if (typeof detailed_csv_url !== undefined) {

function detailed_csv() {
    var product = $('#summary-filter-form input[type=text]').eq(0).val();
    var status = $('#summary-filter-form select :selected').val();
    var from_date = $('#summary-filter-form input[type=text]').eq(1).val();
    var to_date = $('#summary-filter-form input[type=text]').eq(2).val();
    var csv_url = detailed_csv_url + '?product=' +
                  encodeURIComponent(product) + '&status=' +
                  encodeURIComponent(status) + '&from_date=' +
                  encodeURIComponent(from_date) + '&to_date=' +
                  encodeURIComponent(to_date);
    window.open(csv_url, '_blank');
}

}

if (typeof summary_csv_url !== undefined) {

function summary_csv() {
    var product = $('#summary-filter-form input[type=text]').eq(0).val();
    var status = $('#summary-filter-form select :selected').val();
    var from_date = $('#summary-filter-form input[type=text]').eq(1).val();
    var to_date = $('#summary-filter-form input[type=text]').eq(2).val();
    var csv_url = summary_csv_url + '?product=' +
                  encodeURIComponent(product) + '&status=' +
                  encodeURIComponent(status) + '&from_date=' +
                  encodeURIComponent(from_date) + '&to_date=' +
                  encodeURIComponent(to_date);
    window.open(csv_url, '_blank');
}

}

