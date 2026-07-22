from __future__ import annotations

from pathlib import Path

import pandas as pd

from algorithm.graph_builder import build_conflict_graph
from algorithm.scheduler import generate_timetable


SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample_data"


def load_case(case_name: str):
    courses = pd.read_csv(SAMPLE_DIR / f"{case_name}_courses.csv")
    rooms = pd.read_csv(SAMPLE_DIR / f"{case_name}_rooms.csv")
    slots = pd.read_csv(SAMPLE_DIR / f"{case_name}_slots.csv")
    return courses, rooms, slots


def assert_valid_schedule(result, expected_courses: int) -> None:
    assert result.success, result.message
    assert len(result.schedule) == expected_courses
    assert result.schedule["course_id"].is_unique
    assert result.metrics["conflicts_found"] == 0
    assert result.metrics["student_clashes"] == 0
    assert result.metrics["room_conflicts"] == 0
    assert result.metrics["capacity_issues"] == 0


def test_small_dataset_with_four_courses_generates_valid_timetable():
    courses, rooms, slots = load_case("small")
    result = generate_timetable(courses, rooms, slots)
    assert_valid_schedule(result, expected_courses=4)


def test_medium_dataset_with_eight_courses_generates_valid_timetable():
    courses, rooms, slots = load_case("medium")
    result = generate_timetable(courses, rooms, slots, max_solutions=50)
    assert_valid_schedule(result, expected_courses=8)


def test_many_conflicts_dataset_uses_separate_slots_for_clique():
    courses, rooms, slots = load_case("dense_conflicts")
    graph = build_conflict_graph(courses)
    assert graph.number_of_edges() == 10

    result = generate_timetable(courses, rooms, slots)
    assert_valid_schedule(result, expected_courses=5)
    assert result.metrics["slots_used"] == 5


def test_insufficient_rooms_case_returns_clear_failure():
    courses, rooms, slots = load_case("insufficient_rooms")
    result = generate_timetable(courses, rooms, slots)
    assert not result.success
    assert "No valid timetable found" in result.message


def test_room_capacity_issue_case_returns_clear_failure():
    courses, rooms, slots = load_case("capacity_issue")
    result = generate_timetable(courses, rooms, slots)
    assert not result.success
    assert "exceed every room capacity" in result.message


def test_invalid_input_is_reported_without_crashing():
    courses = pd.DataFrame(
        [
            {
                "course_id": "BAD1",
                "course_name": "Invalid Course",
                "strength": 30,
            }
        ]
    )
    rooms = pd.DataFrame([{"room_id": "R1", "capacity": 50}])
    slots = pd.DataFrame([{"date": "2026-07-01", "time_slot": "09:00-12:00"}])

    result = generate_timetable(courses, rooms, slots)
    assert not result.success
    assert "missing columns" in result.message

