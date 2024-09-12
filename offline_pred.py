import threading
import cv2
from ultralytics import YOLO
import os

def run_tracker_in_thread(filename, model, file_index):
    """
    Runs a video file or webcam stream concurrently with the YOLOv8 model using threading.

    This function captures video frames from a given file or camera source and utilizes the YOLOv8 model for object
    tracking. The function runs in its own thread for concurrent processing.

    Args:
        filename (str): The path to the video file or the identifier for the webcam/external camera source.
        model (obj): The YOLOv8 model object.
        file_index (int): An index to uniquely identify the file being processed, used for display purposes.

    Note:
        Press 'q' to quit the video display window.
    """
    video = cv2.VideoCapture(filename)  # Read the video file

    # Define the output video file
    output_file = f"output_video_{file_index}.mp4"
    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change the fourcc code for MP4 format
    output_video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while True:
        ret, frame = video.read()  # Read the video frames

        # Exit the loop if no more frames in either video
        if not ret:
            break

        # Track objects in frames if available
        results = model.predict(frame)
        res_plotted = results[0].plot()
        cv2.imshow(f"Tracking_Stream_{file_index}", res_plotted)

        # Write the frame with object tracking overlay to the output video
        output_video.write(res_plotted)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release video sources and video writer
    video.release()
    output_video.release()

# Load the models
print(os.getcwd())
model1 = YOLO('realtime/siddique bests/best (5).pt')
model2 = YOLO('realtime/siddique bests/best (5).pt')

# # Define the video files for the trackers
video_file1 = "realtime/vidyo4.mp4"  # Path to video file, 0 for webcam
video_file2 = "realtime/vidyo4.mp4"  # Path to video file, 0 for webcam, 1 for external camera

# # Create the tracker threads
tracker_thread1 = threading.Thread(target=run_tracker_in_thread, args=(video_file1, model1, 1), daemon=True)
tracker_thread2 = threading.Thread(target=run_tracker_in_thread, args=(video_file2, model2, 2), daemon=True)

# # Start the tracker threads
tracker_thread1.start()
tracker_thread2.start()

# # Wait for the tracker threads to finish
tracker_thread1.join()
tracker_thread2.join()

# # Clean up and close windows
# cv2.destroyAllWindows()