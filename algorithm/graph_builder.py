"""Conflict graph construction for examination courses."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations

import networkx as nx
import pandas as pd

from algorithm.constraints import normalize_courses_dataframe, split_student_groups


def build_conflict_graph(courses_df: pd.DataFrame) -> nx.Graph:
    """Build an undirected graph where edges mean courses share a student group."""
    courses = normalize_courses_dataframe(courses_df)
    graph = nx.Graph()
    group_to_courses: dict[str, list[str]] = defaultdict(list)

    for _, row in courses.iterrows():
        groups = split_student_groups(row["student_groups"])
        graph.add_node(
            row["course_id"],
            course_name=row["course_name"],
            student_groups=groups,
            strength=int(row["strength"]),
        )
        for group in groups:
            group_to_courses[group].append(row["course_id"])

    for group, course_ids in group_to_courses.items():
        for course_a, course_b in combinations(sorted(course_ids), 2):
            if graph.has_edge(course_a, course_b):
                graph[course_a][course_b]["conflict_groups"].append(group)
            else:
                graph.add_edge(course_a, course_b, conflict_groups=[group])

    for course_a, course_b in graph.edges():
        graph[course_a][course_b]["conflict_groups"] = sorted(
            set(graph[course_a][course_b]["conflict_groups"])
        )

    return graph


def graph_summary(graph: nx.Graph) -> dict[str, int | float]:
    """Return small graph metrics that are useful for the UI and presentation."""
    node_count = graph.number_of_nodes()
    edge_count = graph.number_of_edges()
    density = nx.density(graph) if node_count > 1 else 0.0
    max_degree = max(dict(graph.degree()).values(), default=0)
    return {
        "nodes": node_count,
        "edges": edge_count,
        "density": round(density, 3),
        "max_degree": max_degree,
    }

