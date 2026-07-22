from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from algorithm.constraints import evaluate_schedule, validate_input_data
from algorithm.graph_builder import build_conflict_graph, graph_summary
from algorithm.scheduler import generate_timetable
from utils.file_handler import dataframe_to_csv_bytes, load_default_data
from utils.styles import (
    dark_table,
    feature_card,
    hero_section,
    inject_custom_css,
    metric_card,
    section_header,
    sidebar_brand,
    status_badges,
)
from utils.visualizer import create_conflict_graph_figure, create_room_utilization_figure


BASE_DIR = Path(__file__).resolve().parent


st.set_page_config(
    page_title="AI Exam Timetable Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_state() -> None:
    if "courses_df" not in st.session_state:
        courses, rooms, slots = load_default_data(BASE_DIR)
        st.session_state.courses_df = courses
        st.session_state.rooms_df = rooms
        st.session_state.slots_df = slots
    if "schedule_result" not in st.session_state:
        st.session_state.schedule_result = None


def reset_to_sample() -> None:
    courses, rooms, slots = load_default_data(BASE_DIR)
    st.session_state.courses_df = courses
    st.session_state.rooms_df = rooms
    st.session_state.slots_df = slots
    st.session_state.schedule_result = None


def clear_all_data() -> None:
    st.session_state.courses_df = pd.DataFrame(
        columns=["course_id", "course_name", "student_groups", "strength"]
    )
    st.session_state.rooms_df = pd.DataFrame(columns=["room_id", "capacity"])
    st.session_state.slots_df = pd.DataFrame(columns=["date", "time_slot"])
    st.session_state.schedule_result = None


def show_metric_cards(metrics: dict) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_card("Total Courses", metrics.get("total_courses", 0))
    with col2:
        metric_card("Total Rooms", metrics.get("total_rooms", 0))
    with col3:
        metric_card("Slots Used", metrics.get("slots_used", 0))
    with col4:
        metric_card("Conflicts Found", metrics.get("conflicts_found", 0))
    with col5:
        metric_card("Room Utilization", f"{metrics.get('room_utilization_percent', 0)}%")


def show_input_health() -> None:
    validation = validate_input_data(
        st.session_state.courses_df,
        st.session_state.rooms_df,
        st.session_state.slots_df,
    )
    if validation.is_valid:
        st.success("Dataset is ready for timetable generation.")
    else:
        st.error("Please fix these input issues before generation.")
        for error in validation.errors:
            st.write(error)


def render_home() -> None:
    hero_section()
    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        feature_card(
            "Conflict-Free Scheduling",
            "Prevents student groups from receiving two exams in the same date-time slot.",
            "01",
        )
    with col2:
        feature_card(
            "Graph Coloring Based Allocation",
            "Models courses as graph nodes and assigns exam slots as colors.",
            "02",
        )
    with col3:
        feature_card(
            "Room and Resource Optimization",
            "Checks room capacity, avoids room clashes, and reports utilization.",
            "03",
        )

    st.write("")
    section_header(
        "Current Dataset Overview",
        "A quick snapshot of the active courses, conflict graph, rooms, and available exam slots.",
    )

    validation = validate_input_data(
        st.session_state.courses_df,
        st.session_state.rooms_df,
        st.session_state.slots_df,
    )
    if validation.is_valid:
        graph = build_conflict_graph(validation.courses)
        summary = graph_summary(graph)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Courses", summary["nodes"])
        col2.metric("Conflict Edges", summary["edges"])
        col3.metric("Graph Density", summary["density"])
        col4.metric("Max Degree", summary["max_degree"])
    else:
        show_input_health()


def render_data_page() -> None:
    section_header(
        "Add / Upload Data",
        "Manage courses, student groups, rooms, capacities, dates, and time slots before running the scheduler.",
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Load Sample Data", use_container_width=True):
            reset_to_sample()
            st.success("Sample data loaded.")
    with col2:
        if st.button("Clear All Data", use_container_width=True):
            clear_all_data()
            st.warning("All tables cleared.")
    with col3:
        show_input_health()

    tab_courses, tab_rooms, tab_slots, tab_upload = st.tabs(
        ["Courses", "Rooms", "Exam Slots", "Upload CSV"]
    )

    with tab_courses:
        left, right = st.columns([0.88, 1.4], gap="large")
        with left:
            with st.container(border=True):
                st.subheader("Add Course")
                st.caption("Separate multiple student groups with semicolons.")
                with st.form("add_course_form", clear_on_submit=True):
                    course_id = st.text_input("Course ID", placeholder="AI201")
                    course_name = st.text_input("Course Name", placeholder="Artificial Intelligence")
                    student_groups = st.text_input("Student Groups", placeholder="AIML-A; AIML-B")
                    strength = st.number_input("Strength", min_value=1, step=1, value=40)
                    submitted = st.form_submit_button("Add Course", use_container_width=True)
                    if submitted:
                        if not course_id.strip() or not student_groups.strip():
                            st.error("Course ID and student groups are required.")
                        else:
                            new_row = pd.DataFrame(
                                [
                                    {
                                        "course_id": course_id,
                                        "course_name": course_name or course_id,
                                        "student_groups": student_groups,
                                        "strength": int(strength),
                                    }
                                ]
                            )
                            st.session_state.courses_df = pd.concat(
                                [st.session_state.courses_df, new_row], ignore_index=True
                            )
                            st.session_state.schedule_result = None
                            st.success("Course added.")
        with right:
            with st.container(border=True):
                st.subheader("Course Table")
                st.session_state.courses_df = st.data_editor(
                    st.session_state.courses_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="courses_editor",
                )

    with tab_rooms:
        left, right = st.columns([0.88, 1.4], gap="large")
        with left:
            with st.container(border=True):
                st.subheader("Add Room")
                st.caption("Capacity must be enough for assigned course strength.")
                with st.form("add_room_form", clear_on_submit=True):
                    room_id = st.text_input("Room ID", placeholder="R101")
                    capacity = st.number_input("Capacity", min_value=1, step=1, value=60)
                    submitted = st.form_submit_button("Add Room", use_container_width=True)
                    if submitted:
                        if not room_id.strip():
                            st.error("Room ID is required.")
                        else:
                            new_row = pd.DataFrame([{"room_id": room_id, "capacity": int(capacity)}])
                            st.session_state.rooms_df = pd.concat(
                                [st.session_state.rooms_df, new_row], ignore_index=True
                            )
                            st.session_state.schedule_result = None
                            st.success("Room added.")
        with right:
            with st.container(border=True):
                st.subheader("Room Table")
                st.session_state.rooms_df = st.data_editor(
                    st.session_state.rooms_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="rooms_editor",
                )

    with tab_slots:
        left, right = st.columns([0.88, 1.4], gap="large")
        with left:
            with st.container(border=True):
                st.subheader("Add Exam Slot")
                st.caption("Each unique date-time pair becomes one graph color.")
                with st.form("add_slot_form", clear_on_submit=True):
                    exam_date = st.date_input("Exam Date")
                    time_slot = st.text_input("Time Slot", placeholder="09:30-12:30")
                    submitted = st.form_submit_button("Add Slot", use_container_width=True)
                    if submitted:
                        if not time_slot.strip():
                            st.error("Time slot is required.")
                        else:
                            new_row = pd.DataFrame(
                                [{"date": str(exam_date), "time_slot": time_slot.strip()}]
                            )
                            st.session_state.slots_df = pd.concat(
                                [st.session_state.slots_df, new_row], ignore_index=True
                            )
                            st.session_state.schedule_result = None
                            st.success("Exam slot added.")
        with right:
            with st.container(border=True):
                st.subheader("Exam Slot Table")
                st.session_state.slots_df = st.data_editor(
                    st.session_state.slots_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="slots_editor",
                )

    with tab_upload:
        with st.container(border=True):
            st.subheader("Upload CSV Files")
            st.caption("Upload one or more CSV files. Existing tables are replaced only for files you select.")
            col1, col2, col3 = st.columns(3)
            uploaded_courses = col1.file_uploader("Courses CSV", type=["csv"], key="upload_courses")
            uploaded_rooms = col2.file_uploader("Rooms CSV", type=["csv"], key="upload_rooms")
            uploaded_slots = col3.file_uploader("Slots CSV", type=["csv"], key="upload_slots")
            if st.button("Apply Uploaded Files", use_container_width=True):
                try:
                    if uploaded_courses is not None:
                        st.session_state.courses_df = pd.read_csv(uploaded_courses)
                    if uploaded_rooms is not None:
                        st.session_state.rooms_df = pd.read_csv(uploaded_rooms)
                    if uploaded_slots is not None:
                        st.session_state.slots_df = pd.read_csv(uploaded_slots)
                    st.session_state.schedule_result = None
                    st.success("Uploaded files applied.")
                except Exception as exc:
                    st.error(f"Could not read uploaded CSV: {exc}")


def render_generate_page() -> None:
    section_header(
        "Generate Timetable",
        "Run the graph-coloring and backtracking search. The algorithm tries the most constrained courses first.",
    )
    validation = validate_input_data(
        st.session_state.courses_df,
        st.session_state.rooms_df,
        st.session_state.slots_df,
    )

    if not validation.is_valid:
        show_input_health()
        return

    graph = build_conflict_graph(validation.courses)
    summary = graph_summary(graph)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Courses", summary["nodes"])
    col2.metric("Conflict Edges", summary["edges"])
    col3.metric("Rooms", len(validation.rooms))
    col4.metric("Available Slots", len(validation.slots))

    with st.container(border=True):
        st.subheader("Search Settings")
        col1, col2 = st.columns(2)
        with col1:
            max_solutions = st.slider("Maximum valid schedules to compare", 1, 500, 100)
        with col2:
            max_nodes = st.slider("Maximum backtracking states", 1000, 250000, 100000, step=1000)

        st.markdown('<div class="big-generate">', unsafe_allow_html=True)
        generate_clicked = st.button(
            "Generate Timetable",
            type="primary",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if generate_clicked:
        with st.spinner("Running graph coloring, backtracking, and constraint checks..."):
            result = generate_timetable(
                st.session_state.courses_df,
                st.session_state.rooms_df,
                st.session_state.slots_df,
                max_solutions=max_solutions,
                max_nodes=max_nodes,
            )
            st.session_state.schedule_result = result

    result = st.session_state.schedule_result
    if result is None:
        st.info("Ready to generate. Click the main button when your input data is finalized.")
    elif result.success:
        st.success(result.message)
        status_badges(
            [
                ("Valid timetable", "status-success"),
                ("Conflict-free", "status-success"),
                ("Rooms assigned", "status-info"),
            ]
        )
        show_metric_cards(result.metrics)
        dark_table(result.schedule)
        st.caption(f"Backtracking states visited: {result.nodes_visited}")
    else:
        st.error(result.message)
        if result.nodes_visited:
            st.caption(f"Backtracking states visited: {result.nodes_visited}")


def render_graph_page() -> None:
    section_header(
        "Conflict Graph",
        "Each node is a course. An edge means two courses have at least one common student group, so they cannot be scheduled in the same slot.",
    )
    validation = validate_input_data(
        st.session_state.courses_df,
        st.session_state.rooms_df,
        st.session_state.slots_df,
    )
    if validation.courses is None:
        st.error("Course data is invalid. Fix courses before drawing the graph.")
        return

    graph = build_conflict_graph(validation.courses)
    summary = graph_summary(graph)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nodes", summary["nodes"])
    col2.metric("Edges", summary["edges"])
    col3.metric("Density", summary["density"])
    col4.metric("Max Degree", summary["max_degree"])

    with st.container(border=True):
        st.subheader("Visual Conflict Map")
        st.caption("Highly connected courses are the hardest to schedule and are handled first by the backtracking search.")
        fig = create_conflict_graph_figure(graph)
        st.pyplot(fig, clear_figure=True, use_container_width=True)


def filter_schedule(schedule_df: pd.DataFrame) -> pd.DataFrame:
    filtered = schedule_df.copy()
    col1, col2, col3 = st.columns(3)

    date_options = ["All"] + sorted(filtered["date"].astype(str).unique().tolist())
    room_options = ["All"] + sorted(filtered["room_id"].astype(str).unique().tolist())
    course_options = ["All"] + sorted(filtered["course_id"].astype(str).unique().tolist())

    selected_date = col1.selectbox("Filter by Date", date_options)
    selected_room = col2.selectbox("Filter by Room", room_options)
    selected_course = col3.selectbox("Filter by Course", course_options)

    if selected_date != "All":
        filtered = filtered[filtered["date"].astype(str) == selected_date]
    if selected_room != "All":
        filtered = filtered[filtered["room_id"].astype(str) == selected_room]
    if selected_course != "All":
        filtered = filtered[filtered["course_id"].astype(str) == selected_course]
    return filtered


def render_results_page() -> None:
    section_header(
        "Results",
        "Review the generated timetable, filter it for presentation, and download the final CSV output.",
    )
    result = st.session_state.schedule_result
    if result is None:
        st.info("Generate a timetable first.")
        return
    if not result.success:
        st.error(result.message)
        return

    st.success(result.message)
    status_badges(
        [
            ("Valid timetable", "status-success"),
            ("Conflict-free", "status-success"),
            ("Room assigned", "status-info"),
        ]
    )
    show_metric_cards(result.metrics)

    with st.container(border=True):
        st.subheader("Timetable Filters")
        filtered_schedule = filter_schedule(result.schedule)
        dark_table(filtered_schedule)

    csv_data = dataframe_to_csv_bytes(result.schedule)
    st.download_button(
        "Download Full Timetable as CSV",
        data=csv_data,
        file_name="generated_exam_timetable.csv",
        mime="text/csv",
        use_container_width=True,
    )

    col1, col2 = st.columns([1.25, 0.9], gap="large")
    with col1:
        with st.container(border=True):
            st.subheader("Room Utilization")
            st.pyplot(create_room_utilization_figure(result.schedule), clear_figure=True, use_container_width=True)
    with col2:
        with st.container(border=True):
            st.subheader("Summary")
            recalculated = evaluate_schedule(result.schedule, result.graph)
            dark_table(pd.DataFrame([recalculated]))


def render_algorithm_page() -> None:
    section_header(
        "Algorithm Analysis",
        "A presentation-ready explanation of how the project maps to DAA concepts.",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        feature_card(
            "Graph Coloring",
            "Courses are vertices. Date-time slots behave like colors. Adjacent courses must receive different colors.",
            "GC",
        )
    with col2:
        feature_card(
            "Backtracking",
            "The scheduler recursively assigns slot-room pairs and reverses choices when a hard constraint fails.",
            "BT",
        )
    with col3:
        feature_card(
            "Constraint Satisfaction",
            "Every assignment must avoid student clashes, room conflicts, capacity violations, and missing values.",
            "CSP",
        )

    st.write("")
    with st.container(border=True):
        st.subheader("Pseudocode")
        st.code(
            """
build conflict graph G from courses
sort courses by decreasing graph degree
best_schedule = none

BACKTRACK(index):
    if all courses are assigned:
        evaluate schedule
        update best valid schedule
        return

    course = ordered_courses[index]
    for each slot in date-time order:
        for each room ordered by best fit:
            if no student clash and room is free and capacity is enough:
                assign course to slot and room
                BACKTRACK(index + 1)
                remove assignment
            """.strip(),
            language="text",
        )

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("Time Complexity")
            st.write(
                "Let C be courses, S be date-time slots, and R be rooms. "
                "Worst-case backtracking explores O((S * R)^C) assignments."
            )
            st.write(
                "With candidate constraint checks against assigned courses, a practical upper bound is O(C * (S * R)^C)."
            )
    with col2:
        with st.container(border=True):
            st.subheader("Space Complexity")
            st.write(
                "The conflict graph uses O(C + E), where E is the number of conflict edges."
            )
            st.write(
                "The recursion stack and current assignment dictionary use O(C) additional space."
            )


def main() -> None:
    initialize_state()
    inject_custom_css()
    sidebar_brand()

    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio(
        "Choose a section",
        [
            "Home",
            "Add / Upload Data",
            "Generate Timetable",
            "Conflict Graph",
            "Results",
            "Algorithm Analysis",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Project Info")
    st.sidebar.caption("Topic: AI-Based Examination Timetable Generator")
    st.sidebar.caption("DAA Concepts: Graph Coloring, Backtracking, CSP")
    st.sidebar.caption("Stack: Python, Streamlit, NetworkX, Pandas")

    if page == "Home":
        render_home()
    elif page == "Add / Upload Data":
        render_data_page()
    elif page == "Generate Timetable":
        render_generate_page()
    elif page == "Conflict Graph":
        render_graph_page()
    elif page == "Results":
        render_results_page()
    elif page == "Algorithm Analysis":
        render_algorithm_page()


if __name__ == "__main__":
    main()
