import config
import random


class Darwin:
    """Класс отвечающий за генетический алгоритм."""

    def __init__(self, brain_cls, sandbox, size=config.POPULATION_SIZE,
                 childs=config.CHILDS, mutator=None):
        self.brain_cls = brain_cls  # класс из которого создаются НС
        self.sandbox = sandbox  # комната для симуляции (тестирования) НС
        self.size = size  # размер популяции
        self.childs = childs  # количество новых потомков от пары родителей
        self.mutator = mutator  # функция мутации генов
        self.population = []
        self.generation_count = 0  # счетчик поколений
        self.best_score = 0  # результат самого лучшего генотипа
        self.last_score = 0  # лучший результат генотипа последнего поколения
        self.best_brains = []  # сохраняем лучшие генотипы
        self.best_brain = None  # последний лучший генотип
        self._fill()

    def __str__(self):
        """Вывод текущих значений."""
        msg = "Generation: {:6}, Last: {:6}, Mean: {:6}, Best: {:6}"
        return msg.format(self.generation_count,
                          self.last_score,
                          self._get_mean(),
                          self.best_score)

    @classmethod
    def _cross(cls, a, b):
        """Скрещивает случайным образом два генотипа."""
        out = []
        if isinstance(a, list) and isinstance(b, list):
            for _a, _b in zip(a, b):
                out.append(cls._cross(_a, _b))
            return out
        return random.choice((a, b))

    def _get_best(self):
        """После тестирования вычисляем лучший генотип."""
        self.population.sort(key=lambda x: x.get_score(), reverse=True)
        b = self.population[0]
        self.last_score = b.get_score()
        if self.last_score > self.best_score:
            self.best_score = self.last_score
            self.best_brain = b
        self.best_brains.append(b)

    def _get_mean(self):
        s = sum([i.get_score() for i in self.population])
        return int(s / len(self.population))

    def _fill(self):
        """Создаем начальную популяцию со случайными значениями."""
        for i in range(self.size):
            b = self.brain_cls()
            b.make_synapse()
            self.population.append(b)

    def _crossing(self, a, b):
        """Создаем и возвращаем новый генотип путем скрещивания двух других."""
        n = self.brain_cls()
        n.set_synapse(self._cross(a.get_synapse(), b.get_synapse()))
        return n

    def get_best_score(self):
        return self.best_score

    def get_best_brain(self):
        return self.best_brain

    def fit(self):
        """Поочередно тестируем генотипы текущей популяции."""
        for b in self.population:
            b.reset_score()
            score = self.sandbox.simulate(b)
            b.set_score(score)
        self._get_best()

    def selection(self):
        """Создаем новыую популяцию на основе лучших генотипов текущей."""
        pop_it = iter(self.population)
        newpop = []
        a = next(pop_it)
        for b in pop_it:
            for c in range(self.childs):
                n = self._crossing(a, b)
                if self.mutator is not None:
                    self.mutator(n.get_synapse())
                newpop.append(n)
            a = b
            if len(newpop) >= self.size:
                break
        self.population = newpop
        self.generation_count += 1


def mutagen(frac=config.MUTATE_FRACTION, mutator=lambda x: x):
    """Функция случайным образом меняет заданную долю генов."""
    def mutate(a):
        if isinstance(a, list):
            if not isinstance(a[0], list):
                for i, v in enumerate(a):
                    if random.random() <= frac:
                        a[i] = mutator(v)
            for i in a:
                mutate(i)
    return mutate


def main():
    """Заглушка."""
    pass


if __name__ == "__main__":
    main()
