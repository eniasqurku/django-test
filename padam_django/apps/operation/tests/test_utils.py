import datetime
from unittest.mock import Mock

from padam_django.apps.operation.utils import is_overlapping


def test_no_shifts_returns_false():
    """Test that an empty queryset returns False"""
    empty_shifts = []
    current_interval = (datetime.time(10, 0), datetime.time(11, 0))
    assert is_overlapping(empty_shifts, current_interval) == False


def test_shifts_with_none_times_returns_false():
    """Test that shifts with None times are effectively ignored"""
    shifts = [
        Mock(start_time=None, finish_time=None),
        Mock(start_time=None, finish_time=None),
    ]
    current_interval = (datetime.time(10, 0), datetime.time(11, 0))
    assert is_overlapping(shifts, current_interval) == False


def test_overlapping_shift_start_inside_existing_shift():
    """Test when current interval's start time is inside an existing shift"""
    shifts = [Mock(start_time=datetime.time(9, 0), finish_time=datetime.time(11, 30))]
    current_interval = (datetime.time(10, 0), datetime.time(12, 0))
    assert is_overlapping(shifts, current_interval) == True


def test_overlapping_shift_end_inside_existing_shift():
    """Test when current interval's end time is inside an existing shift"""
    shifts = [Mock(start_time=datetime.time(11, 0), finish_time=datetime.time(13, 0))]
    current_interval = (datetime.time(9, 0), datetime.time(12, 0))
    assert is_overlapping(shifts, current_interval) == True


def test_no_overlap_before_existing_shift():
    """Test when current interval is completely before an existing shift"""
    shifts = [Mock(start_time=datetime.time(12, 0), finish_time=datetime.time(14, 0))]
    current_interval = (datetime.time(9, 0), datetime.time(11, 0))
    assert is_overlapping(shifts, current_interval) == False


def test_no_overlap_after_existing_shift():
    """Test when current interval is completely after an existing shift"""
    shifts = [Mock(start_time=datetime.time(9, 0), finish_time=datetime.time(11, 0))]
    current_interval = (datetime.time(12, 0), datetime.time(14, 0))
    assert is_overlapping(shifts, current_interval) == False


def test_multiple_shifts_some_overlapping():
    """Test with multiple shifts where some overlap and some don't"""
    shifts = [
        Mock(start_time=datetime.time(9, 0), finish_time=datetime.time(10, 30)),
        Mock(start_time=datetime.time(14, 0), finish_time=datetime.time(16, 0)),
        Mock(start_time=datetime.time(12, 0), finish_time=datetime.time(13, 0)),
    ]
    current_interval = (datetime.time(10, 0), datetime.time(12, 30))
    assert is_overlapping(shifts, current_interval) == True


def test_edge_case_exact_same_times():
    """Test when the current interval exactly matches an existing shift"""
    shifts = [Mock(start_time=datetime.time(10, 0), finish_time=datetime.time(12, 0))]
    current_interval = (datetime.time(10, 0), datetime.time(12, 0))
    assert is_overlapping(shifts, current_interval) == True


def test_edge_case_adjacent_non_overlapping_shifts():
    """Test shifts that are exactly adjacent but not overlapping"""
    shifts = [Mock(start_time=datetime.time(9, 0), finish_time=datetime.time(10, 0))]
    current_interval = (datetime.time(10, 0), datetime.time(12, 0))
    assert is_overlapping(shifts, current_interval) == False
