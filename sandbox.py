import random
import entity
import utils
import config


class Sandbox:
    def __init__(self, width=config.SANDBOX_WIDTH, balls=config.BALLS,
                 height=config.SANDBOX_HEIGHT, limit=config.SCORE_LIMIT):
        self.width = width
        self.height = height
        self.limit = limit
        self.balls = []
        # заполняем комнату противниками
        for _ in range(balls):
            e = entity.Ball(width=width, height=height)
            self.balls.append(e)
        # создаем нашего агента
        self.agent = entity.Ball(
            width=width,
            height=height,
            speed=config.AGENT_SPEED,
            radius=config.AGENT_SIZE,
            color=config.AGENT_COLOR
        )
        self.run = False

    def _prepare(self):
        """Подготавливаем комнату перед очередной симуляцией."""
        self.run = True
        self.agent.setpos(self.width // 2, self.height // 2)
        self.agent.setvelocity(0.0, 0.0)
        for b in self.balls:
            while True:
                b.setpos(random.randint(0, self.width),  # X
                         random.randint(0, self.height))  # Y
                if not self._check_collision(self.agent, b):
                    break
            b.setvelocity(random.random() * 2 - 1, random.random() * 2 - 1)

    def _check_collision(self, a, b):
        return utils.is_collide(a.x, b.x, a.y, b.y, a.radius, b.radius)

    def _balls_update(self):
        for ball in self.balls:
            ball.update()
            if self._check_collision(self.agent, ball):
                self.run = False
                return

    def _radar(self, spectrum):
        r = [0] * spectrum
        for b in self.balls:
            angle = utils.angle(self.agent.x, b.x, self.agent.y, b.y)
            distance = utils.dist(self.agent.x, b.x, self.agent.y, b.y)
            r[utils.sector(angle, spectrum)] += utils.scale(distance)
        # передаем на вход сети сигналы от стен, чтобы агент не прилипал к краю
        r[utils.sector(0, spectrum)] += utils.scale(self.width - self.agent.x)
        r[utils.sector(90, spectrum)] += utils.scale(self.height - self.agent.y)
        r[utils.sector(180, spectrum)] += utils.scale(self.agent.x)
        r[utils.sector(270, spectrum)] += utils.scale(self.agent.y)
        return r

    def _update(self, brain):
        self._balls_update()
        spectrum = brain.get_input_size()
        input_vector = self._radar(spectrum)
        vx, vy = brain.think(input_vector)
        self.agent.setvelocity(vx, vy)
        self.agent.update()
        return self.run

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def prepare(self):
        self._prepare()

    def update(self, brain):
        return self._update(brain)

    def draw(self, canvas):
        self.agent.draw(canvas)
        for b in self.balls:
            b.draw(canvas)

    def simulate(self, brain):
        self._prepare()
        c = 0
        while self.run and c < self.limit:
            self._update(brain)
            c += 1
        return c


def main():
    """Заглушка."""
    pass


if __name__ == "__main__":
    main()
