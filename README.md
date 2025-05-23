# YouTube-Video-Downloader
A Streamlit app to download YouTube videos and audio


#Docker Use

To build the docker conatiner use the command
```bash
docker build -t YouTube-Video-Downloader .
```

Run the Docker container 
```bash
docker run -itd -v ./downloads:/app/downloads --name YouTube-Video-Downloader YouTube-Video-Downloader
```