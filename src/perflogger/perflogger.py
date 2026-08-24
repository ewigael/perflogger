import inspect
import time

from os import PathLike
from pathlib import Path
import jsonlines

from .logger import Logger


class PerfLogger(Logger):

    def __init__(
        self,
        name: str | None = None,
        tick_func=time.perf_counter,
        avgs_step: int | float = 1,
        output_file_path: str | PathLike | None = None,
    ):
        super().__init__()

        self.name = (
            name if name is not None else inspect.currentframe().f_back.f_code.co_name
        )
        self.tick = tick_func
        self.avgs_step = avgs_step
        self.output_file_path = Path(output_file_path) if output_file_path else None

        self.tags = []
        self.tags_data = {}
        self.avgs = {}
        self._avgs_counter = None

    def start(self):
        """Clear the tags table and init a start tag"""
        self.clear()
        self.tags = [("start", self.tick())]

    def clear(self):
        """Clear the tags table"""
        self.tags.clear()

    def add(self, tag_name):
        """Add a new tag in the tags table as the delta between now and last tag;
        append that delta to the tags_data table to later compute averages"""
        now = self.tick()
        delta = now - self.tags[-1][1]
        if self.output_file_path is not None:
            self.write_to_file(tag_name, now, delta)
        self.tags_data.setdefault(tag_name, []).append(delta)
        self.tags.append((tag_name, now))

    def _set_averages(self):
        """Compute averages from stored data"""
        self.avgs.clear()
        for name, data in self.tags_data.items():
            self.avgs[name] = sum(data) / len(data)

    def _write_to_file(self, lines):
        with self._get_write_lock(self.output_file_path):
            with jsonlines.open(self.output_file_path, "a") as file:
                file.write(lines)

    def write_to_file(self, tag_name, value, delta):
        line = {
            "logger_name": self.name,
            "logger_class": type(self).__name__,
            "value_name": tag_name,
            "value_plain": value,
            "value_delta": delta,
        }
        self._write_to_file(line)

    def get_deltas(self):
        """Return deltas stored in the tags table both in a human readable format and true float"""

        # Black/PEP8 does us dirty here so here's the same code in a more leggible format
        # return [
        #     (
        #         name,
        #              f"{vs[-1]:.2f}s" if vs[-1] >= 1
        #         else f"{vs[-1] * 1e3:.2f}ms" if vs[-1] >= 1e-3
        #         else f"{vs[-1] * 1e6:.2f}μs" if vs[-1] >= 1e-6
        #         else f"{vs[-1] * 1e9:.2f}ns",
        #         vs[-1]
        #     ) for name, vs in self.tags_data.items()
        # ]

        return [
            (
                name,
                (
                    f"{vs[-1]:.2f}s"
                    if vs[-1] >= 1
                    else (
                        f"{vs[-1] * 1e3:.2f}ms"
                        if vs[-1] >= 1e-3
                        else (
                            f"{vs[-1] * 1e6:.2f}μs"
                            if vs[-1] >= 1e-6
                            else f"{vs[-1] * 1e9:.2f}ns"
                        )
                    )
                ),
                vs[-1],
            )
            for name, vs in self.tags_data.items()
        ]

    def get_averages(self):
        if self._avgs_counter is None:
            self._avgs_counter = self.tick()

        if self.tick() - self._avgs_counter >= self.avgs_step:
            self._set_averages()
            self.tags_data.clear()
            self._avgs_counter = self.tick()

        # Black/PEP8 does us dirty here so here's the same return value in more legible code
        # return [
        #     (
        #         name,
        #              f"{vs:.2f}s" if vs >= 1
        #         else f"{vs * 1e3:.2f}ms" if vs >= 1e-3
        #         else f"{vs * 1e6:.2f}μs" if vs >= 1e-6
        #         else f"{vs * 1e9:.2f}ns",
        #         vs
        #     ) for name, vs in self.avgs.items()
        # ]

        return [
            (
                name,
                (
                    f"{vs:.2f}s"
                    if vs >= 1
                    else (
                        f"{vs * 1e3:.2f}ms"
                        if vs >= 1e-3
                        else f"{vs * 1e6:.2f}μs" if vs >= 1e-6 else f"{vs * 1e9:.2f}ns"
                    )
                ),
                vs,
            )
            for name, vs in self.avgs.items()
        ]
