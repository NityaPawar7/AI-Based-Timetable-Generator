# AI-Based Examination Timetable Generator

A complete Design and Analysis of Algorithms project with a Streamlit UI. The system generates conflict-free examination timetables using graph coloring, recursive backtracking, and constraint satisfaction.

## Problem Statement

Manual examination timetable preparation is slow and error-prone when many courses share student groups and rooms have limited capacity. This project automatically creates a valid exam schedule by preventing student clashes, room conflicts, and room capacity violations.

## Syllabus Mapping

- Graph Coloring: Courses are graph nodes. A date-time exam slot is treated as a color.
- Backtracking: The algorithm recursively assigns colors and rooms, then backtracks when a constraint fails.
- Constraint Satisfaction: Every assignment must satisfy student, room, capacity, and completeness constraints.

## Folder Structure

```text
exam-timetable-generator/
|-- app.py
|-- algorithm/
|   |-- graph_builder.py
|   |-- scheduler.py
|   `-- constraints.py
|-- data/
|   |-- sample_courses.csv
|   |-- sample_rooms.csv
|   `-- sample_slots.csv
|-- sample_data/
|   |-- small_courses.csv
|   |-- medium_courses.csv
|   |-- dense_conflicts_courses.csv
|   |-- insufficient_rooms_courses.csv
|   `-- capacity_issue_courses.csv
|-- utils/
|   |-- file_handler.py
|   `-- visualizer.py
|-- tests/
|   `-- test_scheduler.py
|-- README.md
`-- requirements.txt
```

## Input CSV Format

Courses:

```csv
course_id,course_name,student_groups,strength
CS201,Data Structures,AIML-A; CSE-A,64
```

Rooms:

```csv
room_id,capacity
R101,90
```

Slots:

```csv
date,time_slot
2026-07-01,09:30-12:30
```

## Algorithm Used

1. Normalize and validate all course, room, and slot data.
2. Build a conflict graph:
   - Each course is a node.
   - An edge is added when two courses share at least one student group.
3. Sort courses by descending graph degree, so the most constrained courses are scheduled first.
4. Use recursive backtracking:
   - Try each date-time slot as a graph color.
   - Try rooms in best-fit order.
   - Accept an assignment only if every constraint is satisfied.
5. Compare valid schedules using an optimization score:
   - Fewer exam days used is better.
   - Fewer date-time slots used is better.
   - Better room utilization is better.
   - Any hard conflict receives a heavy penalty.

## Constraints Checked

- The same student group cannot have two exams in the same date-time slot.
- The same room cannot be used for two exams in the same date-time slot.
- Room capacity must be greater than or equal to course strength.
- Every course must be assigned exactly one date, time slot, and room.

## Pseudocode

```text
BUILD_GRAPH(courses):
    create empty graph G
    for each course:
        add course as node
    for each pair of courses:
        if they share a student group:
            add edge between them
    return G

GENERATE_TIMETABLE(courses, rooms, slots):
    G = BUILD_GRAPH(courses)
    ordered_courses = courses sorted by descending degree in G
    best_schedule = null

    BACKTRACK(index):
        if index == number of courses:
            evaluate current schedule
            if schedule is valid and better than best_schedule:
                best_schedule = current schedule
            return

        course = ordered_courses[index]
        for each slot in slots:
            for each room in rooms sorted by best fit:
                if CAN_ASSIGN(course, slot, room):
                    assign course to slot and room
                    BACKTRACK(index + 1)
                    remove assignment

    BACKTRACK(0)
    return best_schedule or failure message
```

## Complexity Analysis

Let:

- C = number of courses
- S = number of date-time slots
- R = number of rooms
- E = number of conflict edges

Graph construction compares courses through shared student groups. In the worst case, the conflict graph can have O(C^2) edges.

Backtracking tries up to S * R choices for each course. Therefore, the worst-case time complexity is:

```text
O((S * R)^C)
```

Each constraint check may compare the candidate assignment against already assigned courses, so a practical upper bound is:

```text
O(C * (S * R)^C)
```

Space complexity:

```text
O(C + E)
```

for the graph, plus O(C) for the recursion stack and assignment table.

## How to Run

From the project folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## How to Use the UI

1. Open the Home page to view the current dataset summary.
2. Use Add/View Data to add courses, rooms, and exam slots manually or upload CSV files.
3. Open Conflict Graph to see courses as nodes and student-group conflicts as edges.
4. Open Generate Timetable and click Generate timetable.
5. Open Results & Download to view the final timetable, summary metrics, utilization chart, and CSV download.

## Sample Test Cases

The `sample_data` folder contains five ready-made datasets:

| Case | Purpose | Expected Result |
| --- | --- | --- |
| small | 4 courses with light conflicts | Valid timetable |
| medium | 8 courses with mixed student groups | Valid timetable |
| dense_conflicts | Many courses sharing one group | Valid timetable using separate slots |
| insufficient_rooms | Too few room-slot combinations | No valid timetable |
| capacity_issue | Course strength exceeds all rooms | No valid timetable |

## Running Tests

```bash
pytest
```

The tests verify valid schedules, zero hard conflicts, dense graph behavior, insufficient room handling, room capacity failure, and invalid CSV input handling.

## Output Fields

The generated timetable includes:

- course_id
- course_name
- date
- time_slot
- room_id
- student_groups
- strength
- room_capacity
- room_utilization_percent

## Screenshot Instructions

For a college report or presentation:

1. Run `streamlit run app.py`.
2. Take a screenshot of the Home page with dataset metrics.
3. Take a screenshot of the Add/View Data page showing course, room, and slot tables.
4. Take a screenshot of the Conflict Graph page.
5. Generate a timetable and take a screenshot of the Results & Download page.
6. Add one failure-case screenshot by uploading the capacity issue CSV files from `sample_data`.

