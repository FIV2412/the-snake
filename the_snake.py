"""Игра «Изгиб Питона» — змейка на Pygame."""

from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
cell_x = SCREEN_WIDTH // GRID_SIZE
cell_y = SCREEN_HEIGHT // GRID_SIZE
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FONT_COLOR = (255, 255, 255)
SPEED = 20


class GameObject:
    """Базовый игровой объект."""

    def __init__(self, position=None, body_color=None):
        """Сохраняет позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект (переопределяется в наследниках)."""

    def draw_cell(self, surface, position, color):
        """Рисует одну клетку заданного цвета."""
        pygame.draw.rect(
            surface,
            color,
            pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        )

    def move(self):
        """Двигает объект (переопределяется в наследниках)."""

    def check_border(self):
        """Проверяет границы поля (переопределяется в наследниках)."""


class Snake(GameObject):
    """Змейка: сегменты, направление и скорость."""

    def __init__(self):
        """Создаёт змейку в центре поля."""
        super().__init__(None, SNAKE_COLOR)
        self.speed = SPEED
        self.reset()
        self.direction = RIGHT

    def draw(self, surface):
        """Рисует сегменты змейки и затирает ушедший хвост."""
        for position in self.positions:
            self.draw_cell(surface, position, self.body_color)
        if self.last is not None:
            self.draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Сдвигает змейку на одну клетку со сквозным проходом краёв."""
        head_x, head_y = self.get_head_position()
       # self.direction = RIGHT
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Применяет отложенное направление."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку в центр поля."""
        self.length = 1
        self.positions = [(
            SCREEN_CENTER_X // GRID_SIZE * GRID_SIZE,
            SCREEN_CENTER_Y // GRID_SIZE * GRID_SIZE)]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None
        self.last = None


class Apple(GameObject):
    """Яблоко: случайная позиция на сетке."""

    def __init__(self):
        """Создаёт яблоко со случайной позицией."""
        super().__init__(None, APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        """Ставит яблоко в свободную случайную клетку поля."""
        if snake_positions is None:
            snake_positions = [SCREEN_CENTER_X, SCREEN_CENTER_Y]
        while True:
            rect_x = randint(0, cell_x - 1) * GRID_SIZE
            rect_y = randint(0, cell_y - 1) * GRID_SIZE
            if (rect_x, rect_y) not in snake_positions:
                self.position = (rect_x, rect_y)
                break

    def draw(self, surface):
        """Рисует яблоко на игровом поле."""
        self.draw_cell(surface, self.position, self.body_color)


def draw_board_border(surface):
    """Рисует рамку вокруг игрового поля."""
    pygame.draw.rect(
        surface,
        BORDER_COLOR,
        pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
        width=4
    )


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и выход из игры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            if event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            if event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            if event.key == pygame.K_EQUALS:
                snake.speed += 15
            if event.key == pygame.K_MINUS and snake.speed > 5:
                snake.speed -= 15


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def main():
    """Запускает основной игровой цикл."""
    snake = Snake()
    apple = Apple()
    font = pygame.font.Font(None, 15)
    screen.fill(BOARD_BACKGROUND_COLOR)
    draw_board_border(screen)
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head_position = snake.get_head_position()   

        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if head_position in snake.positions[1:]:
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)
        speed_text = font.render(f'S: {snake.speed}', True, (FONT_COLOR))
        text = font.render(f'L: {snake.length}', True, (FONT_COLOR))
        screen.blit(speed_text, (10, 10))
        text = font.render(f'L: {snake.length}', True, (FONT_COLOR))
        screen.blit(text, (10, 20))
        draw_board_border(screen)
        pygame.display.update()
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()