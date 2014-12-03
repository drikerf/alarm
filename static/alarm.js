
// Get current alarm from server.
var getAlarm = function() {
    request = new XMLHttpRequest();
    request.open('GET', '/alarm', true);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            data = JSON.parse(request.responseText);
            console.log('Got response from get alarm:');
            console.log(data);
            if (data.hour) {
                console.log('There was data!');
                dispAlarm(data);
                dispDelete();
            } else {
                console.log('There was empty data!');
            }
        } else {
            // Server responded with error.
        }
    };
    request.onerror = function() {
        // Problem with connection.
    };
    request.send();
};

// Display alarm.
var dispAlarm = function(time) {
    console.log('Setting alarm for ' + data.hour + ' hours and ' + data.minute + ' minutes');
    document.getElementById('hour').value = data.hour;
    document.getElementById('minute').value = data.minute;
};

// Display delete button.
var dispDelete = function() {
    document.getElementById('deleteAlarm').style.display = 'block';
};

// Hide delete button.
var hideDelete = function() {
    document.getElementById('deleteAlarm').style.display = 'none';

};

// Set alarm.
var setAlarm = function() {
    data = {}
    data.hour = document.getElementById('hour').value;
    data.minute = document.getElementById('minute').value;
    if (data.hour === '' || data.minute == '') {
        alert('fill out form');
        return;
    }
    console.log('Setting alarm for ' + data.hour + ' hours and ' + data.minute + ' minutes');
    request = new XMLHttpRequest();
    request.open('POST', '/alarm', true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            console.log('POST status OK');
            dispDelete();
        } else {
            console.log('Server responded with error code: ' + request.status);
        }
    };
    request.onerror = function() {
        // Problem with connection.
    };
    request.send(JSON.stringify(data));
};

// Delete alarm.
var deleteAlarm = function() {
    request.open('DELETE', '/alarm', true);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            console.log('Server responded ok! Alarm deleted.');
            hideDelete();
        } else {
            // Server responded with error.
        }
    };
    request.onerror = function() {
        // Problem with connection.
    };
    request.send();
};

// Set event listeners.
document.getElementById('setAlarm').onclick = function() {
    setAlarm();
};
document.getElementById('deleteAlarm').onclick = function() {
    deleteAlarm();
};

// Init.
getAlarm();
