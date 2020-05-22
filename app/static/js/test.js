$( document ).ajaxStart(function() {
    $( "#loading" ).show();
  }).ajaxStop(function() {
    $( "#loading" ).hide();
  });

var pos = null;
var ctrl_pos = null;
var crc = null;

function colorizeHamming(str, id, positions=null, corPos=null){
    let array = str.split('')
    let potega = 1;
    for (let i = 0; i<str.length; i++) {
        if (i === potega - 1) {
            potega += potega;
            array[i] = str.charAt(i).fontcolor('green');
        }else {
            array[i] = str[i];
        }
    }
    if (positions != null){
        for(let i = 0; i < positions.length; i++){
            array[positions[i]] = str.charAt(positions[i]).fontcolor('red');
        }
    }
    if (corPos != null){
        array[corPos] = str.charAt(corPos).fontcolor('violet');
    }
    let s1 = document.getElementById(id);
    s1.innerHTML = array.join('');
}

function hamming(){
    $.ajax({
        url : "http://localhost:5000/hamming",
        method : 'post',
        data : {
            inputData : $("#entryData").val(),
            crcType : $("#crcType").val(),
        },
        dataType : "json"
    })
    .done(function(response){
        ctrl_pos = response['ctrl_pos'];
        $("#0").text(response['bitInputData']);
        crc = response['crc']
        $("#1").text(crc);
        $("#2").text(response['inp_crc']);
        colorizeHamming(response['hamming'], 3);
    }).fail(function(response){
        $("#0").html(response.responseText.fontcolor('red'));
    }).always(function (response){
        $( "#data" ).show();
        $( "#corrupt" ).hide();
        $( "#fixed" ).hide();
        $( "#decode" ).hide();
    });
}

function corrupt(){
    let hamm = document.getElementById(3);
    $.ajax({
        url : "http://localhost:5000/corrupt",
        method : 'post',
        data : {
            inputData : hamm.innerText,
            positions : $("#corBits").val()
        },
        dataType : "json"
    })
    .done(function(response){
        pos = response['corruptedPositions']
        colorizeHamming(response['corruptedData'], 4, pos);
    }).fail(function(response){
        $("#4").html(response.responseText.fontcolor('red'));

    }).always(function (response){
        $( "#corrupt" ).show();
        $( "#fixed" ).hide();
        $( "#decode" ).hide();
    });
}

function fix(){
    let corrupted = document.getElementById(4)
    $.ajax({
        url : "http://localhost:5000/fix",
        method : 'post',
        data : {
            inputData : corrupted.innerText,
        },
        dataType : "json"
    })
    .done(function(response){
        $("#5").text(response['corPos']);
        colorizeHamming(response['output'], 6, pos, response['corPos']);
    }).fail(function(response){
        $( "#5" ).html(response.responseText.fontcolor('red'));
    }).always(function (response){
        $( "#fixed" ).show();
        $( "#decode" ).hide();
    });
}

function decode(){
    $.ajax({
        url : "http://localhost:5000/decode",
        method : 'post',
        data : {
            original_data: $( "#0" ).text(),
            inputData: $( "#6" ).text(),
            crc_code: crc,
        },
        dataType : "json"
    })
    .done(function(response){
        $( "#7" ).text(response['original']);
        $( "#8" ).text(response['data']);
        $( "#9" ).text(response['msg']);
        $( "#10" ).text(response['ascii']);
    }).fail(function(response){
    }).always(function (response){
        $( "#decode" ).show();
    });
}