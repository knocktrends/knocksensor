var recording = false;


function send_status() {

    var dateUnixTime = $('#datetimepicker').data("DateTimePicker").date().unix();
    var uses = $("#uses").val();

    var date = dateUnixTime.toString();

    $.ajax({
        type: "POST",
        contentType: "application/json",
        dataType: 'json',
        url: "http://127.0.0.1:5000/patterns/",
        data : JSON.stringify({name: "Test", expiration: date, maxUses: uses})
    });

    recording = true;
}

$(function () {
    $('#datetimepicker').datetimepicker();
});