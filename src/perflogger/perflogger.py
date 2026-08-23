import inspect
import time
import weakref


class PerfLogger:

    _instances = []

    def __init__(self, name=None, tick_func=time.perf_counter, avgs_step=1):

        PerfLogger._instances.append(weakref.ref(self))

        self.name = (
            name if name is not None else inspect.currentframe().f_back.f_code.co_name
        )
        self.tick = tick_func
        self.avgs_step = avgs_step

        self.tags = []
        self.tags_data = {}
        self.avgs = {}
        self._avgs_counter = None

    @classmethod
    def get_all_instances(cls):
        """Return a list of all instances of current class in creation order"""
        cls._instances[:] = [ref for ref in cls._instances if ref() is not None]
        return [ref() for ref in cls._instances]

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
        self.tags_data.setdefault(tag_name, []).append(now - self.tags[-1][1])
        self.tags.append((tag_name, now))

    def _set_averages(self):
        """Compute averages from stored data"""
        self.avgs.clear()
        for name, data in self.tags_data.items():
            self.avgs[name] = sum(data) / len(data)

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
