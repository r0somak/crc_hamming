$( document ).ajaxStart(function() {
    $( "#loading" ).show();
  }).ajaxStop(function() {
    $( "#loading" ).hide();
  });

function colorizeHamming(str, id){
        let coloredHamming = "";
        let potega = 1;
        for (let i = 0; i<str.length; i++) {
            if (i === potega - 1) {
                potega += potega;
                coloredHamming += str.charAt(i).fontcolor("red");
            }else {
                coloredHamming += str[i];
            }
        }
        let s1 = document.getElementById(id);
        s1.innerHTML = coloredHamming;
}

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
        $("#datatable").show();
        $("#0").text(response['bitInputData']);
        $("#1").text(response['crc']);
        $("#2").text(response['inp_crc']);
        colorizeHamming(response['hamming'], 3)

    }).fail(function(){
        $("#0").text("CHINA BAD");
    });
}