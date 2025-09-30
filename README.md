# Description
A retro-inspired block breaker game built with Python and Pygame. The player controls a paddle to bounce a ball and break blocks. The game includes upgrades, sound effects, CRT-style visuals, and multiple levels. It also features a pause menu and intro screen with interactive buttons.

# Features

- **Intuitive Gameplay**: Control the bar to keep the ball in play and break all the blocks.
- **Dynamic Upgrades**: Collect various upgrades to enhance your gameplay, including speed and size modifications.
- **Interactive Main Menu**: Start the game, learn more, or quit through an intuitive main menu interface.
- **Pause Functionality**: Easily pause and resume your game with a key press.
- **Retro CRT Effect**: Enjoy a nostalgic gaming experience with a built-in CRT-style visual effect.
- **Sound Effects and Music**: Engaging background music and sound effects enhance the gaming experience.

# Screenshots
<img width="500" height="371" alt="Screenshot 2025-09-30 200151" src="https://github.com/user-attachments/assets/bd63071e-6e5a-432a-858a-b766f9296603" />
<img width="498" height="367" alt="Screenshot 2025-09-30 200206" src="https://github.com/user-attachments/assets/a63e17ed-0630-49ff-89bb-9be4bb53873e" />

# Implementation Details

This project is implemented in **Python** using the **Pygame** library.  
The game logic is fully object-oriented, with separate classes for each entity:

- **`Ball`**  
  Handles ball movement, collision detection with the paddle (`Bar`), blocks, and screen boundaries.  
  It updates position based on speed and direction, and reverses trajectory upon collisions.

- **`Bar` (Paddle)**  
  Represents the player’s paddle. It reacts to keyboard input (`LEFT` / `RIGHT` keys) and restricts movement within screen boundaries.  
  Collision with the ball influences the ball’s angle.

- **`Block`**  
  Represents destructible blocks. Each block has coordinates, dimensions, and health.  
  When hit by the ball, it decreases health and disappears when destroyed.

- **`Upgrade`**  
  Power-ups that randomly spawn when a block is destroyed.  
  Examples: paddle extension, speed change, extra life. They fall down and are collected if the paddle catches them.

- **`Game`**  
  Main game controller:
  - Initializes Pygame and screen  
  - Loads levels (block layouts)  
  - Handles game loop (events, updates, rendering)  
  - Manages score, lives, upgrades, and level transitions  
  - Includes pause menu and intro screen with interactive buttons  

### Game Loop Structure
1. **Event Handling** –> keyboard input, quitting, pause menu.  
2. **Update Phase** –> updates positions of the ball, paddle, upgrades, and checks collisions.  
3. **Render Phase** –> draws background, blocks, paddle, ball, UI (score, lives), and active effects.  


