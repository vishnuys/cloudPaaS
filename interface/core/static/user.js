var servicesList = [];

$('#file-doc').change(function() {
	$('#file-name').val($('#file-doc')[0].files[0].name);
});

function showrealtime() {
	$('#static-group').slideUp();
	$('#realtime-group').slideDown();
}

function showstatic() {
	$('#realtime-group').slideUp();
	$('#static-group').slideDown();
}

/* <span class="badge badge-pill badge-secondary">1 - Processing</span>
<span class="badge badge-pill badge-secondary">2 - Analytics</span>
<span class="badge badge-pill badge-secondary">3 - Storage</span>
*/

function serviceChecked(item) {
	if (servicesList.includes(item)) {
		let i = servicesList.indexOf(item)
		servicesList.splice(i, 1);
	}
	else {
		servicesList.push(item);
	}
	$('#order-field').html('');
	for(var i in servicesList) {
		$('#order-field').append('<span class="badge badge-pill badge-secondary ml-1">' + (parseInt(i)+1) + ' - ' + servicesList[i]  + '</span>')
	}
}