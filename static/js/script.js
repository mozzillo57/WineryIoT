let map;
let ids = [];
let values = [];
let labels = [];
let datasets = [];
let data = {};
let count = 0;
function initMap() {
    // The map, centered at Uluru
    var pos = { lat: lat, lng: lng }
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: pos,
    });

    // The marker, positioned at Uluru
    var marker = new google.maps.Marker({
        position: pos,
        map: map,
    });
}

function timedRefresh(timeoutPeriod) {
    setTimeout("location.reload(true);", timeoutPeriod);
}

function setupVal(id, v, l) {
    ids.push(String('Sensor' + id))
    values.push(v.split(", "))
    labels.push(l)
}

function createchart(id) {
    var ctx = document.getElementById(id).getContext('2d');
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    var rgb = "rgb(" + r + "," + g + "," + b + ")";
    var label = 'Sensor'+id
    var dataset = {
        label: label,
        data: JSON.parse(values[count]),
        fill: false,
        borderColor: rgb,
    }

    var data = {
        datasets: [dataset],
        labels: JSON.parse(labels[count])
    }

    var prova = {
        type: 'line',
        data: data,
        options: {
            responsive: false
        }
    }
    var chart = new Chart(ctx, prova);
    count = count + 1;
}