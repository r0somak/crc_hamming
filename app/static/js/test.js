$( document ).ajaxStart(function() {
    $( "#loading" ).show();
  }).ajaxStop(function() {
    $( "#loading" ).hide();
  });

function generateCrc(){
    $.ajax({
        url : "http://localhost:5000/crc",
        method : 'post',
        data : {
            inputData : $("#entryData").val(),
            crcType : $("#crcType").val(),
        },
        dataType : "json"
    })
    .done(function(response){
        $("#1").text(response['crc'])
    }).fail(function(){
        $("#1").text("CHINA BAD")
    });
}