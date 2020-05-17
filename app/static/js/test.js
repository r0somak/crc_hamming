$( document ).ajaxStart(function() {
    $( "#loading" ).show();
  }).ajaxStop(function() {
    $( "#loading" ).hide();
  });

function colorizeHamming(str, id, positions=null){
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
        $("#0").text(response['bitInputData']);
        $("#1").text(response['crc']);
        $("#2").text(response['inp_crc']);
        colorizeHamming(response['hamming'], 3);
        $("#datatable").show();
    }).fail(function(response){
        $("#0").html(response.responseText.fontcolor('red'));
        $("#datatable").show();
    });
}

function corrupt(){
    let hamm = document.getElementById(3);
    console.log(hamm.innerText)
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
        colorizeHamming(response['corruptedData'], 4, response['corruptedPositions']);
        $( "#corTable" ).show();
    }).fail(function(response){
        $("#4").html(response.responseText.fontcolor('red'));
        $( "#corTable" ).show();
    });
}