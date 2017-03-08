var recording = false;


function send_status() {

    var dateUnixTime = $('#datetimepicker').data("DateTimePicker").date().unix();
    var uses = $("#uses").val();
    console.log(dateUnixTime);

    $.post({
        url: "http://127.0.0.1:5000/patterns/",
        data : { name: "Test", expiration: dateUnixTime, maxUses: uses},
        success : function(json) {
            console.log(json);
        }
    });

    recording = true;
}

$(function () {
    $('#datetimepicker').datetimepicker();
});