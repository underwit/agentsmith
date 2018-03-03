import random
import math


class BrainBase:
    """Класс для работы с нейронной сетью."""

    def __init__(self):
        self.score = 0
        self.synapse = []  # тут храним веса нейронной сети

    def _multiply(self, values, weights):
        """Перемножаем входные значения на соответствующие веса."""
        # никогда так не пишите
        result = [sum(map(lambda a, b: a * b, values, w)) for w in weights]
        return list(map(math.tanh, result))

    def set_shape(self, shape):
        self.shape = shape

    def reset_score(self):
        self.score = 0

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def make_synapse(self):
        """Задаем случайные веса в соответствии с формой сети."""
        layers = iter(self.shape)
        layer1 = next(layers)
        for layer2 in layers:
            l1 = range(layer1)
            l2 = range(layer2)
            w = [[random.random() * 2 - 1 for _ in l1] for _ in l2]
            self.synapse.append(w)
            layer1 = layer2

    def set_synapse(self, synapse):
        self.synapse = synapse

    def get_synapse(self):
        return self.synapse

    def get_input_size(self):
        return self.shape[0]

    def think(self, v):
        """Подаем входные данные и получаем ответ от сети."""
        for s in self.synapse:
            v = self._multiply(v, s)
        return v


def brainfactory(shape):
    """Функция возвращает класс с определенной формой нейронной сети."""
    if not all([isinstance(i, int) for i in shape]):
        raise ValueError("Bad shape")
    shape.append(2)
    return type("Brain", (BrainBase, object), {"shape": shape})


def main():
    """Заглушка."""
    pass


if __name__ == "__main__":
    main()
