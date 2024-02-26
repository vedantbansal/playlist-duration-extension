let baseURL = "http://localhost:8000";

document.getElementById("urlForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let playlistURL = document.getElementById("playlistURL").value;
    displayDuration(playlistURL);
});

async function displayDuration(playlistURL){
    const pattern = /(?:list=)([\w-]+)/;
    const playlistId = playlistURL.match(pattern);
    let durationDisplay = document.getElementById("durationDisplay");
    if(playlistId === null){
      durationDisplay.textContent = "Couldn't find a playlist.";
      return;
    }
    const duration = await fetch(`${baseURL}/find-duration?playlistId=${playlistId[1]}`)
    const response = await duration.json();
    durationDisplay.textContent = response["hours"] + " hours " + response["minutes"] + " minutes " + response["seconds"] + " seconds";
}