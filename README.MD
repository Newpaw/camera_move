# Motion Detection and Video Recording

This project detects motion using a webcam and records a video when motion is detected. The recorded videos are saved in a specified directory and served via an NGINX web server.

## Requirements

- Docker
- A webcam connected to the host machine

## Setup

### Clone the repository

```bash
git clone <repository-url>
cd camera_move
```
### Install dependencies

If you want to run the application outside of Docker, make sure you have the necessary dependencies installed:

```bash
pip install -r requirements.txt
```
## Usage
### Running with Docker
Build the Docker image
```bash
docker build -t camera_app .
```
Run the Docker container
```bash
sudo docker run --device=/dev/video0:/dev/video0 -v /home/jan/projects/camera_move/videos:/app/videos -p 80:80 --rm camera_app
```
- --device=/dev/video0:/dev/video0: Maps the webcam device to the container.
- -v /home/jan/projects/camera_move/videos:/app/videos: Maps the directory on the host to store recorded videos to the container.
- -p 80:80: Maps port 80 on the host to port 80 in the container.

Now, you should be able to access the recorded videos via your web browser:
```bash
http://<your-server-ip>/videos
```

## License
This project is licensed under the MIT License.