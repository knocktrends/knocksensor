var recording = false;


function send_status() {

    var dateUnixTime = $('#datetimepicker').data("DateTimePicker").date().unix();
    var uses = $("#uses").val();
    console.log(dateUnixTime)
    console.log(uses);

    // $.post({
    //     url: "",
    //     data : { is_recording: !recording, time: dateUnixTime},
    //     success : function(json) {
    //         console.log(data.is_recording);
    //     }
    // });

    recording = true;
}

$(function () {
    $('#datetimepicker').datetimepicker();
});