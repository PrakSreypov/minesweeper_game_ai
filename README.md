# **Minesweeper with AI and Pygame**

## **Introduction**
This project is a Python implementation of the classic Minesweeper game, enhanced with an AI-powered solver. The AI uses logical reasoning to deduce the positions of mines and safe cells. The game is designed with a graphical interface created using **Pygame**.

---

## **Features**
1. **Classic Minesweeper Gameplay**:
   - Reveal cells to find mines.
   - Right-click to flag cells as mines.
   - Avoid detonating a mine to win the game.

2. **AI Solver**:
   - The AI uses a **knowledge base** and logical reasoning to identify safe cells or mines.
   - Incorporates:
     - **Safe move deduction**: Based on known information, marks certain cells as safe.
     - **Random move fallback**: If no logical move is available, the AI makes a random move.
     - **Inference system**: The AI learns from every revealed cell and updates its knowledge base.

3. **Graphical User Interface**:
   - Interactive grid for gameplay.
   - Visual elements for flags, mines, and revealed cells.
   - Dynamic buttons for:
     - Autoplaying with AI.
     - Showing AI inferences (safe and mine predictions).
     - Resetting the game.

4. **Autoplay**:
   - Watch the AI automatically solve the Minesweeper board step-by-step.

---

## **Getting Started**

### **Prerequisites**
- Python 3.x
- Install the following Python libraries:
  ```bash
  pip install pygame
  ```

### **Files in the Project**
1. **`minesweeper.py`**: Contains the game logic and AI logic.
2. **`main.py`**: Runs the graphical interface using Pygame.
3. **Assets**:
   - **Fonts**: Located in `assets/fonts/` (e.g., `OpenSans-Regular.ttf`).
   - **Images**: Located in `assets/images/` (e.g., `flag.png`, `mine.png`).

---

## **How to Run**

1. **Clone or Download the Repository**:
   - Clone the repository or download it as a zip file.

2. **Navigate to the Project Directory**:
   ```bash
   cd <project-directory>
   ```

3. **Run the Game**:
   ```bash
   python runner.py
   ```

---

## **Game Instructions**

### **Objective**:
Mark all the mines on the board without triggering any of them.

### **Controls**:
- **Left-Click**: Reveal a cell.
- **Right-Click**: Flag a cell as a mine.
- **Buttons**:
  - **Autoplay**: Lets the AI take over and solve the board.
  - **AI Move**: Allows the AI to make a single move.
  - **Reset**: Resets the game to start over.
  - **Show Inference**: Highlights AI's safe and mine predictions.

### **Win Condition**:
- Flag all mines correctly without triggering any.

### **Lose Condition**:
- Clicking on a mine detonates it, ending the game.

---

## **AI Algorithm**

### **Core Concepts**:
1. **Knowledge Base**:
   - The AI maintains a set of logical **sentences** about the game board.
   - Each sentence represents a relationship between a group of cells and the number of mines in them.

2. **Inference**:
   - The AI deduces:
     - **Safe cells**: Cells that can be revealed without risk.
     - **Mines**: Cells that must contain mines.
   - It uses techniques like **subset reasoning** to infer new information.

3. **Fallback**:
   - When no safe move can be logically deduced, the AI chooses a random unexplored cell.

---

## **Code Overview**

### **`minesweeper.py`**

1. **`Minesweeper` Class**:
   - Handles the game board and mine placement.
   - Tracks the number of nearby mines for any cell.
   - Provides utility methods for checking mines and determining win/loss states.

2. **`Sentence` Class**:
   - Represents logical statements about cells and their mine counts.
   - Provides methods for marking cells as safe or mines, enabling the AI to refine its knowledge base.

3. **`MinesweeperAI` Class**:
   - Implements the AI logic to deduce safe cells and mines.
   - Maintains knowledge of all moves made, safe cells, and mines.
   - Dynamically updates its knowledge base with each new revelation.

---

### **`runner.py`**

1. **Game Setup**:
   - Initializes the Minesweeper board and AI.
   - Loads assets (e.g., images and fonts) for rendering.

2. **Graphical User Interface**:
   - Displays the Minesweeper board, cells, and interactive buttons.
   - Highlights flagged cells, revealed cells, and inferred safe/mine cells.

3. **Gameplay Loop**:
   - Handles user input for cell clicks and button presses.
   - Integrates AI to make safe or random moves during autoplay.

---

## **Project Structure**
```plaintext
📂 Project Folder
├── 📂 assets
│   ├── 📂 fonts
│   │   └── OpenSans-Regular.ttf
│   ├── 📂 images
│       ├── flag.png
│       ├── mine.png
│       ├── mine-red.png
├── .gitignore
├── minesweeper.py
├── README.py
└── runner.py
```

---

## **Future Improvements**
- Add support for customizable grid sizes and mine counts through a user interface.
- Improve AI inference for edge cases with low mine densities.
- Include a leaderboard to track game completions and performance metrics.

--- 

## **Acknowledgments**
- **Pygame**: For creating an intuitive library to design 2D games.
- **Inspiration**: The classic Minesweeper game and AI algorithms based on logical reasoning.
