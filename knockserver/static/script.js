var recording = false;


function send_status() {

    var dateUnixTime = $('#datetimepicker').data("DateTimePicker").date().unix();
    var uses = $("#uses").val();

    var date = dateUnixTime.toString();

    $.ajax({
        type: "POST",
        contentType: "application/json",
        dataType: 'json',
        url: "/patterns/",
        data : JSON.stringify({name: door_name, door_name: door_name, expiration: date, maxUses: uses})
    });

    recording = true;
}

$(function () {
    $('#datetimepicker').datetimepicker();
});