class ProgressConsole():
    def __init__(self, total_phase: int) -> None:
        self.current_phase = -1
        self.total_phase = total_phase
        self.step_by_phase = []
        self.current_step = []

    def add_new_phase(self, message: str, total_step: int):
        self.current_phase = self.current_phase + 1
        self.step_by_phase.append(total_step)
        self.current_step.append(0)
        print("[{}-{}]-[{}] - {}".format(
            self.current_phase + 1,
            self.total_phase,
            self.step_by_phase[self.current_phase],
            message
        ))

    def add_new_step(self):
        self.current_step[self.current_phase] = self.current_step[self.current_phase] + 1
        print("[{}-{}]-[{}-{}]".format(
            self.current_phase + 1,
            self.total_phase,
            self.current_step[self.current_phase],
            self.step_by_phase[self.current_phase],
        ))
