import cv2 # Import the OpenCV library for image and video processing.
import cvzone # Import cvzone for helper functions like hand detection and image overlay.
from cvzone.HandTrackingModule import HandDetector # Import HandDetector for hand detection and tracking.
import numpy as np # Import numpy for numerical operations, especially for clipping values.

# --- Webcam Initialization ---
cap = cv2.VideoCapture(0) # Initialize video capture from the default webcam (index 0).
cap.set(3, 1280) # Set the width of the captured video frame to 1280 pixels.
cap.set(4, 720)  # Set the height of the captured video frame to 720 pixels.

# --- Load Game Resources (Images) ---
# Ensure these image files exist in a 'Resources' folder relative to your script.
imgBackGround = cv2.imread("Resources/Background.png") # Background image for the game.
imgGameOver = cv2.imread("Resources/gameOver.png") # Game over screen image.
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED) # Ball image (with alpha channel for transparency).
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED) # Left player's bat image (with alpha channel).
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED) # Right player's bat image (with alpha channel).

# --- Hand Detector Initialization ---
# Detects a maximum of 2 hands with a detection confidence of 0.8.
detector = HandDetector(detectionCon=0.8, maxHands=2)

# --- Game State Variables ---
ballPos = [100, 100] # Initial position of the ball [x, y].
speedX = 15 # Horizontal speed of the ball.
speedY = 15 # Vertical speed of the ball.

gameOver = False # Flag to indicate if the game is over.
score = [0,0] # Scores for player 1 (left) and player 2 (right). [player1_score, player2_score].

# --- Main Game Loop ---
while True :
    # Read a frame from the webcam. '_' is used to ignore the 'success' boolean as it's not directly checked here.
    _, img = cap.read()
    img = cv2.flip(img, 1) # Flip the image horizontally for a mirror effect.
    
    # Detect hands in the frame. flipType=False means it won't flip hand points internally.
    hands, img = detector.findHands(img, flipType=False)
    
    # Overlay the live camera feed onto the background image with transparency.
    # The game elements will be drawn on top of this blended image.
    img = cv2.addWeighted(img, 0.2, imgBackGround, 0.8, 0) # 0.2 for foreground (camera), 0.8 for background.
    
    if hands : # If any hand is detected:
        for hand in hands : # Iterate through each detected hand.
            x,y,w,h = hand['bbox'] # Get bounding box coordinates for the current hand.
            h1, w1, _ = imgBat1.shape # Get dimensions of the bat image (assuming both bats have same size).
            
            # Calculate the Y position for the center of the bat based on hand's Y position.
            y1 = y - h1//2
            # Clip the Y position to keep the bat within the vertical bounds of the game area.
            y1 = np.clip(y1, 20, 415) # 20 and 415 are calculated bounds based on background/bat size.
            
            # If the detected hand is the Left hand:
            if hand['type'] == "Left" :
                # Overlay bat1 (left player's bat) onto the image at the fixed left X position and calculated Y.
                img = cvzone.overlayPNG(img, imgBat1, (59,y1)) # 59 is the fixed X position for the left bat.
                
                # Collision detection for the left bat with the ball.
                # Check if ball's X is within bat's X range AND ball's Y is within bat's Y range.
                if (59 < ballPos[0] < 59 + w1) and (y1 < ballPos[1] < y1 + h1):
                    speedX = -speedX # Reverse ball's horizontal direction.
                    ballPos[0] += 30 # Move ball slightly to the right to prevent sticking.
                    score[0] += 1 # Increment left player's score.
                    
            # If the detected hand is the Right hand:
            if hand['type'] == "Right" :
                # Overlay bat2 (right player's bat) onto the image.
                # X position for right bat is 1195, adjusting for its width to align to the right edge.
                img = cvzone.overlayPNG(img, imgBat2, (1195,y1))
                
                # Collision detection for the right bat with the ball.
                # (1195 - 50 < ballPos[0] < 1195 - 30) is a simplified check for ball's X hitting the bat.
                # It means ball is within a certain X range close to the right bat.
                if (1195 - 50 < ballPos[0] < 1195 - 30) and (y1 < ballPos[1] < y1 + h1):
                    speedX = -speedX # Reverse ball's horizontal direction.
                    ballPos[0] -= 30 # Move ball slightly to the left to prevent sticking.
                    score[1] += 1 # Increment right player's score.

    # --- Game Over Condition ---
    # If ball goes past the left or right boundaries.
    if ballPos[0] < 40 or ballPos[0] > 1200 : # 40 and 1200 are the X boundaries of the game play area.
        gameOver = True # Set game over flag.
        
    if gameOver : # If game is over:
        img = imgGameOver.copy() # Display the game over screen (use a copy to avoid modifying original asset).
        # Display the total score (sum of both players' scores) on the game over screen.
        cv2.putText(img, str(score[0] + score[1]).zfill(2), (585,360), cv2.FONT_HERSHEY_COMPLEX, 
                    2.5, (200,0,200), 5) # Score position, font, scale, color (purple), thickness.
        
    else : # If game is still ongoing:
        # Check for vertical wall collisions (top and bottom of the play area).
        if ballPos[1] >= 500 or ballPos[1] <= 10 : # 500 and 10 are the Y boundaries of the play area.
            speedY = -speedY # Reverse ball's vertical direction.
    
        # Update ball's position based on its current speed.
        ballPos[0] += speedX
        ballPos[1] += speedY
    
        # Overlay the ball image at its current position.
        img = cvzone.overlayPNG(img, imgBall, ballPos) # Ball's top-left will be at ballPos.
    
    # Display player scores on the game screen (even during gameplay).
    cv2.putText(img, str(score[0]), (300,650), cv2.FONT_HERSHEY_COMPLEX, # Left player score.
                3, (255,255,255), 5) # White color.
    
    cv2.putText(img, str(score[1]), (900,650), cv2.FONT_HERSHEY_COMPLEX, # Right player score.
                3, (255,255,255), 5) # White color.
    
    cv2.imshow("Image", img) # Display the final game image.
    key = cv2.waitKey(1) # Wait for 1ms for a key press.
    
    if key == ord("r") : # If 'r' key is pressed, reset the game.
        ballPos = [100, 100] # Reset ball position.
        speedX = 15 # Reset ball horizontal speed.
        speedY = 15 # Reset ball vertical speed.

        gameOver = False # Reset game over flag.
        score = [0,0] # Reset scores.
        # It's good practice to re-read imgGameOver here if it could have been modified,
        # but in this case, it's just a static image.
        # imgGameOver = cv2.imread("Resources/gameOver.png") 
    
    if key == ord("q") : # If 'q' key is pressed, break the loop and exit.
        break

# Release the webcam object and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()