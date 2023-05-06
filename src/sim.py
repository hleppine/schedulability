""" A simple schedulability analysis simulator.

The simulator can be used to analyse the schedulability
of task sets with fixed-priority pre-emptive scheduling.
"""


class Task:
    name: str
    priority: int
    period: int
    deadline: int
    offset: int
    wcet: int
    response_time: int

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


class Simulator:
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
        lowest_prio = max([t.priority for t in task_set])
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
