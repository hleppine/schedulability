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

    # Input attributes:
    name: str
    priority: int
    period: int
    deadline: int
    offset: int
    wcet: int
    # Dynamic attributes:
    response_time: int
    became_ready: int
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
        return (now - self.offset) % self.period == 0

    def next_time_ready(
        self,
        now: int,
    ) -> int:
        """Determine the next time the task becomes ready."""
        return now + self.period - (now - self.offset) % self.period


class Simulator:
    """The schedulability simulator.

    TODO: Extend description.
    """

    timeline: list[tuple[int, int, str]]
    tasks: set[Task]
    now: int

    def __init__(
        self,
    ):
        self.timeline = []
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
        lowest_priority = min(t.priority for t in task_set)
        self.tasks = set(task_set)
        always_ready_task = Task(
            name="Always_Ready_Task",
            priority=lowest_priority - 1,
            period=duration,
            deadline=duration,
            offset=0,
            wcet=duration,
        )
        self.tasks.add(always_ready_task)
        now = 0
        while now < duration:
            # Check which tasks become ready at this time instant.
            # Tasks that have work left remain ready.
            for task in self.tasks:
                if task.state == TaskState.RUNNING:
                    # If a task is currently running, it must have work left.
                    assert task.work_left > 0
                    # Change the currently running task to ready.
                    # It could become running again below.
                    task.state = TaskState.READY
                if task.becomes_ready(now):
                    task.state = TaskState.READY
                    if task.work_left == 0:
                        task.became_ready = now
                    task.work_left += task.wcet
            # Select the next time instant to analyze:
            # A priori it's the next time some task becomes ready.
            # This might be adjusted below if the current task
            # completes its remaining work.
            new_now = duration
            for task in self.tasks:
                task_next_time_ready = task.next_time_ready(now)
                if task_next_time_ready < new_now:
                    new_now = task_next_time_ready
            # Select which task actually runs during the next slice:
            # The task with the highest priority that is ready.
            # Could be the same task that was already running.
            current_task = always_ready_task
            for task in self.tasks:
                if (
                    task.state == TaskState.READY
                    and task.priority > current_task.priority
                ):
                    current_task = task
            current_task.state = TaskState.RUNNING
            slice_len = new_now - now
            if current_task.work_left <= slice_len:
                # Current task finishes its work before/at the new now.
                # Thus we adjust the new now to be the instant
                # when the current task completes its work.
                slice_len = current_task.work_left
                new_now = now + slice_len
                current_task.work_left = 0
                current_task.state = TaskState.IDLE
                new_response_time = new_now - task.became_ready
                if new_response_time > task.response_time:
                    task.response_time = new_response_time
            else:
                # Current task continues to have work after this slice.
                current_task.work_left -= slice_len
            # Add a new slice to the timeline, or extend the current slice.
            if self.timeline and self.timeline[-1][2] == current_task.name:
                self.timeline[-1][1] = new_now
            else:
                self.timeline.append((now, new_now, current_task.name))
            # Advance the simulation to the next interesting time instant.
            now = new_now
        # Once the while loop ends, now must be exactly at duration.
        assert now == duration
