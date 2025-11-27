from __future__ import annotations
from utils.tools import get_txt_files, read_input, timing_decorator
from advent_of_code.utils.colors import magenta_color, reset_color
from typing import List
from dataclasses import dataclass, field
from enum import Enum
import abc
from collections import defaultdict, deque

files = get_txt_files(__file__)
#########
# Start #
#########


class ModuleType(Enum):
    CONJUNCTION = "&"
    FLIPFLOP = "%"
    BROADCASTER = "broadcaster"


class State(Enum):
    ON = True
    OFF = False


class Pulse(Enum):
    LOW = True
    HIGH = False


@dataclass
class BaseModule(abc.ABC):
    """Base abstract Module. This must be subclassed."""

    name: str
    outputs: list[str]

    # The manager is set when we pass a Module to the ModuleManager
    manager: ModuleManager | None = None

    def send_pulse(self, high: bool):
        """Sends the required pulse to all output modules"""
        assert (
            self.manager is not None
        )  # we must have a manager, before we can send pulses
        for output_name in self.outputs:
            self.manager.send_pulse(self, output_name, high)

    @abc.abstractmethod
    def receive_pulse(self, sender_name: str, high: bool):
        """Must be implement in subclasses.
        Handle receiving a pulse from another module.
        The implementation should:
        - Update any required internal state
        - Determine the pulse value that should bs subsequently sent
        - Call send_pulse()
        """
        pass


@dataclass
class FlipFlopModule(BaseModule):
    """Flips its own state only when it receives a low pulse.
    When it flips state, it sends this state onto outputs."""

    state = False

    def receive_pulse(self, sender_name: str, high: bool):
        if not high:
            self.state = not self.state
            self.send_pulse(self.state)


@dataclass
class ConjunctionModule(BaseModule):
    """The ConjunctionModule implements NAND (Not AND) logic within our system.
    It stores the last received state of all of its inputs (defaulting to False)."""

    inputs: dict[str, bool] = field(default_factory=lambda: defaultdict(bool))
    high_pulse_sent: int | None = None  # record when the first High pulse was received

    def add_input(self, input_name: str):
        self.inputs[input_name] = False

    def send_pulse(self, high: bool):
        """Override and chain.
        If this is the first time we are sending a high pulse,
        record the index of this pulse. This is required for Part 2."""

        assert self.manager is not None
        # If this module is sending a high pulse for the first time
        if high and self.high_pulse_sent is None:
            # Save the index of this high pulse
            self.high_pulse_sent = self.manager.button_pushes

        return super().send_pulse(high)

    def receive_pulse(self, sender_name: str, high: bool):
        """Updates the last received state from this input.
        Then sends Low ONLY IF ALL input states are High. Otherwise sends High."""
        self.inputs[sender_name] = high
        self.send_pulse(not all(self.inputs.values()))


class BroadcastModule(BaseModule):
    """Sends specified pulse to all outputs."""

    def receive_pulse(self, sender_name: str, high: bool):
        self.send_pulse(high)


