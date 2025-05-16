import pygame
import random

pygame.init()
pygame.font.init()  

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
TILE_WIDTH = 70
TILE_HEIGHT = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (150, 205, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 155)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Domino Game")
font = pygame.font.SysFont("Arial", 24, bold=False, italic=False)

# Function to draw a domino tile
def draw_domino(surface, x, y, width, height, dots1, dots2):
    """Draws a domino shape on the given Pygame surface."""
    pygame.draw.rect(surface, WHITE, (x, y, width, height))
    pygame.draw.rect(surface, BLACK, (x, y, width, height), 2)
    mid = y + height // 2
    pygame.draw.line(surface, BLACK, (x, mid), (x + width, mid), 2)

    def draw_dots(dots, cx, cy):
        """Draw dots on one side of the domino."""
        dot_radius = 5
        positions = {
            1: [(0, 0)],
            2: [(-15, -15), (15, 15)],
            3: [(-15, -15), (0, 0), (15, 15)],
            4: [(-15, -15), (15, -15), (-15, 15), (15, 15)],
            5: [(-15, -15), (15, -15), (0, 0), (-15, 15), (15, 15)],
            6: [(-15, -15), (15, -15), (-15, 0), (15, 0), (-15, 15), (15, 15)],
        }
        for dx, dy in positions.get(dots, []):
            pygame.draw.circle(surface, BLACK, (cx + dx, cy + dy), dot_radius)

    draw_dots(dots1, x + width // 2, y + height // 4)
    draw_dots(dots2, x + width // 2, y + 3 * height // 4)

# Function to generate a deck of unique dominoes
def generate_unique_dominoes():
    """Generate all unique dominoes (where left <= right)."""
    dominoes = [(i, j) for i in range(7) for j in range(i, 7)]
    random.shuffle(dominoes)
    return dominoes

# Function to draw the player's hand
def draw_hand(surface, hand, start_x, start_y):
    for i, (left, right) in enumerate(hand):
        draw_domino(surface, start_x + i * (TILE_WIDTH + 10), start_y, TILE_WIDTH, TILE_HEIGHT, left, right)

# Function to check if a domino can be placed on the board
def can_place(domino, board):
    if not board:
        return True
    left_end = board[0][0]
    right_end = board[-1][1]
    return domino[0] == left_end or domino[1] == right_end or domino[0] == right_end or domino[1] == left_end

# Function to place a domino on the board
def place_domino(domino, board):
    if not board:
        board.append(domino)
    else:
        left_end = board[0][0]
        right_end = board[-1][1]
        if domino[0] == left_end:
            board.insert(0, (domino[1], domino[0]))
        elif domino[1] == left_end:
            board.insert(0, domino)
        elif domino[0] == right_end:
            board.append(domino)
        elif domino[1] == right_end:
            board.append((domino[1], domino[0]))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("Arial", 24, bold=False, italic=False)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 200), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2,
                                   self.y + (self.height - text_surface.get_height()) // 2))

    def is_hovered(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height

    def click(self):
        if self.action:
            self.action()

# Function to calculate the score of a player's remaining dominoes
def calculate_score(hand):
    return sum(left + right for left, right in hand)

# Main game function
def game():
    global current_player
    running = True
    clock = pygame.time.Clock()

    all_dominoes = generate_unique_dominoes()
    player1_hand = all_dominoes[:7]
    player2_hand = all_dominoes[7:14]
    board = []
    current_player = random.choice([1, 2])

    def take_domino():
        global current_player, warning_text, can_take
        if current_player == 1 and len(all_dominoes) > 14:
            player1_hand.append(all_dominoes[14])
            all_dominoes.pop(14)
            warning_text = None
            can_take = False
            current_player = 2
        elif current_player == 2 and len(all_dominoes) > 14:
            player2_hand.append(all_dominoes[14])
            all_dominoes.pop(14)
            warning_text = None
            can_take = False
            current_player = 1

    Domino_taking_button = Button(680, 700, 140, 50, "Take domino", take_domino)
    warning_text = None
    can_take = False

    while running:
        screen.fill(GREEN)

        board_width = len(board) * (TILE_WIDTH + 10) - 10
        x_offset = (SCREEN_WIDTH - board_width) // 2
        y_offset = (SCREEN_HEIGHT - TILE_HEIGHT) // 2
        for i, (left, right) in enumerate(board):
            draw_domino(screen, x_offset + i * (TILE_WIDTH + 10), y_offset, TILE_WIDTH, TILE_HEIGHT, left, right)

        hand_width = len(player1_hand) * (TILE_WIDTH + 10) - 10
        player1_x_offset = (SCREEN_WIDTH - hand_width) // 2
        hand_width = len(player2_hand) * (TILE_WIDTH + 10) - 10
        player2_x_offset = (SCREEN_WIDTH - hand_width) // 2
        draw_hand(screen, player1_hand, player1_x_offset, (SCREEN_HEIGHT // 2) - 200)
        draw_hand(screen, player2_hand, player2_x_offset, (SCREEN_HEIGHT // 2) + 100)

        turn_text = font.render(f"Player {current_player}'s Turn", True, BLUE)
        screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, 30))

        if warning_text:
            screen.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))

        Domino_taking_button.draw(screen)

        if not player1_hand:
            winner_text = font.render("Player 1 Wins!", True, BLUE)
            screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - 250))
            score_text = font.render(f"Player 2's Score: {calculate_score(player2_hand)}", True, RED)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False
        elif not player2_hand:
            winner_text = font.render("Player 2 Wins!", True, BLUE)
            screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - 250))
            score_text = font.render(f"Player 1's Score: {calculate_score(player1_hand)}", True, RED)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                placed = False
                if current_player == 1:
                    for i, (left, right) in enumerate(player1_hand):
                        tile_x = player1_x_offset + i * (TILE_WIDTH + 10)
                        tile_y = (SCREEN_HEIGHT // 2) - 200
                        if tile_x < mouse_x < tile_x + TILE_WIDTH and tile_y < mouse_y < tile_y + TILE_HEIGHT:
                            if can_place((left, right), board):
                                place_domino((left, right), board)
                                player1_hand.pop(i)
                                placed = True
                                warning_text = None
                                current_player = 2
                                can_take = False
                                break
                    if not placed:
                        warning_text = font.render("Invalid move! Press 'Take domino' to pick a new one.", True, RED)
                        can_take = True
                elif current_player == 2:
                    for i, (left, right) in enumerate(player2_hand):
                        tile_x = player2_x_offset + i * (TILE_WIDTH + 10)
                        tile_y = (SCREEN_HEIGHT // 2) + 100
                        if tile_x < mouse_x < tile_x + TILE_WIDTH and tile_y < mouse_y < tile_y + TILE_HEIGHT:
                            if can_place((left, right), board):
                                place_domino((left, right), board)
                                player2_hand.pop(i)
                                placed = True
                                warning_text = None
                                current_player = 1
                                can_take = False
                                break
                    if not placed:
                        warning_text = font.render("Invalid move! Press 'Take domino' to pick a new one.", True, RED)
                        can_take = True

                if Domino_taking_button.is_hovered((mouse_x, mouse_y)) and can_take:
                    Domino_taking_button.click()

        pygame.display.flip()
        clock.tick(30)

pygame.quit()

if __name__ == "__main__":
    game()