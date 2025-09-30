from dramatiq_project.tasks import do_quick, do_slow


def test_do_quick_runs_fast():
    # Just ensure the function runs without error
    do_quick("test-quick")


def test_do_slow_runs():
    do_slow("test-slow", duration=0.1)
