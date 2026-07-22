"""CSV helpers used by the Streamlit app."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_csv_file(file_or_path) -> pd.DataFrame:
    return pd.read_csv(file_or_path)


def load_default_data(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    data_dir = base_dir / "data"
    courses = pd.read_csv(data_dir / "sample_courses.csv")
    rooms = pd.read_csv(data_dir / "sample_rooms.csv")
    slots = pd.read_csv(data_dir / "sample_slots.csv")
    return courses, rooms, slots


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

