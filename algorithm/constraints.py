"""Validation, constraint checks, and schedule metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


COURSE_COLUMNS = ["course_id", "course_name", "student_groups", "strength"]
ROOM_COLUMNS = ["room_id", "capacity"]
SLOT_COLUMNS = ["date", "time_slot"]


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]
    courses: pd.DataFrame | None = None
    rooms: pd.DataFrame | None = None
    slots: pd.DataFrame | None = None


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with predictable lower_snake_case column names."""
    cleaned = df.copy()
    cleaned.columns = [
        str(column).strip().lower().replace(" ", "_").replace("-", "_")
        for column in cleaned.columns
    ]
    return cleaned


def split_student_groups(value: Any) -> list[str]:
    """Split a group field such as 'AIML-A; CSE-A' into canonical group names."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, (list, tuple, set)):
        raw_items = value
    else:
        raw_text = str(value).replace("|", ";").replace(",", ";")
        raw_items = raw_text.split(";")

    groups: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        group = str(item).strip().upper()
        if group and group not in seen:
            groups.append(group)
            seen.add(group)
    return groups


def normalize_courses_dataframe(courses_df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(courses_df)
    missing = set(COURSE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Courses CSV is missing columns: {', '.join(sorted(missing))}")

    df = df.copy()
    df["course_id"] = df["course_id"].astype(str).str.strip().str.upper()
    df["course_name"] = df["course_name"].astype(str).str.strip()
    df["student_groups"] = df["student_groups"].apply(
        lambda value: "; ".join(split_student_groups(value))
    )
    df["strength"] = pd.to_numeric(df["strength"], errors="coerce")

    errors: list[str] = []
    if df.empty:
        errors.append("Add at least one course.")
    if df["course_id"].eq("").any():
        errors.append("Every course must have a course_id.")
    if df["course_id"].duplicated().any():
        duplicates = sorted(df.loc[df["course_id"].duplicated(), "course_id"].unique())
        errors.append(f"Duplicate course_id values found: {', '.join(duplicates)}")
    if df["student_groups"].eq("").any():
        errors.append("Every course must have at least one student group.")
    if df["strength"].isna().any() or (df["strength"] <= 0).any():
        errors.append("Course strength must be a positive number for every course.")

    if errors:
        raise ValueError(" ".join(errors))

    df["course_name"] = df.apply(
        lambda row: row["course_name"] if row["course_name"] else row["course_id"],
        axis=1,
    )
    df["strength"] = df["strength"].astype(int)
    return df[COURSE_COLUMNS].sort_values("course_id").reset_index(drop=True)


def normalize_rooms_dataframe(rooms_df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(rooms_df)
    missing = set(ROOM_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Rooms CSV is missing columns: {', '.join(sorted(missing))}")

    df = df.copy()
    df["room_id"] = df["room_id"].astype(str).str.strip().str.upper()
    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")

    errors: list[str] = []
    if df.empty:
        errors.append("Add at least one room.")
    if df["room_id"].eq("").any():
        errors.append("Every room must have a room_id.")
    if df["room_id"].duplicated().any():
        duplicates = sorted(df.loc[df["room_id"].duplicated(), "room_id"].unique())
        errors.append(f"Duplicate room_id values found: {', '.join(duplicates)}")
    if df["capacity"].isna().any() or (df["capacity"] <= 0).any():
        errors.append("Room capacity must be a positive number for every room.")

    if errors:
        raise ValueError(" ".join(errors))

    df["capacity"] = df["capacity"].astype(int)
    return df[ROOM_COLUMNS].sort_values("room_id").reset_index(drop=True)


def normalize_slots_dataframe(slots_df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(slots_df)
    missing = set(SLOT_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Slots CSV is missing columns: {', '.join(sorted(missing))}")

    df = df.copy()
    df["date"] = df["date"].astype(str).str.strip()
    df["time_slot"] = df["time_slot"].astype(str).str.strip()

    errors: list[str] = []
    if df.empty:
        errors.append("Add at least one exam date and time slot.")
    if df["date"].eq("").any():
        errors.append("Every slot must have a date.")
    if df["time_slot"].eq("").any():
        errors.append("Every slot must have a time_slot.")

    if errors:
        raise ValueError(" ".join(errors))

    df = df.drop_duplicates(subset=["date", "time_slot"])
    return df[SLOT_COLUMNS].reset_index(drop=True)


def validate_input_data(
    courses_df: pd.DataFrame,
    rooms_df: pd.DataFrame,
    slots_df: pd.DataFrame,
) -> ValidationResult:
    errors: list[str] = []
    courses = rooms = slots = None

    try:
        courses = normalize_courses_dataframe(courses_df)
    except ValueError as exc:
        errors.append(str(exc))

    try:
        rooms = normalize_rooms_dataframe(rooms_df)
    except ValueError as exc:
        errors.append(str(exc))

    try:
        slots = normalize_slots_dataframe(slots_df)
    except ValueError as exc:
        errors.append(str(exc))

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        courses=courses,
        rooms=rooms,
        slots=slots,
    )


def can_assign(
    course_id: str,
    slot_key: str,
    room_id: str,
    assignments: dict[str, dict[str, Any]],
    graph: Any,
    courses_by_id: dict[str, dict[str, Any]],
    rooms_by_id: dict[str, dict[str, Any]],
) -> bool:
    """Check all hard CSP constraints for one candidate assignment."""
    course = courses_by_id[course_id]
    room = rooms_by_id[room_id]

    if int(room["capacity"]) < int(course["strength"]):
        return False

    for assigned_course_id, assigned in assignments.items():
        if assigned["slot_key"] != slot_key:
            continue
        if graph.has_edge(course_id, assigned_course_id):
            return False
        if assigned["room_id"] == room_id:
            return False
    return True


def evaluate_schedule(schedule_df: pd.DataFrame, graph: Any | None = None) -> dict[str, float | int]:
    """Calculate conflicts, utilization, and a demo-friendly fitness score."""
    if schedule_df is None or schedule_df.empty:
        return {
            "total_courses": 0,
            "total_rooms": 0,
            "slots_used": 0,
            "days_used": 0,
            "student_clashes": 0,
            "room_conflicts": 0,
            "capacity_issues": 0,
            "conflicts_found": 0,
            "room_utilization_percent": 0.0,
            "room_waste": 0,
            "fitness_score": 0.0,
        }

    df = schedule_df.copy()
    if "slot_key" not in df.columns:
        df["slot_key"] = df["date"].astype(str) + " | " + df["time_slot"].astype(str)

    student_clashes = 0
    if graph is not None:
        rows_by_course = df.set_index("course_id").to_dict("index")
        for course_a, course_b in graph.edges():
            if course_a in rows_by_course and course_b in rows_by_course:
                if rows_by_course[course_a]["slot_key"] == rows_by_course[course_b]["slot_key"]:
                    student_clashes += 1

    room_conflicts = 0
    for _, group in df.groupby(["slot_key", "room_id"]):
        if len(group) > 1:
            room_conflicts += len(group) - 1

    capacity_issues = int((df["strength"].astype(int) > df["room_capacity"].astype(int)).sum())
    conflicts_found = student_clashes + room_conflicts + capacity_issues

    total_capacity = int(df["room_capacity"].sum())
    total_strength = int(df["strength"].sum())
    utilization = (total_strength / total_capacity * 100) if total_capacity else 0.0
    room_waste = int((df["room_capacity"] - df["strength"]).clip(lower=0).sum())
    days_used = int(df["date"].nunique())
    slots_used = int(df["slot_key"].nunique())

    conflict_penalty = conflicts_found * 25
    day_penalty = max(0, days_used - 1) * 2
    waste_penalty = max(0.0, 100.0 - utilization) * 0.15
    fitness = max(0.0, 100.0 - conflict_penalty - day_penalty - waste_penalty)

    return {
        "total_courses": int(df["course_id"].nunique()),
        "total_rooms": int(df["room_id"].nunique()),
        "slots_used": slots_used,
        "days_used": days_used,
        "student_clashes": int(student_clashes),
        "room_conflicts": int(room_conflicts),
        "capacity_issues": capacity_issues,
        "conflicts_found": int(conflicts_found),
        "room_utilization_percent": round(utilization, 2),
        "room_waste": room_waste,
        "fitness_score": round(fitness, 2),
    }
