import curses
import random
import sys
import os

# Try to import curses. If it fails on Windows, give a helpful message.
try:
    import curses
except ImportError:
    if os.name == 'nt':
        print("Error: The 'curses' module is not installed.")
        print("Please install it by running: pip install windows-curses")
        sys.exit(1)
    else:
        print("Error: The 'curses' module is missing.")
        sys.exit(1)

def create_food(snake, box_height, box_width, start_y, start_x):
    """
    Generate a new food location that is not part of the snake body.
    box_height, box_width: Dimensions of the playable area.
    start_y, start_x: Top-left corner of the playable area.
    """
    snake_positions = set(tuple(pos) for pos in snake)
    while True:
        # Generate random coordinates within the game boundaries (excluding borders)
        food_y = random.randint(start_y + 1, start_y + box_height - 2)
        food_x = random.randint(start_x + 1, start_x + box_width - 2)
        
        if (food_y, food_x) not in snake_positions:
            return [food_y, food_x]

def main(stdscr):
    # 1. Setup Screen
    curses.curs_set(0)        # Hide the cursor
    stdscr.nodelay(1)         # Make getch() non-blocking
    stdscr.timeout(100)       # Refresh every 100ms (controls game speed)
    
    # Enable Colors if supported
    if curses.has_colors():
        curses.start_color()
        # Pair 1: Green text on Black background (Snake)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # Pair 2: Red text on Black background (Food)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        # Pair 3: White text on Black background (Border/Text)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    # Get Screen Dimensions
    sh, sw = stdscr.getmaxyx()
    
    # To ensure the game fits in most terminals and looks neat, let's define a game box.
    # We will use the full screen but keep a margin or just use the full dimension provided.
    # Writing to the absolute bottom-right char often causes error in curses, so we reduce by 1.
    box_h = sh
    box_w = sw
    
    # Initialize Snake (start in the middle)
    # Snake is a list of [y, x] coordinates. Head is at index 0.
    snk_y = box_h // 2
    snk_x = box_w // 4
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]
    
    # Initialize separate colors for snake head and body if desired, 
    # but for simplicity we use Green for the whole snake.

    # Place initial food
    food = create_food(snake, box_h, box_w, 0, 0)
    
    # Initial Direction
    key = curses.KEY_RIGHT
    
    # Score
    score = 0
    
    # 2. Game Loop
    while True:
        # --- Draw Phase ---
        stdscr.clear()
        
        # Draw Border
        stdscr.attron(curses.color_pair(3))
        # border(ls, rs, ts, bs, tl, tr, bl, br)
        # We handle drawing manually to avoid issues with some terminals or simple box()
        stdscr.border(0) 
        
        # Display Score and Title
        title = f" SNAKE GAME - Score: {score} "
        # Center the title at the top border
        stdscr.addstr(0, (box_w // 2) - (len(title) // 2), title, curses.color_pair(3) | curses.A_BOLD)
        stdscr.attroff(curses.color_pair(3))
        
        # Draw Food
        stdscr.addch(food[0], food[1], '●', curses.color_pair(2) | curses.A_BOLD)
        
        # Draw Snake
        for i, point in enumerate(snake):
            y, x = point
            # Head drawn slightly differently (optional) or just same
            char = 'O' if i == 0 else 'o'
            stdscr.addch(y, x, char, curses.color_pair(1))
            
        # Refresh screen to show changes
        stdscr.refresh()
        
        # --- Input Phase ---
        next_key = stdscr.getch()
        
        # If no key is pressed, keep going in same direction
        # If key is pressed, update direction, but prevent 180 degree turns
        if next_key != -1:
            if (next_key == curses.KEY_DOWN and key != curses.KEY_UP) or \
               (next_key == curses.KEY_UP and key != curses.KEY_DOWN) or \
               (next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
               (next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT):
                key = next_key
            # Support WASD
            elif (next_key == ord('s') and key != curses.KEY_UP): key = curses.KEY_DOWN
            elif (next_key == ord('w') and key != curses.KEY_DOWN): key = curses.KEY_UP
            elif (next_key == ord('a') and key != curses.KEY_RIGHT): key = curses.KEY_LEFT
            elif (next_key == ord('d') and key != curses.KEY_LEFT): key = curses.KEY_RIGHT
            # Exit Key
            elif next_key == 27: # ESC
                break

        # --- Logic Phase ---
        # Calculate new head position
        head = snake[0]
        if key == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif key == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif key == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif key == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
            
        # Check Collision with Walls
        # Borders are at 0 and box_h-1, 0 and box_w-1
        # Playable area is 1 to box_h-2, 1 to box_w-2
        if (new_head[0] <= 0 or new_head[0] >= box_h - 1 or
            new_head[1] <= 0 or new_head[1] >= box_w - 1):
            break
            
        # Check Collision with Self
        if new_head in snake:
            break
            
        # Move Snake
        snake.insert(0, new_head)
        
        # Check Food Consumption
        if new_head == food:
            score += 1
            # Increase speed slightly every 5 points (optional, keeps it interesting)
            # timer = getattr(stdscr, 'timeout') # Not directly accessible easily, skip for simplicity or use manual variable
            food = create_food(snake, box_h, box_w, 0, 0)
        else:
            # If food not eaten, remove tail to maintain length
            snake.pop()

    # --- Game Over ---
    stdscr.nodelay(0) # Switch back to blocking input
    
    # Show Game Over Message
    msg_lines = [
        "GAME OVER",
        f"Final Score: {score}",
        "",
        "Press any key to exit..."
    ]
    
    # Calculate center position
    center_y = box_h // 2 - len(msg_lines) // 2
    
    # Draw a box for the message
    for i, line in enumerate(msg_lines):
        center_x = box_w // 2 - len(line) // 2
        stdscr.addstr(center_y + i, center_x, line, curses.color_pair(3) | curses.A_BOLD)
    
    stdscr.refresh()
    stdscr.getch() # Wait for input

if __name__ == "__main__":
    # Check for windows-curses on Windows
    # (The check at top handles the import error, but we can't automate install inside script easily without subproccess)
    curses.wrapper(main)
