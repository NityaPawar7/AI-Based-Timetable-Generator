# 📅 AI-Based Examination Timetable Generator

An intelligent examination scheduling system that generates conflict-free exam timetables using **Graph Coloring**, **Constraint Satisfaction**, and **Recursive Backtracking**. The application features an interactive Streamlit interface, automated room allocation, CSV-based input validation, and graph visualization for analyzing scheduling conflicts.

---

## 📌 Overview

Creating examination timetables manually is a complex task due to multiple constraints such as overlapping student registrations, room capacities, and scheduling conflicts.

This project models the scheduling problem as a **graph coloring and constraint satisfaction problem**, enabling automated generation of feasible examination schedules while minimizing conflicts and optimizing room allocation.

---

## ✨ Features

- Automated examination timetable generation
- Graph-based conflict detection
- Graph Coloring algorithm implementation
- Recursive Backtracking search
- Constraint Satisfaction approach
- Automatic room allocation
- CSV-based data validation
- Interactive Streamlit interface
- NetworkX conflict graph visualization
- Downloadable timetable output

---

## 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- NetworkX
- Pytest

---

## 🧠 Concepts Demonstrated

- Graph Theory
- Graph Coloring
- Constraint Satisfaction Problems (CSP)
- Recursive Backtracking
- Search Algorithms
- Scheduling Optimization
- Data Validation
- Python Application Development

---

## ⚙ Algorithm Overview

The scheduling workflow consists of:

1. Reading examination and student registration data.
2. Constructing a conflict graph where subjects sharing students are connected.
3. Applying Graph Coloring with Recursive Backtracking to assign non-conflicting time slots.
4. Enforcing scheduling constraints through constraint satisfaction techniques.
5. Allocating examination rooms based on capacity requirements.
6. Validating generated schedules and exporting the final timetable.

---

## 📂 Project Structure

```
.
├──AI-Exam-Timetable-Generator/
│
├── README.md
├── LICENSE
├── requirements.txt
├── app.py
│
├── algorithm/
│   ├── __init__.py
│   ├── constraints.py
│   ├── graph_builder.py
│   └── scheduler.py
│
├── utils/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── styles.py
│   └── visualizer.py
│
├── data/
│   ├── sample_courses.csv
│   ├── sample_rooms.csv
│   └── sample_slots.csv
│
├── sample_data/
│   ├── small_courses.csv
│   ├── small_rooms.csv
│   ├── small_slots.csv
│   ├── medium_courses.csv
│   ├── medium_rooms.csv
│   ├── medium_slots.csv
│   ├── dense_conflicts_courses.csv
│   ├── dense_conflicts_rooms.csv
│   ├── dense_conflicts_slots.csv
│   ├── capacity_issue_courses.csv
│   ├── capacity_issue_rooms.csv
│   ├── capacity_issue_slots.csv
│   ├── insufficient_rooms_courses.csv
│   ├── insufficient_rooms_rooms.csv
│   └── insufficient_rooms_slots.csv
│
├── tests/
│   └── test_scheduler.py
│
└── .streamlit/
    └── config.toml
```



---

## 🚀 Running the Project

1. Clone or download the repository.
2. Install the required dependencies.

```bash
pip install -r requirements.txt
```

3. Launch the Streamlit application.

```bash
streamlit run app.py
```

---

## 📊 Learning Outcomes

This project strengthened my understanding of:

- Graph-based problem modeling
- Constraint Satisfaction Problems
- Recursive search algorithms
- Scheduling optimization
- Streamlit application development
- Data validation and preprocessing
- Software design for algorithmic applications


---

## 👩‍💻 Author

**Nitya R Pawar**

B.E. Artificial Intelligence & Machine Learning  
BMS College of Engineering, Bengaluru

GitHub: https://github.com/NityaPawar7
