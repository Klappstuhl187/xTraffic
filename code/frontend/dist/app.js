"use strict";
const timeOptions = { year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
let socket; // WebSocket-Objekt
function connectWebSocket() {
    // Verbindung zum WebSocket-Server herstellen
    socket = new WebSocket('ws://localhost:3000/ws');
    socket.addEventListener('open', () => {
        // Event-Handler für erfolgreiche Verbindung
        console.log('WebSocket connection established.');
        document.getElementById('reconnect-button').style.display = "none"; // Verstecke den "Reconnect"-Button
    });
    socket.addEventListener('message', (event) => {
        console.log(event.data);
        let data = JSON.parse(event.data); // Nachricht parsen
        if (Array.isArray(data)) {
            const firstEntry = data[0];
            if ('state' in firstEntry) {
                console.log(data);
                data = data;
                console.log('Receiving initial-data.');
                updateCrossingList(data);
            }
            else if ('id' in firstEntry) {
                data = data;
                console.log('Receiving initial-data (traffic-data).');
                for (const dataEntry of data)
                    addTrafficEntry(dataEntry);
            }
        }
        else {
            if ('state' in data) {
                data = data;
                console.log('Crossing update received.');
                updateSingleCrossing(data.crossingId, data.state);
            }
            else if ('time' in data) {
                data = data;
                console.log('Crossing countdown received.');
                startCrossingCountdown(data.crossingId, data.time);
            }
            else if ('id' in data) {
                data = data;
                console.log('Traffic data received.');
                addTrafficEntry(data);
            }
        }
    });
    socket.addEventListener('close', () => {
        // Event-Handler für geschlossene Verbindung
        console.log('WebSocket connection closed.');
        document.getElementById('reconnect-button').style.display = "block"; // Zeige den "Reconnect"-Button
    });
    socket.addEventListener('error', (error) => {
        // Event-Handler für Fehler
        console.error('WebSocket error:', error);
        document.getElementById('reconnect-button').style.display = "block"; // Zeige den "Reconnect"-Button
    });
}
function addTrafficEntry(data) {
    const tableRow = document.createElement('tr');
    const dataId = document.createElement('td');
    dataId.textContent = data.id.toString();
    const dataCrossingId = document.createElement('td');
    dataCrossingId.textContent = data.crossingId.toString();
    const time1 = new Date(data.time1 * 1000);
    const time2 = new Date(data.time2 * 1000);
    const speed = (data.speed * 3.6).toFixed(2);
    const dataTime1 = document.createElement('td');
    dataTime1.textContent = time1.toLocaleString('de-DE', timeOptions);
    const dataTime2 = document.createElement('td');
    dataTime2.textContent = time2.toLocaleString('de-DE', timeOptions);
    const dataSpeed = document.createElement('td');
    dataSpeed.textContent = speed + "Km/H";
    tableRow.appendChild(dataId);
    tableRow.appendChild(dataCrossingId);
    tableRow.appendChild(dataTime1);
    tableRow.appendChild(dataTime2);
    tableRow.appendChild(dataSpeed);
    document.getElementById('db-table').appendChild(tableRow);
}
function startCrossingCountdown(crossingId, time) {
    const countdownDiv = document.getElementById("cd-" + crossingId);
    countdownDiv.style.display = "block";
    const spanElement = document.getElementById("cdt-" + crossingId);
    const interval = setInterval(() => {
        time = time - 1;
        if (time <= 0) {
            clearInterval(interval);
            countdownDiv.style.display = "none";
        }
        else
            spanElement.textContent = time.toString();
    }, 1000);
}
function toggleCrossing(crossingId) {
    // Sende die ID der Schranke zum Server, um den Zustand zu toggeln
    socket.send(crossingId.toString());
}
function setButtonState(button, state) {
    // Setze den Zustand des Buttons basierend auf dem Schranken-Zustand
    if (state) {
        button.classList.remove('up');
        button.classList.add('down');
        button.textContent = 'Schranke runterfahren'; // Text für den Zustand "unten"
    }
    else {
        button.classList.remove('down');
        button.classList.add('up');
        button.textContent = 'Schranke hochfahren'; // Text für den Zustand "oben"
    }
}
function setTextState(element, crossingId, state) {
    element.textContent = `Übergang ${crossingId} - Schranken ${state ? 'Oben' : 'Unten'}`;
}
function updateCrossingList(crossings) {
    const crossingList = document.getElementById('crossing-list');
    if (!crossingList)
        return;
    crossingList.innerHTML = '';
    crossings.forEach(crossing => {
        const crossingDiv = document.createElement('div');
        crossingDiv.classList.add('crossing-item');
        const crossingText = document.createElement('span');
        crossingText.id = "text-" + crossing.crossingId;
        setTextState(crossingText, crossing.crossingId, crossing.state);
        // Countdown
        const countdownDiv = document.createElement('div');
        countdownDiv.id = "cd-" + crossing.crossingId;
        countdownDiv.className = "countdown";
        countdownDiv.style.display = "none";
        const countdownImg = document.createElement('img');
        countdownImg.src = "/clock.png";
        const countdownText = document.createElement('span');
        countdownText.id = "cdt-" + crossing.crossingId;
        countdownDiv.appendChild(countdownImg);
        countdownDiv.appendChild(countdownText);
        const button = document.createElement('button');
        button.id = "btn-" + crossing.crossingId;
        if (!crossing.disabled) {
            button.addEventListener('click', () => toggleCrossing(crossing.crossingId));
            setButtonState(button, crossing.state);
            button.classList.add('button');
        }
        else {
            button.className = 'disabled-button';
            button.textContent = 'Nicht verfügbar';
        }
        crossingDiv.appendChild(crossingText);
        crossingDiv.appendChild(countdownDiv);
        crossingDiv.appendChild(button);
        crossingList.appendChild(crossingDiv);
    });
}
function updateSingleCrossing(crossingId, newState) {
    console.log(`Crossing ${crossingId} -> ${newState}`);
    const crossingText = document.getElementById(`text-${crossingId}`);
    const crossingButton = document.getElementById(`btn-${crossingId}`);
    setTextState(crossingText, crossingId, newState);
    setButtonState(crossingButton, newState);
}
function init() {
    connectWebSocket();
    document.getElementById('reconnect-button').onclick = () => connectWebSocket();
}
init();
