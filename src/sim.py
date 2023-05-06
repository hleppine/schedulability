""" A simple schedulability analysis simulator.

The simulator can be used to analyse the schedulability
of task sets with fixed-priority pre-emptive scheduling.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a task in a real-time system.

    Attributes need to be set before running the sim,
    except for response_time, which is set by the sim.
    """

    name: str
    priority: int
    period: int
    deadline: int
    offset: int
    wcet: int
    response_time: int = 0


class Simulator:
    """The schedulability simulator.

    TODO: Extend description.
    """

    timeline: dict[tuple[int, int], Task]
    tasks: set[Task]

    def __init__(
        self,
    ):
        self.timeline = {}
        self.tasks = set()

    def run(
        self,
        task_set: set[Task],
        duration: int,
    ) -> None:
        # Add an "always ready" task to the task set.
        # It has the lowest priority, and measures the amount of free CPU.
        lowest_priority = max(t.priority for t in task_set)
        self.tasks = set(task_set)
        self.tasks.add(
            Task(
                name="Always_Ready_Task",
                priority=lowest_priority + 1,
                period=duration + 1,
                deadline=duration + 1,
                offset=0,
                wcet=duration + 1,
            )
        )
