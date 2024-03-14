# playlist-duration-extension

A chrome extension to calculate the duration of a youtube playlist.

1) Get your API key on "https://console.developers.google.com/"
2) Install the required libraries by running the command `pip install -r requirements.txt`
3) Run the fastapi backend by running `uvicorn restController:app  --reload` in py directory.
4) Backend application will start and swagger can be accessed using http://127.0.0.1:8000/docs.
