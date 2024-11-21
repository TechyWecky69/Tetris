import pygame
import random

global score

pygame.init()

WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

SHAPES = {
    "O": [[1, 1],
          [1, 1]],

    "I": [[1],
          [1],
          [1],
          [1]],

    "T": [[0, 1, 0],
          [1, 1, 1]],

    "L": [[1, 0],
          [1, 0],
          [1, 1]],

    "Z": [[1, 1, 0],
          [0, 1, 1]],

    "S": [[0,1,1],
          [1,1,0]]
}


class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2  # Center the block
        self.y = 0

    def move_down(self, grid):
        """Move the block down if possible."""
        if not self.collision(grid, dx=0, dy=1):
            self.y += 1
        else:
            self.lock_to_grid(grid)

    def move_sideways(self, grid, direction):
        """Move the block left or right if possible."""
        dx = 1 if direction == "right" else -1
        if not self.collision(grid, dx=dx, dy=0):
            self.x += dx

    def rotate(self, grid):
        """Rotate the block 90 degrees clockwise if possible."""
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        original_shape = self.shape
        self.shape = rotated_shape

        if self.collision(grid):
            self.shape = original_shape

    def collision(self, grid, dx=0, dy=0):
        """Check for collision with the grid."""
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if (
                        new_x < 0 or new_x >= COLS or
                        new_y >= ROWS or
                        (new_y >= 0 and grid[new_y][new_x])
                    ):
                        return True
        return False

    def lock_to_grid(self, grid):
        """Lock the block to the grid."""
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[self.y + i][self.x + j] = self.color


def create_grid():
    """Create an empty grid."""
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


def clear_full_rows(grid):
    """Clear full rows and return the updated grid."""
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(new_grid) < ROWS:
        new_grid.insert(0, [0 for _ in range(COLS)])
    return new_grid


def draw_grid(grid):
    """Draw the grid on the screen."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)  # Draw grid lines
            if cell:
                pygame.draw.rect(screen, cell, rect)


def main():
    grid = create_grid()
    current_block = Block(random.choice(list(SHAPES.values())), random.choice(COLORS))
    running = True
    fall_time = 0
    fall_speed = 500

    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick(60)

        if fall_time > fall_speed:
            current_block.move_down(grid)
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_block.move_sideways(grid, "left")
                elif event.key == pygame.K_RIGHT:
                    current_block.move_sideways(grid, "right")
                elif event.key == pygame.K_DOWN:
                    current_block.move_down(grid)
                elif event.key == pygame.K_SPACE:
                    current_block.rotate(grid)

        if any(grid[0]):
            print("Game Over!")
            running = False
        elif current_block.collision(grid, dy=1):
            current_block.lock_to_grid(grid)
            grid = clear_full_rows(grid)
            current_block = Block(random.choice(list(SHAPES.values())), random.choice(COLORS))

        draw_grid(grid)
        for i, row in enumerate(current_block.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = current_block.x + j
                    y = current_block.y + i
                    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(screen, current_block.color, rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
