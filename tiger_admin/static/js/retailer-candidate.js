function make_comment_editable(data_table) {
	$('[id*="comment|"]').editable('/retailer-candidate/update-comment/', {
		"callback": function(value, y) {
			var aPos = data_table.fnGetPosition(this);
			data_table.fnUpdate(value, aPos[0], aPos[1]);
			},
		"height": "20px",
		"placeholder" : "",
		"tooltip": "Click to edit"
    });
}

$(document).ready(function() {
    data_table = $('.mws-datatable-no-sort-first-column').dataTable({
        sPaginationType: 'full_numbers',
        'aoColumnDefs': [
           { 'bSortable': false, 'aTargets': [0] }
       ]
    });

	$('#datatable').on('draw.dt', function() {
        make_comment_editable(data_table);
    })

    make_comment_editable(data_table);
});

function getSelectedId() {
    var selected_radio = $('tbody input[type=radio]:checked');

    if (selected_radio.length > 0) return selected_radio.val();
    return false;
}

if (typeof reject_ajax !== undefined) {

function reject() {
    var checked_id = getSelectedId();
    if (checked_id === false) {
        alert('No candidate is selected');
        return;
    };

    var params = {candidate_id: checked_id};
    $.post(reject_ajax, params, function(data) {
        if (data) {
            alert(data);
        }
        else {
            location.reload(true);
        }
    });
}

}

if (typeof register_url !== undefined) {

function register() {
    var checked_id = getSelectedId();
    if (checked_id === false) {
        alert('No candidate is selected');
        return;
    };

    window.location = register_url + '?cid=' + checked_id;
}

}

if (typeof mark_as_pending_ajax !== undefined) {

function mark_as_pending() {
    var checked_id = getSelectedId();
    if (checked_id === false) {
        alert('No candidate is selected');
        return;
    };

    var params = {candidate_id: checked_id};
    $.post(mark_as_pending_ajax, params, function(data) {
        if (data) {
            alert(data);
        }
        else {
            location.reload(true);
        }
    });
}

}
