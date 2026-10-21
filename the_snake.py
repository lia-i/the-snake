from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(self):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


class GameObject:
    """Базовый класс объектов."""

    def __init__(self):
        self.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def randomize_position(self):
        """Получить координаты точки."""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод для отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи."""

    def __init__(self):
        self.randomize_position()
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = (0, 1)
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод, позволяющий получить голову змеи."""
        return self.positions[0]

    def move(self, apple_object):
        """Метод, отвечающий за движение змеи."""
        x, y = self.get_head_position()
        i, j = self.direction
        new_head = ((x + i * GRID_SIZE + SCREEN_WIDTH) % SCREEN_WIDTH,
                    (y + j * GRID_SIZE + SCREEN_HEIGHT) % SCREEN_HEIGHT)

        if new_head == apple_object.position:
            self.length += 1
            self.last = None
            apple_object.randomize_position()

        elif new_head in self.positions:
            self.reset(apple_object)
        else:
            self.last = self.positions.pop()

        self.positions.insert(0, new_head)

    def reset(self, apple_object):
        """Метод, с помощью которого игра начинается сначала."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple_object.randomize_position()
        self.randomize_position()

    def draw(self):
        """Метод для отрисовки змеи."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    """PyGame."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    running = True

    while running:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        snake.draw()
        apple.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
