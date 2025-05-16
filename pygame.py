import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
CELL_SIZE = BOARD_SIZE // 3
O_COLOR = (255, 0, 0)  # Red
X_COLOR = (0, 0, 255)  # Blue
LINE_COLOR = (0, 0, 0)  # Black
BG_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (180, 180, 180)
WINNING_LINE_COLOR = (0, 200, 0)  # Green

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")

# Fonts
try:
    font = pygame.font.SysFont('Arial', 40)
    small_font = pygame.font.SysFont('Arial', 30)
except:
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 30)

def draw_board(board):
    """Draws the Tic-Tac-Toe grid and the players' moves."""
    # Draw the grid lines
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), 
                         (BOARD_SIZE, i * CELL_SIZE), LINE_WIDTH)  # Horizontal
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), 
                         (i * CELL_SIZE, BOARD_SIZE), LINE_WIDTH)  # Vertical
    
    # Draw X's and O's
    for i in range(9):
        row, col = i // 3, i % 3
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        
        if board[i] == "X":
            offset = CELL_SIZE // 3
            pygame.draw.line(screen, X_COLOR,
                             (center_x - offset, center_y - offset),
                             (center_x + offset, center_y + offset),
                             LINE_WIDTH)
            pygame.draw.line(screen, X_COLOR,
                             (center_x + offset, center_y - offset),
                             (center_x - offset, center_y + offset),
                             LINE_WIDTH)
        elif board[i] == "O":
            radius = CELL_SIZE // 3
            pygame.draw.circle(screen, O_COLOR, (center_x, center_y), radius, LINE_WIDTH)

def draw_status(message):
    """Displays the game status message."""
    pygame.draw.rect(screen, BG_COLOR, (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))
    text = font.render(message, True, TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, BOARD_SIZE + 20))

def draw_button(text, rect, hover=False):
    """Draws a button with hover effect."""
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, TEXT_COLOR, rect, 2)
    text_surface = small_font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def check_winner(board):
    """Checks if there is a winner or a draw."""
    # Winning combinations: rows, columns, diagonals
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]], combo  # Winner and winning combination
    if " " not in board:
        return "Draw", []  # Draw
    return None, []  # No winner yet

def minimax(board, depth, is_maximizing):
    """Implements the minimax algorithm for AI decision-making."""
    result, _ = check_winner(board)
    if result == "X":
        return -10 + depth
    elif result == "O":
        return 10 - depth
    elif result == "Draw":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def ai_move(board):
    """Determines the best move for the AI using minimax."""
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def draw_winning_line(combo):
    """Draws a line through the winning combination."""
    start = combo[0] // 3 * CELL_SIZE + CELL_SIZE // 2, combo[0] % 3 * CELL_SIZE + CELL_SIZE // 2
    end = combo[2] // 3 * CELL_SIZE + CELL_SIZE // 2, combo[2] % 3 * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(screen, WINNING_LINE_COLOR, start, end, WIN_LINE_WIDTH)

def reset_game():
    """Resets the game state."""
    return [" "] * 9, "X", False, None, []

def main():
    """Main game loop."""
    board, current_player, game_over, winner, winning_combo = reset_game()
    reset_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over and reset_rect.collidepoint(event.pos):
                    board, current_player, game_over, winner, winning_combo = reset_game()
                elif not game_over and current_player == "X":
                    x, y = event.pos
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        col, row = x // CELL_SIZE, y // CELL_SIZE
                        index = row * 3 + col
                        if board[index] == " ":
                            board[index] = "X"
                            winner, winning_combo = check_winner(board)
                            game_over = winner is not None
                            current_player = "O" if not game_over else current_player

        if not game_over and current_player == "O":
            move = ai_move(board)
            if move is not None:
                board[move] = "O"
                winner, winning_combo = check_winner(board)
                game_over = winner is not None
                current_player = "X"

        # Drawing
        screen.fill(BG_COLOR)
        draw_board(board)
        if game_over:
            if winner == "Draw":
                draw_status("Game Over - It's a Draw!")
            else:
                draw_status(f"Game Over - {winner} Wins!")
                draw_winning_line(winning_combo)
        else:
            draw_status(f"Current Player: {current_player}")
        draw_button("Play Again", reset_rect, reset_rect.collidepoint(mouse_pos))
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pygame.quit()
        sys.exit()