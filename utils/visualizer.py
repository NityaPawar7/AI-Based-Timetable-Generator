"""Matplotlib visualizations for the timetable generator."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def create_conflict_graph_figure(graph: nx.Graph):
    fig, ax = plt.subplots(figsize=(10.5, 6.5), facecolor="#0F172A")
    ax.set_facecolor("#0F172A")
    ax.set_title("Course Conflict Graph", color="#F8FAFC", fontsize=16, fontweight="bold", pad=18)

    if graph.number_of_nodes() == 0:
        ax.text(0.5, 0.5, "No courses available", ha="center", va="center", color="#CBD5E1")
        ax.axis("off")
        return fig

    pos = nx.spring_layout(graph, seed=42, k=0.9)
    degrees = dict(graph.degree())
    node_sizes = [900 + degrees[node] * 180 for node in graph.nodes()]
    node_colors = [
        "#38BDF8" if degrees[node] == max(degrees.values(), default=0) else "#6366F1"
        for node in graph.nodes()
    ]

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=0.92,
        edgecolors="#E0F2FE",
        linewidths=1.5,
        ax=ax,
    )
    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color="#F472B6",
        width=2.0,
        alpha=0.68,
        ax=ax,
    )
    nx.draw_networkx_labels(
        graph,
        pos,
        labels={node: node for node in graph.nodes()},
        font_color="white",
        font_size=9,
        font_weight="bold",
        ax=ax,
    )

    edge_labels = {
        (course_a, course_b): ",".join(data.get("conflict_groups", []))
        for course_a, course_b, data in graph.edges(data=True)
    }
    if edge_labels:
        nx.draw_networkx_edge_labels(
            graph,
            pos,
            edge_labels=edge_labels,
            font_size=7,
            font_color="#E0F2FE",
            bbox={"facecolor": "#1E293B", "edgecolor": "#334155", "alpha": 0.85, "pad": 2},
            ax=ax,
        )

    ax.axis("off")
    fig.tight_layout()
    return fig


def create_room_utilization_figure(schedule_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10.5, 4.5), facecolor="#0F172A")
    ax.set_facecolor("#0F172A")
    if schedule_df is None or schedule_df.empty:
        ax.text(
            0.5,
            0.5,
            "Generate a timetable to view utilization",
            ha="center",
            va="center",
            color="#CBD5E1",
        )
        ax.axis("off")
        return fig

    plot_df = schedule_df.copy()
    plot_df["label"] = plot_df["course_id"] + " - " + plot_df["room_id"]
    ax.bar(
        plot_df["label"],
        plot_df["room_utilization_percent"],
        color="#38BDF8",
        edgecolor="#E0F2FE",
        linewidth=0.8,
    )
    ax.axhline(100, color="#F472B6", linewidth=1.2, linestyle="--")
    ax.set_ylabel("Room utilization (%)", color="#CBD5E1")
    ax.set_xlabel("Course - Room", color="#CBD5E1")
    ax.set_ylim(0, max(110, float(plot_df["room_utilization_percent"].max()) + 10))
    ax.tick_params(axis="x", rotation=35, colors="#CBD5E1")
    ax.tick_params(axis="y", colors="#CBD5E1")
    ax.grid(axis="y", color="#334155", alpha=0.42, linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_color("#334155")
    fig.tight_layout()
    return fig
