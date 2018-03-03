"""Программа оптимизаци нейронной сети."""

import config
import brain
import gena
import sandbox
import copy
import json
import argparse
import random
from datetime import datetime


MTS = {"gauss": random.gauss, "normal": random.normalvariate}


def get_args():
    """Получаем настройки из командной строки."""
    parser = argparse.ArgumentParser(
        description="Простой генетический алгоритм"
    )
    parser.add_argument(
        "-s", "--shape",
        nargs="+",
        type=int,
        default=config.NN_SHAPE,
        help="Форма нейронной сети"
    )
    parser.add_argument(
        "--no-mutate",
        action="store_true",
        help="Отменить мутации новых особей"
    )
    parser.add_argument(
        "-M", "--mutate-func",
        type=str,
        default=config.MUTATE_FUNC,
        choices=list(MTS),
        help="Функция мутации генов"
    )
    parser.add_argument(
        "-F", "--mutate-fraction",
        type=float,
        default=config.MUTATE_FRACTION,
        help="Доля мутируемых генов"
    )
    parser.add_argument(
        "-D", "--mutate-deviation",
        type=float,
        default=config.MUTATE_DEVIATION,
        help="Отклонение при мутации"
    )
    parser.add_argument(
        "-L", "--score-limit",
        type=int,
        default=config.SCORE_LIMIT,
        help="Лимит необходимых очков"
    )
    parser.add_argument(
        "-b", "--balls",
        type=int,
        default=config.BALLS,
        help="Количество мячей противников"
    )
    parser.add_argument(
        "-p", "--population-size",
        type=int,
        default=config.POPULATION_SIZE,
        help="Количество особей в популяции"
    )
    parser.add_argument(
        "-c", "--childs",
        type=int,
        default=config.CHILDS,
        help="Количество новых детей"
    )
    parser.add_argument(
        "-g", "--generation-count",
        type=int,
        default=config.GENERATION_COUNT,
        help="Количество поколений"
    )
    parser.add_argument(
        "-W", "--sandbox-width",
        type=int,
        default=config.SANDBOX_WIDTH,
        help="Ширина комнаты симуляции"
    )
    parser.add_argument(
        "-H", "--sandbox-height",
        type=int,
        default=config.SANDBOX_HEIGHT,
        help="Высота комнаты симуляции"
    )
    parser.add_argument(
        "-r", "--random-state",
        type=int,
        default=config.RANDOM_STATE,
        help="Начальное состояние генератора случайных чисел"
    )
    args = parser.parse_args()
    return args


def main():
    """Альфа."""
    args = get_args()

    for k, v in args.__dict__.items():
        print("{:20}: {}".format(k, v))
    print("\nStarting...\n")

    try:
        run(args)
    except KeyboardInterrupt:
        print("Exit...")


def savenn(ga, data):
    """Сохраняем в json все настройки и лучшую нейронную сеть."""
    fname = "{}_{}_{}.json".format("-".join(map(str, data["shape"])),
                                   ga.get_best_score(),
                                   datetime.now().strftime("%d%m%Y_%H%M"))
    b = ga.get_best_brain()
    data["best_nn"] = b.synapse
    data["best_score"] = ga.get_best_score()
    data_str = json.dumps(data)
    with open(fname, "w") as f:
        f.write(data_str)
        print("file writed {}".format(fname))


def run(args):
    """Запускаем процесс оптимизации нейронной сети средствами ГА."""
    data = copy.copy(args.__dict__)

    if args.random_state is not None:
        random.seed(args.random_state)

    if not args.no_mutate:
        mutator = gena.mutagen(
            frac=args.mutate_fraction,
            mutator=lambda x: MTS[args.mutate_func](x, args.mutate_deviation)
        )

    brain_cls = brain.brainfactory(args.shape)
    sandbox_obj = sandbox.Sandbox(
        width=args.sandbox_width,
        height=args.sandbox_height,
        balls=args.balls,
        limit=args.score_limit
    )

    ga = gena.Darwin(brain_cls, sandbox_obj, size=args.population_size,
                     childs=args.childs, mutator=mutator)

    for _ in range(args.generation_count):
        ga.fit()
        print(ga)
        s = ga.get_best_score()
        if s < args.score_limit:
            ga.selection()
            continue
        else:
            break
    savenn(ga, data)


if __name__ == "__main__":
    main()
