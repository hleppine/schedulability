""" Tests for the schedulability simulator.

TODO: Further documentation.
"""

from sched.sim import Simulator, Task


def test():
    """
    TODO
    """
    task_set = [
        Task(
            name="a",
            priority=1,
            period=50,
            deadline=50,
            offset=0,
            wcet=12,
        ),
        Task(
            name="b",
            priority=2,
            period=40,
            deadline=40,
            offset=0,
            wcet=10,
        ),
        Task(
            name="c",
            priority=3,
            period=30,
            deadline=30,
            offset=0,
            wcet=10,
        ),
    ]
    sim = Simulator(task_set, 60)
    sim.run()
    expected_timeline = [
        (0, 10, "c"),
        (10, 20, "b"),
        (20, 30, "a"),
        (30, 40, "c"),
        (40, 50, "b"),
        (50, 60, "a"),
    ]
    assert sim.timeline == expected_timeline
    # TODO: Detect the overrun that occurs in this task set
    for item in sim.timeline:
        print(f"{item[0]} .. {item[1]}: {item[2]}")


def test2():
    """
    TODO
    """
    task_set = [
        Task(
            name="a",
            priority=1,
            period=80,
            deadline=80,
            offset=0,
            wcet=40,
        ),
        Task(
            name="b",
            priority=2,
            period=40,
            deadline=40,
            offset=0,
            wcet=10,
        ),
        Task(
            name="c",
            priority=3,
            period=20,
            deadline=20,
            offset=0,
            wcet=5,
        ),
    ]
    sim = Simulator(task_set, 80)
    sim.run()
    expected_timeline = [
        (0, 5, "c"),
        (5, 15, "b"),
        (15, 20, "a"),
        (20, 25, "c"),
        (25, 40, "a"),
        (40, 45, "c"),
        (45, 55, "b"),
        (55, 60, "a"),
        (60, 65, "c"),
        (65, 80, "a"),
    ]
    assert sim.timeline == expected_timeline


if __name__ == "__main__":
    test()
    test2()
