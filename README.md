Hospital Emergency Routing System

Technologies Used: Python (Flask), NetworkX, Matplotlib, HTML, CSS
Algorithms Used: Dijkstra’s, Hamiltonian Cycle (Backtracking), Kruskal’s

📖 Problem Statement

Design a system to determine the fastest and most efficient routes for an ambulance to visit multiple critical hospitals or patients and return to base.

The system should:

Compute shortest paths between all locations.

Suggest an optimized route to visit all hospitals.

Build a minimum-cost emergency network connecting all hospitals.

This simulation helps in real-time emergency management and hospital network optimization.

⚙️ Algorithms Used
Algorithm	Type	Purpose
🚑 Dijkstra’s Algorithm	Greedy	Finds the shortest route from the base hospital to every other location.
🔁 Hamiltonian Cycle (Backtracking)	Backtracking	Ensures the ambulance visits all hospitals exactly once and returns to the starting point.
🧮 Kruskal’s Algorithm	Greedy	Builds a Minimum Spanning Tree (MST) connecting all hospitals with the least total cost.

✅ This project demonstrates a mix of Greedy and Backtracking strategies in a real-world emergency context.

💡 Real-Life Applications

Ambulance routing & dispatch systems in smart cities

Hospital network planning and communication design

Disaster management – optimal paths for medical response

Emergency logistics for medicine and blood transport

🧩 Features

✅ Dark-themed, hospital-inspired UI (red-blue tones)
✅ Dynamic random distance generation between hospitals/patients
✅ Real-time visualization (no images saved)
✅ Clear distinction of algorithms in the visualization:

🔴 Red — Hamiltonian (TSP route)

🔵 Blue — Kruskal MST (network)

🟢 Green — Dijkstra shortest paths
✅ Built with Flask and visualized using NetworkX + Matplotlib

📂 Folder Structure
HOSPITAL_ROUTING_DARK/
│
├── app.py                # Main Flask backend
├── requirements.txt       # Dependencies
│
├── templates/
│   └── index.html         # Web interface
│
├── static/
│   └── style.css          # Dark themed styling
│
└── README.md              # Documentation

🧰 Installation & Setup
1️⃣ Prerequisites

Python 3.8+

pip package manager

2️⃣ Install Required Libraries
pip install flask networkx matplotlib

3️⃣ Run the Application
python app.py

4️⃣ Open in Browser

Visit: http://127.0.0.1:5000

🖥️ Usage

Enter hospital/patient names (comma-separated):

Base Hospital, Patient A, Hospital B, Patient C


Click Compute Routes

The system will:

Generate random distances between locations

Apply Dijkstra, Kruskal, and Hamiltonian algorithms

Display a beautiful interactive graph with colored routes

View the summary panel for algorithm results:

Dijkstra distances

Kruskal MST connections

Hamiltonian (TSP) path and total cost

🎨 Visualization Meaning
Color	Represents	Algorithm
🔴 Red	Optimal round trip (ambulance visiting all locations)	Hamiltonian Cycle
🔵 Blue	Minimal hospital network (infrastructure plan)	Kruskal MST
🟢 Green	Shortest path from base hospital	Dijkstra’s Algorithm
🧮 Example Output

Input:

Base Hospital, Hospital A, Hospital B, Patient X, Patient Y


Output (example):

Shortest Distance (Dijkstra): [0, 18, 22, 34, 45]
MST (Kruskal): Base–A(18), A–B(12), B–X(25), X–Y(15)
TSP (Hamiltonian): Base → A → B → X → Y → Base
Total Cost: 98

🚀 Future Enhancements

Integrate real-time map data (OpenStreetMap / Google Maps)

Add time and traffic constraints

Support multi-ambulance routing

Implement Genetic Algorithm or Ant Colony Optimization for faster large-scale TSP solving
