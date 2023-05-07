""" Tests for the schedulability simulator.

TODO: Further documentation.
"""

from sched.sim import Simulator, Task


def test():
    """
    Simple tests.

    Test some task sets with expected results from literature.
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
    sim = Simulator()
    sim.run(task_set, 60)
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


if __name__ == "__main__":
    test()
