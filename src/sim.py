""" A simple schedulability analysis simulator.

The simulator can be used to analyse the schedulability
of task sets with fixed-priority pre-emptive scheduling.
"""

from enum import Enum


class TaskState(Enum):
    """Task state.

    An idle task has no work to perform.
    A ready task has work to perform and is waiting
    for its turn to run.
    A running task currently performs its work.
    Only one task can be running at a time.
    """

    IDLE = 0
    READY = 1
    RUNNING = 2


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
    response_time: int
    last_time_ready: int
    state: TaskState
    work_left: int

    def __init__(
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

        self.response_time = 0
        self.state = TaskState.IDLE
        self.work_left = 0

    def becomes_ready(
        self,
        now: int,
    ) -> bool:
        """Returns True if the task becomes ready at the given now."""
        return (now - offset) % period == 0

    def next_time_ready(
        self,
        now: int,
    ) -> int:
        """Determine the next time the task becomes ready."""
        return now + period - (now - offset) % period





class Simulator:
    """The schedulability simulator.

    TODO: Extend description.
    """

    timeline: dict[tuple[int, int], Task]
    tasks: set[Task]
    now: int

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
        now = 0
        # Add an "always ready" task to the task set.
        # It has the lowest priority, and measures the amount of free CPU.
        lowest_priority = max(t.priority for t in task_set)
        self.tasks = set(task_set)
        self.tasks.add(
            Task(
                name="Always_Ready_Task",
                priority=lowest_priority + 1,
                period=duration,
                deadline=duration,
                offset=0,
                wcet=duration,
            )
        )
        while self.now <= duration:
            for task in self.tasks:

                if task.becomes_ready(now):
                    task.state = TaskState.READY
                    task.work_left += task.wcet
                

