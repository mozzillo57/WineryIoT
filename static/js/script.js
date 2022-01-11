let map;
let ids = [];
let values = [];
let labels = [];
let datasets = [];
let data = {};
let count = 0;
let marker;

function initMap() {
    // The map, centered at Uluru
    var pos = { lat: lat, lng: lng }
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: pos,
    });
    marker = new google.maps.Marker();
    // The marker, positioned at Uluru
    marker.setPosition(pos);
    marker.setMap(map);
}

function period_type(){   
    window.location.reload();
}

function timedRefresh(timeoutPeriod) {
    setTimeout("location.reload(true);", timeoutPeriod);
}

function setupVal(id, v, l) {
    ids.push(String('Sensor' + id))
    values.push(v.split(", "))
    labels.push(l.split(", "))
}

function createchart(id, period) {
    var ctx = document.getElementById(id).getContext('2d');
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    var rgb = "rgb(" + r + "," + g + "," + b + ")";
    var label = 'Sensor'+id
    var lbs = []
    var dataset = {
        label: label,
        data: JSON.parse(values[count]),
        fill: false,
        borderColor: rgb,
    }

    var e = document.getElementById("period");
    console.log(e.value);

    var data = {
        datasets: [dataset],
        labels: JSON.parse(labels[count])
    }

    var config = {
        type: 'line',
        data: data,
        options: {
            responsive: false,
            scales: {
                xAxes: [ {
                    display: true,
                    type: 'time',
                    time: {
                      unit: e.value,
                      unitStepSize: 1,
                      displayFormats : {
                        'second': 'HH:MM:SS',
                        'minute': 'HH:MM',
                        'hour': 'HH:MM',
                        'day': 'MMM DD',
                      }
                    }
                  }
                ]
            }
        }
    }
    var chart = new Chart(ctx, config);
    count = count + 1;
}