import cv2
import os

def crop_and_save_video(input_video_path, output_video_path, crop_coords, target_fps):
    """
    Function to crop a video to the specified coordinates in real-time and adjust FPS.

    :param input_video_path: Path to the input video.
    :param output_video_path: Path to save the cropped video.
    :param crop_coords: Tuple of (start_x, start_y, end_x, end_y) for cropping.
    :param target_fps: Desired frames per second (FPS) for the output video.
    """

    # Open the input video file
    cap = cv2.VideoCapture(input_video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video_path}")
        return
    
    # Get the original video's frame rate (FPS)
    original_fps = cap.get(cv2.CAP_PROP_FPS)

    # Handle case where FPS is zero (invalid)
    if original_fps == 0:
        print(f"Error: Original FPS is zero for video {input_video_path}. Skipping this video.")
        cap.release()
        return

    # Ensure the target FPS does not exceed the original FPS
    if target_fps > original_fps:
        print(f"Warning: Target FPS ({target_fps}) is higher than the original FPS ({original_fps}). Setting target FPS to original FPS.")
        target_fps = original_fps

    # Get the original video dimensions (width and height)
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Processing video: {input_video_path}")
    print(f"Original video size: {original_width}x{original_height}")

    # Define the crop coordinates (start_x, start_y, end_x, end_y)
    start_x, start_y, end_x, end_y = crop_coords

    # Ensure the crop coordinates don't exceed the video dimensions
    if end_x > original_width or end_y > original_height:
        print(f"Error: Crop dimensions exceed original video dimensions. Max allowed is {original_width}x{original_height}")
        cap.release()
        return

    # Adjust the cropping width and height based on video size
    cropped_width = end_x - start_x
    cropped_height = end_y - start_y

    if cropped_width <= 0 or cropped_height <= 0:
        print(f"Error: Invalid crop dimensions for {input_video_path}. Skipping this video.")
        cap.release()
        return

    # Define the codec and create VideoWriter object to save the output video with the target FPS
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, target_fps, (cropped_width, cropped_height))

    frame_count = 0
    skip_frames = max(1, int(original_fps // target_fps))  # Ensure skip_frames is at least 1

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Only write every nth frame, based on the target FPS
        if frame_count % skip_frames == 0:
            # Crop the frame based on the new valid coordinates
            cropped_frame = frame[start_y:end_y, start_x:end_x]

            # Write the cropped frame to the output video
            out.write(cropped_frame)

        frame_count += 1

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Finished processing: {output_video_path}")

# Example usage for cropping and changing FPS for multiple videos
input_video_dir = 'org_footage/'
output_video_dir = 'processed_footage/'

# Create the output directory if it doesn't exist
if not os.path.exists(output_video_dir):
    os.makedirs(output_video_dir)

# Define the calculated video cropping coordinates
crop_coords = (24, 14, 405, 180)

# Define the target FPS for the output videos
target_fps = 10

# Process each video
for video_file in os.listdir(input_video_dir):
    if video_file.endswith('.mp4'):
        input_video_path = os.path.join(input_video_dir, video_file)
        output_video_path = os.path.join(output_video_dir, f'processed_{video_file}')

        crop_and_save_video(input_video_path, output_video_path, crop_coords, target_fps)

print("Processing completed for all videos.")
