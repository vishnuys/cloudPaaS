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

$('#create-job').on('click', function(event) {
	var jobname = $('#jobname').val();
	var datatype = $('input[name=datatype]:checked').val();
	var colname = $('#colname').val();
	if (datatype == 'static') {
		var formData = new FormData();
		formData.append('file', $('#file-doc')[0].files[0], $('#file-doc')[0].files[0].name);
		formData.append('jobname', jobname);
		formData.append('datatype', datatype);
		formData.append('serviceslist', JSON.stringify(servicesList));
		formData.append('colname', colname);
		$.ajax({
			method: 'POST',
			url: '',
			data: formData,
			cache: false,
			contentType: false,
			mimeType: 'multipart/form-data',
			processData: false,
			success: function(data) {
				location.reload()
			}
		})
	}
});