import pygame
from random import randint, choice

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
# Скорость движения змейки:
SPEED = 20


class GameObject:
    """Базовый игровой объект."""

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект (переопределяется в наследниках)."""
        pass

    def move(self):
        """Двигает объект (переопределяется в наследниках)."""
        pass

    def check_border(self):
        """Проверяет границы поля (переопределяется в наследниках)."""
        pass


class Snake(GameObject):
    """Змейка: список сегментов, направление движения, скорость."""

    def __init__(self):
        """Создаёт змейку из одного сегмента в центре поля."""
        super().__init__(None, SNAKE_COLOR)
        cell_x = SCREEN_CENTER_X // GRID_SIZE * GRID_SIZE
        cell_y = SCREEN_CENTER_Y // GRID_SIZE * GRID_SIZE
        self.length = 1
        self.positions = [(cell_x, cell_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.speed = SPEED

    def draw(self, surface):
        """Отрисовывает сегменты змейки и затирает хвост."""
        for position in self.positions:
            pygame.draw.rect(
                surface,
                self.body_color,
                pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            )
        if self.last is not None:
            pygame.draw.rect(
                surface,
                BOARD_BACKGROUND_COLOR,
                pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            )

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Сдвигает змейку на одну клетку, сохраняя хвост для затирания."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Применяет выбранное направление."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку: длина 1, центр, случайное направление."""
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
        """Создаёт яблоко и ставит его в случайную позицию."""
        super().__init__(None, APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает яблоко в случайную позицию на сетке."""
        cell_x = SCREEN_WIDTH // GRID_SIZE
        cell_y = SCREEN_HEIGHT // GRID_SIZE
        rect_x = randint(0, cell_x - 1) * GRID_SIZE
        rect_y = randint(0, cell_y - 1) * GRID_SIZE
        self.position = (rect_x, rect_y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        pygame.draw.rect(
            surface,
            self.body_color,
            pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        )


def draw_board_border(surface):
    """Рисует рамку вокруг игрового поля."""
    pygame.draw.rect(
        surface,
        BORDER_COLOR,
        pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
        width=2
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
    """Запускает игру."""
    snake = Snake()
    apple = Apple()
    font = pygame.font.Font(None, 15)
    while True:
        handle_keys(snake)
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)
        draw_board_border(screen)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)
        speed_text = font.render(f"S: {snake.speed}", True, (255, 255, 255))
        screen.blit(speed_text, (10, 10))
        text = font.render(f"L: {snake.length}", True, (255, 255, 255))
        screen.blit(text, (10, 20))
        pygame.display.update()                # показать
        clock.tick(snake.speed)                # скорость


if __name__ == '__main__':
    main()
