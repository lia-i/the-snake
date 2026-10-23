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
OBJECT_COLOR = (0, 255, 255)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

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


def handle_keys(object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            object.next_direction = KEYDOWN_DIRECTION_DICT.get(
                (object.direction, event.key),
                object.direction
            )


class GameObject:
    """
    Базовый класс для игровых объектов.

    Предоставляет общую логику для хранения позиции, цвета и отрисовки
    объектов на игровом поле. Используется как родительский класс для
    яблока и змеи.

    Атрибуты:
        position (tuple): Текущие координаты объекта.
        body_color (tuple): Цвет объекта в формате RGB.
    """

    def __init__(self, color=OBJECT_COLOR):
        self.position = CENTER
        self.body_color = color

    def randomize_position(self, occupied_positions):
        """Получить координаты точки для позиции."""
        while self.position in occupied_positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

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
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_positions=(CENTER))

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
        x_head_position, y_head_position = self.get_head_position()
        x_direction, y_direction = self.direction
        new_head = (
            (x_head_position + x_direction * GRID_SIZE + SCREEN_WIDTH)
            % SCREEN_WIDTH,
            (y_head_position + y_direction * GRID_SIZE + SCREEN_HEIGHT)
            % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) != self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self, occupied_position=None):
        """Метод, с помощью которого сбрасываются изменяемые свойства змеи."""
        if occupied_position:
            self.randomize_position(occupied_position)
        else:
            self.position = CENTER
        self.positions = [self.position]
        self.length = 1
        self.direction = DOWN
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод для отрисовки змеи."""
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.draw_rect(self.get_head_position())


def main():
    """pg."""
    pg.init()
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset((apple.position))
        elif apple.position in snake.positions:
            apple.randomize_position(snake.positions)
            snake.length += 1
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
