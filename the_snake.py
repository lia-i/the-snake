from random import randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 5

KEYDOWN_DIRECTION_DICT = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT
}


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


def handle_keys(self):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            self.next_direction = KEYDOWN_DIRECTION_DICT.get(
                (self.direction, event.key),
                self.direction
            )


class GameObject:
    """
    Базовый класс объектов игры.
    Атрибуты:
    position - позиция объекта.
    body_color - цвет объекта.
    Методы:
    randomize_position - присваивает позиции случайные незанятые координаты.
    draw_rect - отрисовывает клетку на поле.
    draw - отрисовывает объект на поле с помощью draw_rect.
    """

    def __init__(self, color=APPLE_COLOR):
        self.position = CENTER
        self.body_color = color

    def randomize_position(self, occupied_position):
        """Получить координаты точки для позиции."""
        running = True
        while running:
            self.position = (
                randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE
            )
            if self.position not in occupied_position:
                running = False

    def draw_rect(self, position, color=None):
        """Метод для отрисовки одной ячейки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color if color else self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод для отрисовки объекта."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        super().__init__()
        self.randomize_position(occupied_position=CENTER)

    def draw(self):
        """Метод для отрисовки яблока."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс змеи."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.direction = DOWN
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

    def move(self):
        """Метод, отвечающий за движение змеи."""
        x_coordinate, y_coordinate = self.get_head_position()
        x_add, y_add = self.direction
        new_head = (
            (x_coordinate + x_add * GRID_SIZE + SCREEN_WIDTH) % SCREEN_WIDTH,
            (y_coordinate + y_add * GRID_SIZE + SCREEN_HEIGHT) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

    def reset(self, occupied_position=CENTER):
        """Метод, с помощью которого сбрасываются изменяемые свойства змеи."""
        self.randomize_position(occupied_position)
        self.positions = [self.position]
        self.length = 1
        self.direction = DOWN
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод для отрисовки змеи."""
        self.draw_rect(self.positions[0])

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    """pg."""
    pg.init()
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        snake.draw()
        apple.draw()

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset((apple.position))
        if apple.position in snake.positions:
            apple.randomize_position(snake.positions)
            snake.length += 1
        if len(snake.positions) != snake.length:
            snake.last = snake.positions.pop()
        else:
            snake.last = None
        pg.display.update()


if __name__ == '__main__':
    main()
