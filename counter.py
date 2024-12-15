import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(point1, point2, point3):
    """Calculate angle between three points."""
    a = np.array(point1)  # First
    b = np.array(point2)  # Mid
    c = np.array(point3)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Webcam feed
cap = cv2.VideoCapture(0)

# Rep counting variables
left_counter = 0
left_stage = None
right_counter = 0
right_stage = None

while cap.isOpened():
    ret, frame = cap.read()

    # Convert the frame to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make pose detection
    results = pose.process(image)

    # Revert the image to BGR for rendering
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates for the left arm
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        # Calculate angle for the left arm
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        # Visualize left arm angle
        cv2.putText(image, str(int(left_angle)), 
                    tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                    )

        # Rep counting logic for left arm
        if left_angle > 160:
            left_stage = "down"
        if left_angle < 30 and left_stage == "down":
            left_stage = "up"
            left_counter += 1
            print(f'Left Arm Reps: {left_counter}')

        # Get coordinates for the right arm
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        # Calculate angle for the right arm
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Visualize right arm angle
        cv2.putText(image, str(int(right_angle)), 
                    tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                    )

        # Rep counting logic for right arm
        if right_angle > 160:
            right_stage = "down"
        if right_angle < 30 and right_stage == "down":
            right_stage = "up"
            right_counter += 1
            print(f'Right Arm Reps: {right_counter}')

    except Exception as e:
        print(e)

    # Render pose landmarks
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), 
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )

    # Display the counter
    cv2.rectangle(image, (0, 0), (300, 100), (245, 117, 16), -1)
    cv2.putText(image, 'LEFT REPS', (15, 12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(left_counter), 
                (15, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(image, 'RIGHT REPS', (160, 12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(right_counter), 
                (160, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the output frame
    cv2.imshow('Exercise Rep Counter', image)

    # Break loop with 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
