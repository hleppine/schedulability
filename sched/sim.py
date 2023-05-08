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
        self.now = 0
        self.new_now = 0
        self.duration = 0
        self.always_ready_task = Task(
            name="Always_Ready_Task",
            priority=0,
            period=0,
            deadline=0,
            offset=0,
            wcet=0,
        )

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
        self.tasks = set(task_set)
        self.always_ready_task.priority = min(t.priority for t in task_set) - 1
        self.always_ready_task.period = duration
        self.always_ready_task.deadline = duration
        self.always_ready_task.wcet = duration
        self.tasks.add(self.always_ready_task)
        self.duration = duration
        self.now = 0
        self.new_now = 0
        self.current_task = self.always_ready_task
        while self.now < self.duration:
            self.__update_ready_tasks()
            self.__select_next_ready_time()
            self.__select_task_to_run()
            self.__do_work()
        # Once the while loop ends, now must be exactly at duration.
        assert self.now == self.duration

    def __update_ready_tasks(self) -> None:
        # Check which tasks become ready at this time instant.
        # Tasks that have work left remain ready.
        for task in self.tasks:
            if task.state == TaskState.RUNNING:
                # If a task is currently running, it must have work left.
                assert task.work_left > 0
                # Change the currently running task to ready.
                # It could become running again below.
                task.state = TaskState.READY
            if task.becomes_ready(self.now):
                task.state = TaskState.READY
                if task.work_left == 0:
                    task.became_ready = self.now
                task.work_left += task.wcet

    def __select_next_ready_time(self) -> None:
        # Select the next time instant to analyze:
        # A priori it's the next time some task becomes ready.
        # This might be adjusted below if the current task
        # completes its remaining work.
        self.new_now = self.duration
        for task in self.tasks:
            task_next_time_ready = task.next_time_ready(self.now)
            if task_next_time_ready < self.new_now:
                self.new_now = task_next_time_ready

    def __select_task_to_run(self) -> None:
        # Select which task actually runs during the next slice:
        # The task with the highest priority that is ready.
        # Could be the same task that was already running.
        self.current_task = self.always_ready_task
        for task in self.tasks:
            if (
                task.state == TaskState.READY
                and task.priority > self.current_task.priority
            ):
                self.current_task = task
        self.current_task.state = TaskState.RUNNING

    def __do_work(self) -> None:
        slice_len = self.new_now - self.now
        if self.current_task.work_left <= slice_len:
            # Current task finishes its work before/at the new now.
            # Thus we adjust the new now to be the instant
            # when the current task completes its work.
            slice_len = self.current_task.work_left
            self.new_now = self.now + slice_len
            self.current_task.work_left = 0
            self.current_task.state = TaskState.IDLE
            new_response_time = self.new_now - self.current_task.became_ready
            if new_response_time > self.current_task.response_time:
                self.current_task.response_time = new_response_time
        else:
            # Current task continues to have work after this slice.
            self.current_task.work_left -= slice_len
        # Add a new slice to the timeline, or extend the current slice.
        if self.timeline and self.timeline[-1][2] == self.current_task.name:
            item = self.timeline[-1]
            self.timeline[-1] = (item[0], self.new_now, item[2])
        else:
            self.timeline.append((self.now, self.new_now, self.current_task.name))
        # Advance the simulation to the next interesting time instant.
        self.now = self.new_now
