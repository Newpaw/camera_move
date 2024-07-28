import cv2
import ffmpeg
import time
import os

class VideoRecorder:
    def __init__(self, device='/dev/video0', output_dir='/app/videos'):
        self.device = device
        self.output_dir = output_dir

    def record_video(self, duration, filename):
        output_path = os.path.join(self.output_dir, filename)
        (
            ffmpeg
            .input(self.device, format='v4l2', framerate=30)
            .output(output_path, t=duration, video_bitrate='500k')
            .run()
        )

class MotionDetector:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Cannot open camera")
        self.ret, self.frame1 = self.cap.read()
        self.ret, self.frame2 = self.cap.read()

    def detect_motion(self):
        if not self.ret:
            return False

        diff = cv2.absdiff(self.frame1, self.frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            motion_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(self.frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        self.frame1 = self.frame2
        self.ret, self.frame2 = self.cap.read()

        return motion_detected

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

class MotionCaptureApp:
    def __init__(self, motion_detector, video_recorder, recording_duration=60):
        self.motion_detector = motion_detector
        self.video_recorder = video_recorder
        self.recording_duration = recording_duration

    def run(self):
        while True:
            try:
                if self.motion_detector.detect_motion():
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    filename = f"motion_{timestamp}.mp4"
                    print(f"Motion detected, recording video to {filename}")
                    self.motion_detector.release()
                    self.video_recorder.record_video(self.recording_duration, filename)
                    self.motion_detector = MotionDetector()
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    motion_detector = MotionDetector()
    video_recorder = VideoRecorder()
    app = MotionCaptureApp(motion_detector, video_recorder)
    app.run()
