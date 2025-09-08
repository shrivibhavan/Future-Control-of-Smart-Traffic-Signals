function updateData(){
    fetch('http://127.0.0.1:8000/getData')
    .then(response => response.json())
    .then(data =>{
        document.getElementById('noOfVehiclesNorth').innerHTML = data.noOfVehiclesNorth;
        document.getElementById('timerNorth').innerHTML = data.timerNorth;
        document.getElementById('noOfVehiclesEast').innerHTML = data.noOfVehiclesEast;
        document.getElementById('timerEast').innerHTML = data.timerEast;
        document.getElementById('noOfVehiclesWest').innerHTML = data.noOfVehiclesWest;
        document.getElementById('timerWest').innerHTML = data.timerWest;
        document.getElementById('noOfVehiclesSouth').innerHTML = data.noOfVehiclesSouth;
        document.getElementById('timerSouth').innerHTML = data.timerSouth;
        document.getElementById('estimatedWaitTimeWest').innerHTML = data.estimatedWaitTimeWest;
        document.getElementById('estimatedWaitTimeNorth').innerHTML = data.estimatedWaitTimeNorth;
        document.getElementById('estimatedWaitTimeEast').innerHTML = data.estimatedWaitTimeEast;
        document.getElementById('estimatedWaitTimeSouth').innerHTML = data.estimatedWaitTimeSouth;
    });
}

setInterval(updateData,100);

function signalControl(){
    var data1 = document.getElementById('timerNorth').innerHTML;
    if(data1 == '0'){
        document.getElementById('northRed').setAttribute('style','background-color:#FF033E');
        document.getElementById('northGreen').setAttribute('style','background-color:#337f00');
        document.getElementById('northRed').setAttribute('style','box-shadow: 0 0 5px 2px #fe2255,0 0 11px 6px #d46c6c');
    }
    else{
        document.getElementById('northRed').setAttribute('style','background-color:#920224');
        document.getElementById('northGreen').setAttribute('style','background-color:#5adf02');
        document.getElementById('northGreen').setAttribute('style','box-shadow: 0 0 5px 2px #93e05f,0 0 9px 5px #ffffff');
    }

    var data2 = document.getElementById('timerSouth').innerHTML;
    if(data2 == '0'){
        document.getElementById('southRed').setAttribute('style','background-color:#FF033E');
        document.getElementById('southGreen').setAttribute('style','background-color:#337f00');
        document.getElementById('southRed').setAttribute('style','box-shadow: 0 0 5px 2px #fe2255,0 0 11px 6px #d46c6c');
    }
    else{
        document.getElementById('southRed').setAttribute('style','background-color:#920224');
        document.getElementById('southGreen').setAttribute('style','background-color:#5adf02');
        document.getElementById('southGreen').setAttribute('style','box-shadow: 0 0 5px 2px #93e05f,0 0 9px 5px #ffffff');
    }

    var data3 = document.getElementById('timerEast').innerHTML;
    if(data3 == '0'){
        document.getElementById('eastRed').setAttribute('style','background-color:#FF033E');
        document.getElementById('eastGreen').setAttribute('style','background-color:#337f00');
        document.getElementById('eastRed').setAttribute('style','box-shadow: 0 0 5px 2px #fe2255,0 0 11px 6px #d46c6c');
    }
    else{
        document.getElementById('eastRed').setAttribute('style','background-color:#920224');
        document.getElementById('eastGreen').setAttribute('style','background-color:#5adf02');
        document.getElementById('eastGreen').setAttribute('style','box-shadow: 0 0 5px 2px #93e05f,0 0 7px 5px #ffffff');
    }

    var data4 = document.getElementById('timerWest').innerHTML;
    if(data4 == '0'){
        document.getElementById('westRed').setAttribute('style','background-color:#FF033E');
        document.getElementById('westGreen').setAttribute('style','background-color:#337f00');
        document.getElementById('westRed').setAttribute('style','box-shadow: 0 0 5px 2px #fe2255,0 0 11px 6px #d46c6c');
    }
    else{
        document.getElementById('westRed').setAttribute('style','background-color:#920224');
        document.getElementById('westGreen').setAttribute('style','background-color:#5adf02');
        document.getElementById('westGreen').setAttribute('style','box-shadow: 0 0 5px 2px #93e05f,0 0 7px 5px #ffffff');
    }
}

setInterval(signalControl,100);