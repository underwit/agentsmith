"""Визуализатор работы процесса тестирования одного генотипа."""

import argparse
import json
import tkinter as tk
import brain
import time
import sandbox
import threading
import config


class Window:
    RUN = 0
    STOP = 1
    FINISH = 2

    def __init__(self, sandbox, brain, frame_rate=30):
        self.sandbox = sandbox
        width = self.sandbox.get_width()
        height = self.sandbox.get_height()
        self.brain = brain
        self.root = tk.Tk()
        self.root.title("Neo")
        self.root.geometry("{}x{}".format(width, height))
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._stop)
        self.canvas = tk.Canvas(self.root, width=width, height=height,
                                bg=config.SANDBOX_BACKGROUND_COLOR)
        self.canvas.grid(row=0, column=0)
        self.frame_rate = frame_rate
        self.frame_time = 1.0 / self.frame_rate
        self.state = self.RUN

    def _stop(self):
        self.state = self.STOP
        while self.state != self.FINISH:
            time.sleep(0.1)
        self.root.destroy()

    def _do(self):
        self.sandbox.draw(self.canvas)
        self.canvas.update()
        result = self.sandbox.update(self.brain)
        if not result:
            self.sandbox.prepare()

    def _loop(self):
        while self.state == self.RUN:
            t1 = time.time()
            self._do()
            r = time.time() - t1
            if self.frame_time > r:
                time.sleep(self.frame_time - r)
        self.state = self.FINISH

    def run(self):
        self.sandbox.prepare()
        t = threading.Thread(target=self._loop)
        t.start()
        self.root.mainloop()


def get_args():
    """Получаем настройки из командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализация генетического алгоритма"
    )
    parser.add_argument("brain", type=str, help="Файл с данными")
    parser.add_argument("-b", "--balls", default=None, type=int,
                        help="Количество мячей противников")
    parser.add_argument("-W", "--width", default=None, type=int,
                        help="Ширина комнаты симуляции")
    parser.add_argument("-H", "--height", default=None, type=int,
                        help="Высота комнаты симуляции")
    args = parser.parse_args()
    return args


def read_config(fname):
    """Читаем json конфиг."""
    with open(fname) as f:
        content = f.read()
        data = json.loads(content)
    return data


def main():
    """Альфа."""
    args = get_args()
    data = read_config(args.brain)
    b = brain.BrainBase()
    b.set_shape(data["shape"])
    b.set_synapse(data["best_nn"])
    balls = args.balls if args.balls is not None else data["balls"]
    width = args.width if args.width is not None else data["sandbox_width"]
    height = args.height if args.height is not None else data["sandbox_height"]
    r = sandbox.Sandbox(balls=balls, width=width, height=height)
    window = Window(r, b)
    window.run()


if __name__ == "__main__":
    main()
