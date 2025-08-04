# Real-Time Rock-Paper-Scissors Game

A simple, two-player, real-time Rock-Paper-Scissors game built with Python and the Dash framework. This browser-based game captures keyboard inputs from two players and determines the winner of each round in real-time.

## Features

- **Two-Player Gameplay**: Player 1 on the left, Player 2 on the right.
- **Real-Time Input**: Players must make their move within 300ms of each other for a round to count.
- **Keyboard Controls**: Simple and intuitive keyboard controls for both players.
- **Score Tracking**: The game keeps and displays the score for each player.
- **Clean UI**: A simple and clean user interface built with Dash.

## Tech Stack

- Python
- Dash
- Dash Extensions

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\\Scripts\\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

With your virtual environment activated and dependencies installed, run the following command in the project's root directory:

```bash
python app.py
```

Navigate to the URL printed in your terminal (usually `http://127.0.0.1:8050/`) in your web browser.

## How to Play

The game window must be in focus to register keystrokes. Click anywhere on the game's web page first.

-   **Player 1 Controls (Left Side):**
    -   `A`: Rock
    -   `S`: Paper
    -   `D`: Scissors

-   **Player 2 Controls (Right Side):**
    -   `4`: Rock
    -   `5`: Paper
    -   `6`: Scissors
    (These can be from the number row or the numpad)

Both players must press their key within **300 milliseconds** of each other for the round to be judged. The winner's choice will be highlighted in green, and the score will update.
