$(document).ready(function() {
	var table = $('#admin_table').DataTable();

	$("#weekSelect").html(getWeeks(new Date()));

	$("#weekSelect").change(function (e) {
		var week = document.getElementById('weekSelect').value;
		var dataString = "time_period=" + week;
		sendWeekAjax(dataString, '/retrieveAdminTable');
	});
	$("#weekSelect").trigger('change');

	$('#admin_table tbody').on( 'click', 'tr', function () {
		var week = document.getElementById('weekSelect').value;

		var data = {
			'time_period': week,
			'username': $(this).attr('id')
		};

		if ($(':nth-child(3)', this).html() == "false" || $(':nth-child(4)', this).html() == "false") {
			$('#approve').hide();
		} else {
			$('#approve').show();
		}

 		$('.modal-title').html($(this).attr('id'));
		sendTimesheetAjax(data, '/retrieveTimesheet');
    });

    $('#approve').click(function (e) {
    	data = {
    		'time_period': document.getElementById('weekSelect').value,
    		'username': $('.modal-title').html()
    	}

    	$.ajax({
			type: "POST",
			url: "/approveTimesheet",
			data: data,
			cache: false,
			success: function(result) {
				$("#weekSelect").trigger('change');
				$('#timesheet_modal').modal('hide');
			}
		});
    });
});

function getWeeks(d) {
	var weeks = [];
	var d = new Date(d);
	var day = d.getDay();
	var diff = d.getDate() - day;
	weeks.push(new Date(d.setDate(diff)));
	for (var i = 0; i < 4; i++) {
		var d = new Date(d);
		var day = d.getDay();
		var diff = d.getDate() - day - 7;
		weeks.push(new Date(d.setDate(diff)));
	}

	var selectString = "";
	weeks.forEach(function (day) {
		day = day.toString();
		day = day.split(" ");
		selectString += "<option value='" + day[1] + " " + day[2] + ", " + day[3] + "'>" + day[1] + " " + day[2] + ", " + day[3] + "</option>";
	});
	return selectString;
}

function sendWeekAjax(dataString, url) {
	$.ajax({
		type: "POST",
		url: url,
		data: dataString,
		cache: false,
		success: function(result) {
			displayTimesheets(result);
		}
	});
}

function displayTimesheets(employees) {
	var str = "";

	for (var  i = 0; i < employees.length; i++) {
		var temp = '<tr id=' + employees[i].username + ' class="employeeRow"><td>' + employees[i].first_name + ' ' + employees[i].last_name + '</td>';
		temp += '<td>' + employees[i].hours + '</td>';
		temp += '<td>' + employees[i].is_submitted + '</td>';
		temp += '<td>' + employees[i].is_approved + '</td>';

		str += temp + '</tr>';
	}

	$('#admin_body').html(str);
}

function sendTimesheetAjax(dataString, url) {
	$.ajax({
		type: "POST",
		url: url,
		data: dataString,
		cache: false,
		success: function(result) {
			insertTimesheets(result.sheets);
		}
	});
}

function insertTimesheets(timesheets) {
	var str = "";

	for (var  j = 0; j < timesheets.length; j++) {
		var total = 0;
		var temp = '<tr><td>' + timesheets[j].position + '</td>';
		if (timesheets[j].hours_worked.length > 0) {
			for (var i = 0; i < timesheets[j].hours_worked.length; i++) {
				temp += '<td>' + timesheets[j].hours_worked[i] + '</td>';
				total += timesheets[j].hours_worked[i]
			}
		} else {
			for (var i = 0; i < 7; i++) {
				temp += '<td>0</td>';
			}
		}
		temp += '<td>' + total + '</td>';

		str += temp + '</tr>';
	}

	$('#timesheet_body').html(str);

	$('#timesheet_modal').modal('toggle');
}