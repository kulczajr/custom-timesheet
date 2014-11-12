$(document).ready(function() {
	$("#createPosition").click(function (e) {
		var name = document.getElementById('position').value;
		var dataString = "title=" + name;
		createPositionAjax(dataString, '/createPosition');
	});

	$("#employees").change(function (e) {
		var employee = $(this).val();
		var dataString = "username=" + employee;
		sendAjax(dataString, '/retrievePositions');
	});

	$("#removePosition").click(function (e) {
		var username = document.getElementById('employees').value;
		var position = document.getElementById('userPositions').value;
		var dataString = "username=" + username + "&position=" + position;
		sendAjax(dataString, '/removePosition');
	});

	$("#addPosition").click(function (e) {
		var username = document.getElementById('employees').value;
		var position = document.getElementById('notUserPositions').value;
		var dataString = "username=" + username + "&position=" + position;
		sendAjax(dataString, '/addPosition');
	});

	$("#employees").trigger('change');
});

function sendAjax(dataString, url) {
	$.ajax({
		type: "POST",
		url: url,
		data: dataString,
		cache: false,
		success: function(titles) {
			reloadPositions(titles[0], titles[1]);
		}
	});
}

function reloadPositions(notUserTitles, userTitles) {
	var notUserString = "";
	var userString = "";

	notUserTitles.forEach(function (title) {
		notUserString += '<option value="' + title + '">' + title + "</option>";
	});

	userTitles.forEach(function (title) {
		userString += '<option value="' + title + '">' + title + "</option>";
	});

	$("#notUserPositions").html(notUserString);
	$("#userPositions").html(userString);
}

function createPositionAjax(dataString, url) {
	$.ajax({
		type: "POST",
		url: url,
		data: dataString,
		cache: false,
		success: function(result){
			if (!result) {
				alert("Position already exists");
			}
		}
	});
}
