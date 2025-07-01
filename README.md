# Hand Gesture Pong Game

This project implements a classic Pong-like game controlled by real-time hand gestures. Players use their left and right hands (detected via a webcam) to control virtual "bats" and hit a bouncing ball. The game tracks scores, features collision detection, and includes a "Game Over" state.

## Features

* **Real-time Hand Tracking:** Detects and tracks two hands (left and right) for player control.
* **Intuitive Bat Control:** Players control their bats by moving their hands vertically in front of the webcam.
* **Dynamic Ball Movement:** The ball bounces off the bats and the top/bottom walls of the game area.
* **Score Tracking:** Keeps track of scores for both the left and right players.
* **Collision Detection:** Detects when the ball collides with the bats or goes out of bounds.
* **Game Over State:** The game ends if the ball goes past either side's bat.
* **Game Reset:** Allows players to reset the game at any time by pressing 'R'.
* **Visual Game Interface:** Overlays game elements (ball, bats, scores, background) onto the live webcam feed.

## Prerequisites

* Python (3.x recommended).
* A webcam connected to your computer.
* **Game Assets:** Ensure you have the `Resources` folder containing `Background.png`, `gameOver.png`, `Ball.png`, `bat1.png`, and `bat2.png` in the same directory as `main.py`.

## Installation

1.  **Clone or Download the Repository:**
    Get the project files to your local machine.

2.  **Install Required Libraries:**
    Open your terminal or command prompt, navigate to the project directory, and run the following commands:
    ```bash
    pip install opencv-python numpy cvzone
    ```
    * Ensure `HandTrackingModule.py` is in the same directory as `main.py` or accessible in your Python path.

## Usage

1.  **Run the Script:**
    Open your terminal or command prompt, navigate to the project directory, and execute:
    ```bash
    python main.py
    ```
2.  **Play the Game:**
    * A window will open displaying your webcam feed with the game overlay.
    * **Controls:** Place your **left hand** to control the left bat and your **right hand** to control the right bat. Move your hands up and down to adjust the bats' vertical positions.
    * **Objective:** Hit the ball with your bat to keep it in play and score points.
    * **Scoring:** Each time you successfully hit the ball back, your score (displayed at the bottom of your side) increases.
    * **Game Over:** If the ball passes your bat and goes off-screen, the "Game Over" screen will appear, showing the total score of the game.
3.  **Restart Game:** Press the `R` key on your keyboard to restart the game from the beginning.
4.  **Exit:** Press the `Q` key on your keyboard to close the application window.

## How It Works

1.  **Webcam & Hand Tracking:**
    * The webcam captures live video frames.
    * `cvzone.HandDetector` detects up to two hands, identifies whether each is a "Left" or "Right" hand, and provides their bounding box coordinates.
2.  **Game Board Overlay:**
    * The live webcam feed is blended with a static `Background.png` image using `cv2.addWeighted` to create a game environment.
3.  **Bat Control:**
    * For each detected hand, the script determines its type ("Left" or "Right").
    * The vertical position of the corresponding bat (`imgBat1` or `imgBat2`) is set based on the `y` coordinate of the hand's bounding box. `np.clip` ensures the bats stay within the designated play area.
    * `cvzone.overlayPNG` is used to draw the bats on the game screen, respecting their alpha (transparency) channels.
4.  **Ball Movement & Collision:**
    * The ball's `ballPos` (x, y coordinates) is updated each frame by `speedX` and `speedY`.
    * **Bat Collision:** If the ball's position intersects with a bat's bounding box, `speedX` is reversed, and the ball's `x` position is slightly offset to prevent sticking. The corresponding player's score is incremented.
    * **Wall Collision:** If the ball hits the top or bottom boundaries of the game area, `speedY` is reversed.
    * **Out of Bounds (Game Over):** If the ball's `x` position goes beyond the left or right play area boundaries, `gameOver` is set to `True`.
5.  **Game State Management:**
    * When `gameOver` is `True`, the `imgGameOver` is displayed, along with the total score.
    * Pressing 'R' resets all game variables (ball position, speed, scores, `gameOver` flag).
6.  **Visual Display:**
    * `cvzone.overlayPNG` draws the ball.
    * `cv2.putText` displays the scores for both players in real-time.

## Customization

* **Camera Resolution:** Adjust `cap.set(3, 1280)` and `cap.set(4, 720)` for different webcam resolutions.
* **Hand Detection Confidence:** Modify `detectionCon` in `HandDetector(detectionCon=0.8)` to fine-tune hand detection sensitivity.
* **Ball Speed:** Change `speedX` and `speedY` values to make the game faster or slower.
* **Bat Position & Size:**
    * Adjust the fixed X-coordinates for `imgBat1` (`59`) and `imgBat2` (`1195`) to reposition the bats horizontally.
    * Modify the image files (`bat1.png`, `bat2.png`) themselves to change bat appearance or size.
    * Adjust the `np.clip` values (`20, 415`) to change the vertical movement range of the bats.
* **Game Area Boundaries:** Adjust the `ballPos[0] < 40` / `ballPos[0] > 1200` (horizontal) and `ballPos[1] >= 500` / `ballPos[1] <= 10` (vertical) values to change the game play area.
* **Background Blending:** Adjust the `alpha` value (`0.2` for `img` and `0.8` for `imgBackGround`) in `cv2.addWeighted` to change the transparency balance between the live feed and the background.
* **Game Assets:** Replace the images in the `Resources` folder with your own custom designs.

## Troubleshooting

* **"Unable to capture camera image!":** Verify your webcam is connected, not being used by another application, and its drivers are up-to-date. Try restarting the script or your computer.
* **No hand detection / Bats not moving:** Ensure good lighting conditions and that your hands are clearly visible to the camera. Adjust `detectionCon` if necessary.
* **Ball getting stuck on bats:** Try adjusting `ballPos[0] += 30` or `ballPos[0] -= 30` values slightly to push the ball away from the bat more effectively after a collision.
* **Image not loading:** Ensure all image files (`Background.png`, `gameOver.png`, etc.) are correctly placed in the `Resources` folder relative to your script.
