""" A simple schedulability analysis simulator.

The simulator can be used to analyse the schedulability
of task sets with fixed-priority pre-emptive scheduling.
"""

from typing import Optional


class Task:  # pylint: disable=too-few-public-methods
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
    response_time: Optional[int]
    last_time_ready: int

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        priority: int,
        period: int,
        deadline: int,
        offset: int,
        wcet: int,
    ):
        self.name = name
        self.priority = priority
        self.period = period
        self.deadline = deadline
        self.offset = offset
        self.wcet = wcet

        self.response_time = None
        self.last_time_ready = offset

    def next_time_ready(
        self,
        now: int,
    ) -> int:
        """Determine the next time the task becomes ready.

        Updates the latest time the task became ready.
        """
        if now > self.last_time_ready:
            self.last_time_ready += self.period
            assert now <= self.last_time_ready
        return self.last_time_ready


class Simulator:  # pylint: disable=too-few-public-methods
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
        """Run the simulator.

        Runs the simulator with the given task set for the specified duration.
        Simulation starts at t=0.
        """
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
