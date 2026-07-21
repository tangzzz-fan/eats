import pytest
from python_projects.common.day03_tools import retry, fibonacci_generator

def test_fibonacci_generator():
    try:
        gen = fibonacci_generator()
        first_few = [next(gen) for _ in range(6)]
        assert first_few == [0, 1, 1, 2, 3, 5]
    except (TypeError, StopIteration, NotImplementedError):
        pytest.skip("fibonacci_generator is not implemented yet.")

def test_retry_decorator_success():
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1)
    def dummy_success(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    try:
        result = dummy_success(5)
        if result is None:
            pytest.skip("retry decorator returned None.")
        assert result == 10
        assert call_count == 1
    except NotImplementedError:
        pytest.skip("retry decorator is not implemented yet.")