class ModuleManager:
    """Perform actions on behalf of the modules.
    Registers itself as the manager of all modules.
    Provides the capability to push the button and run the entire flow."""

    def __init__(self, modules: list[BaseModule]):
        """Initialise a ModuleManager by passing in a collection of Modules.
        Each Module in the collection is associated with this Manager."""

        # Store pulses to be processed, as (sender, output, pulse)
        self._pulses: deque[tuple[str, str, bool]] = deque()

        self.high_pulses = 0  # total high pulses sent by the system
        self.low_pulses = 0  # total low pulses sent by the system
        self.button_pushes = 0  # total number of button pushes

        # Store all modules in the system by name, and map name to Module.
        self.modules: dict[str, BaseModule] = {}

        # Mapping between module names and instances for conjunction modules
        # So that we can determine input modules to the Conjunction modules
        conjunctions: dict[str, ConjunctionModule] = {}

        # Process each module
        for module in modules:
            # This Manager is the module's Manager
            module.manager = self
            self.modules[module.name] = module

            if isinstance(module, BroadcastModule):
                self._broadcaster = module

            elif isinstance(module, ConjunctionModule):
                conjunctions[module.name] = module

        # Gather inputs of each conjunction module
        for name, module in self.modules.items():
            for output_name in module.outputs:
                output = conjunctions.get(output_name, None)
                if output is not None:
                    output.add_input(name)

    def push_button(self):
        """Push the button, which triggers the pulse cascade for the system."""
        self.button_pushes += 1
        self.send_pulse(None, self._broadcaster.name, False)

        # Pulses are sent in the order that they are requested.
        # Note that each call to receive_pulse() will then call a send_pulse()
        # which will enqueue the next pulse.
        # So this loop continues until there are no remaining pulses to process.
        while self._pulses:
            sender_name, output_name, high = self._pulses.popleft()
            self.modules[output_name].receive_pulse(sender_name, high)

    def send_pulse(self, sender: BaseModule | None, output_name: str, high: bool):
        """Increments pulse counter and enqueues a pulse for processing."""
        if high:
            self.high_pulses += 1
        else:
            self.low_pulses += 1

        output = self.modules.get(output_name, None)
        if output is None:
            return
        sender_name = "" if sender is None else sender.name
        self._pulses.append((sender_name, output_name, high))

    def get_module(self, name: str) -> BaseModule:
        module = self.modules.get(name, None)
        if module is None:
            raise ValueError(f"Module {name} does not exist")
        return module

    def get_input_modules(self, output_name: str) -> list[BaseModule]:
        return [
            module for module in self.modules.values() if output_name in module.outputs
        ]


class Puzzle:
    def __init__(self, text_input):
        self.input: List[str] = text_input
        self.modules = self.parse_modules(self.input)
        self.manager = ModuleManager(self.modules)

    def parse_modules(self, lines: list[str]) -> list[BaseModule]:
        """Process the configuration to determine all the input and output modules.
        Then use these to create the ModuleManager."""
        modules: list[BaseModule] = []

        for line in lines:
            module_part, outputs_part = [part.strip() for part in line.split("->")]
            outputs = [part.strip() for part in outputs_part.split(",")]

            if module_part == "broadcaster":
                module = BroadcastModule(module_part, outputs)
            else:
                module_type, module_part = module_part[0], module_part[1:]
                match module_type:  # implement a switch-case
                    case "%":
                        module = FlipFlopModule(module_part, outputs)
                    case "&":
                        module = ConjunctionModule(module_part, outputs)
                    case _:
                        assert False, f"Unknown module type {module_type}"

            modules.append(module)

        return modules

    def solve(self, part):
        if part == 1:
            for _ in range(1000):
                self.manager.push_button()
            return self.manager.high_pulses * self.manager.low_pulses
        if part == 2:
            pass


@timing_decorator
def main(raw, part):
    text_input = read_input(raw)
    input_parsed = [i if i else "" for i in text_input]
    puzzle = Puzzle(input_parsed)
    return puzzle.solve(part)


def run_tests():
    print("\nRunning Tests:")
    assert main(raw=files["test"], part=1) == 32000000
    assert main(raw=files["test2"], part=1) == 11687500
    # assert main(raw=files["test"], part=2) == 167409079868000

    # solutions
    print("\nRunning Solutions:")
    assert main(raw=files["input"], part=1) == 919383692
    # assert main(raw=files["input"], part=2) == 296


def solve():
    print("\nSolving:")
    answer1 = main(raw=files["input"], part=1)
    print(f"Answer part1: {magenta_color}{answer1}{reset_color}")
    # answer2 = main(raw=files["input"], part=2)
    # print(f"Answer part2: {magenta_color}{answer2}{reset_color}")


if __name__ == "__main__":
    run_tests()
    solve()
