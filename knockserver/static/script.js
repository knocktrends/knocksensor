var recording = false;


function send_status() {
    $.post({
        url: "",
        data : { is_recording: !recording},
        success : function(json) {
            console.log(data.is_recording);
        }
    })
}

$(function () {
    $('#datetimepicker1').datetimepicker();
});