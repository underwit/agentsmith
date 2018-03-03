import math


def scale(distance, coef=50):
    """Преобразуем дистанцию в сигнал для нейронной сети."""
    return 1.0 / math.exp(distance / coef)


def dist(x1, x2, y1, y2):
    """Дистанция между двумя объектами."""
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def is_collide(x1, x2, y1, y2, r1, r2):
    """Проверяем сталкиваются ли два объекта."""
    d = dist(x1, x2, y1, y2)
    return d <= (r1 + r2)


def angle(x1, x2, y1, y2):
    """Определяем угол между двумя объектами."""
    return (math.atan2(y1 - y2, x1 - x2) / math.pi * 180 + 180) % 360


def sector(angle, spectrum):
    """Определяем сектор по углу."""
    angle = angle % 360
    return int(angle // math.ceil(360 / spectrum))


def main():
    """Заглушка."""
    pass
    # for i in range(1, 600, 10):
    #     print(i, scale(i))
    # print("right: ", angle(0, 1, 0, 0))
    # print("left: ", angle(0, -1, 0, 0))
    # print("top", angle(0, 0, 0, 1))
    # print("bottom", angle(0, 0, 0, -1))


if __name__ == "__main__":
    main()
