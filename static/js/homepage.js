
$(document).ready(function() {
	$('#timesheet_table').DataTable();

	$("#weekSelect").html(getWeeks(new Date()));

	$("#weekSelect").change(function (e) {
		var week = document.getElementById('weekSelect').value;
		var dataString = "time_period=" + week;
		sendWeekAjax(dataString, '/retrieveTimesheet');
	});
	$("#weekSelect").trigger('change');

	$("#saveTimesheet").click(function (e) {
		var week = document.getElementById('weekSelect').value;

		var myRows = [];
		var headersText = [];
		var $headers = $("th");

		var $rows = $("tbody tr").each(function(index) {
			$cells = $(this).find("td input");
			myRows[index] = [];

			myRows[index][0] = $(this).children('td:first-child').html();

			$cells.each(function(cellIndex) {
				cellIndex += 1;
				if(headersText[cellIndex] === undefined) {
					headersText[cellIndex] = $($headers[cellIndex]).text();
				}
				myRows[index][cellIndex] = $(this).val();
			});    
		});

		var mergedData = []
		mergedData = mergedData.concat.apply(mergedData, myRows);

		var data = {
			'week': week,
			'hours': mergedData
		};
 
		sendSaveAjax(data, '/saveTimesheet');
	});

	$('#submitTimesheet').click(function (e) {
    	data = {
    		'time_period': document.getElementById('weekSelect').value,
    		'username': $('#user').html()
    	}

    	$.ajax({
			type: "POST",
			url: "/submitTimesheet",
			data: data,
			cache: false,
			success: function(result) {
				$("#weekSelect").trigger('change');
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
			insertTimesheets(result.sheets);
		}
	});
}

function insertTimesheets(timesheets) {
	var str = "";

	if (timesheets[0].is_submitted) {
		for (var  j = 0; j < timesheets.length; j++) {
			var temp = '<tr><td>' + timesheets[j].position + '</td>';
			if (timesheets[j].hours_worked.length > 0) {
				for (var i = 0; i < timesheets[j].hours_worked.length; i++) {
					temp += '<td><input disabled=true id="hour[' + i + ']" value=' + timesheets[j].hours_worked[i] + '></input></td>';
				}
			} else {
				for (var i = 0; i < 7; i++) {
					temp += '<td><input disabled=true id="hour[' + i + ']" value=0></input></td>';
				}
			}

			str += temp + '</tr>';
		}

		$('#saveTimesheet').prop("disabled", true);
		$('#submitTimesheet').prop("disabled", true);
	} else {
		for (var  j = 0; j < timesheets.length; j++) {
			var temp = '<tr><td>' + timesheets[j].position + '</td>';
			if (timesheets[j].hours_worked.length > 0) {
				for (var i = 0; i < timesheets[j].hours_worked.length; i++) {
					temp += '<td><input id="hour[' + i + ']" value=' + timesheets[j].hours_worked[i] + '></input></td>';
				}
			} else {
				for (var i = 0; i < 7; i++) {
					temp += '<td><input id="hour[' + i + ']" value=0></input></td>';
				}
			}

			str += temp + '</tr>';
		}

		$('#saveTimesheet').prop("disabled", false);
		$('#submitTimesheet').prop("disabled", false);
	}

	$('#timesheet_body').html(str);
}

function sendSaveAjax(dataString, url) {

	//dataString = {"week": "hello", "hours": "fake"};

	$.ajax({
		type: "POST",
		url: url,
		data: dataString,
		traditional: true,
		cache: false,
		success: function(result) {
			
		}
	});
}