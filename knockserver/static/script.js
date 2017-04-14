var recording = false;


function send_status() {

    var expirationDate = $('#datetimepicker').data("DateTimePicker").date().unix().toString();
    var uses = $("#uses").val();

    var doNotDisturbStart = $('#dnd_start').data("DateTimePicker").date().unix().toString();
    var doNotDisturbEnd = $('#dnd_end').data("DateTimePicker").date().unix().toString();

    $.ajax({
        type: "POST",
        contentType: "application/json",
        dataType: 'json',
        url: "http://127.0.0.1:5000/patterns/",
        data : JSON.stringify({name: "Test", expiration: expirationDate, maxUses: uses})
    });

    recording = true;
}

$(function () {
    $('#datetimepicker').datetimepicker();
    $('#dnd_start').datetimepicker();
    $('#dnd_end').datetimepicker();
});