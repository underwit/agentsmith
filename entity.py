import config


class Ball:
    def __init__(self, x=0, y=0, radius=config.ENEMY_SIZE,
                 speed=config.ENEMY_SPEED, color=config.ENEMY_COLOR,
                 width=config.SANDBOX_WIDTH, height=config.SANDBOX_HEIGHT):
        """Устанавливаем начальные координаты, радиус и вектор движения."""
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.vx = 0.0
        self.vy = 0.0
        self.width = width
        self.height = height
        self.color = color
        self.view = None

    def setpos(self, x, y):
        if 0 <= x <= self.width:
            self.x = x
        if 0 <= y <= self.height:
            self.y = y

    def setvelocity(self, vx, vy):
        if -1.0 <= vx <= 1.0:
            self.vx = vx
        if -1.0 <= vy <= 1.0:
            self.vy = vy

    def update(self):
        self._move()
        self._bounce_from_wall()

    def _move(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

    def _bounce_from_wall(self):
        # если объект врезается в стену, он от неё отскакивает
        if self.x - self.radius < 0:
            self.vx *= -1.0
            self.x = self.radius + 1
        if self.x + self.radius > self.width:
            self.vx *= -1.0
            self.x = self.width - (self.radius + 1)
        if self.y - self.radius < 0:
            self.vy *= -1.0
            self.y = self.radius + 1
        if self.y + self.radius > self.height:
            self.vy *= -1.0
            self.y = self.height - (self.radius + 1)

    def draw(self, canvas):
        """Отрисовываем объект на холсте."""
        if self.view is None:
            self.view = canvas.create_oval(
                self.x - self.radius,
                self.y - self.radius,
                self.x + self.radius,
                self.y + self.radius,
                fill=self.color
            )
        else:
            canvas.coords(
                self.view,
                self.x - self.radius,
                self.y - self.radius,
                self.x + self.radius,
                self.y + self.radius
            )


def main():
    """Заглушка."""
    pass


if __name__ == '__main__':
    main()
