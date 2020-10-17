import random


class Snake:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.snake = [(rows // 2 - 1, columns // 2 - 1)]
        self.direction = 'right'
        self.snacks = set()
        self.add_snack()
        self.current_score = 0

    def tick(self, direction=None):
        if direction:
            if (self.direction == 'up' and direction != 'down') or \
                    (self.direction == 'down' and direction != 'up') or \
                    (self.direction == 'left' and direction != 'right') or \
                    (self.direction == 'right' and direction != 'left'):
                self.direction = direction
        new_cell = None
        if self.direction == 'right':
            new_cell = (self.snake[0][0], self.snake[0][1] + 1)
        elif self.direction == 'left':
            new_cell = (self.snake[0][0], self.snake[0][1] - 1)
        elif self.direction == 'up':
            new_cell = (self.snake[0][0] - 1, self.snake[0][1])
        elif self.direction == 'down':
            new_cell = (self.snake[0][0] + 1, self.snake[0][1])
        self.snake.insert(0, new_cell)

        # Проверть не съедена ли еда
        if self.snake[0] in self.snacks:
            self.snacks.discard(self.snake[0])
            self.add_snack()
            self.current_score += 1
        else:
            del self.snake[-1]

    def get_board(self):
        # Создаём поле
        board = []
        for row in range(self.rows):
            new_row = []
            for column in range(self.columns):
                if (row, column) in self.snake:
                    new_row.append(1)
                elif (row, column) in self.snacks:
                    new_row.append(2)
                else:
                    new_row.append(0)
            board.append(new_row)
        return board

    def add_snack(self):
        while True:
            new_snack = (random.randrange(0, self.rows - 1),
                         random.randrange(0, self.columns - 1))

            # Проверка на расположение еды внутри змейки/ другой еды
            if new_snack not in self.snake and new_snack not in self.snacks:
                break
        self.snacks.add(new_snack)

    def score(self):
        return self.current_score

    def finish(self):
        if self.snake[0] in self.snake[1:] or self.snake[0][0] < 0 or self.snake[0][0] > self.rows - 1 \
                or self.snake[0][1] < 0 or self.snake[0][1] > self.columns - 1:
            return len(self.snake)
        else:
            return 0
