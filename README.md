# Maze Runner Game – Advanced Pathfinding in Python

A comprehensive maze simulation and pathfinding project developed in Python using object-oriented design.

This system can read maze configurations, simulate exploration, compute optimal paths, and generate performance statistics.

---

## 📌 Project Overview

The project models a 2D grid maze environment where a runner navigates through walls and open paths using multiple algorithms.

It supports:

- Reading and parsing maze files
- Handling arbitrary maze dimensions
- Wall detection and boundary management
- Exploration logging
- Shortest-path computation
- Performance comparison between algorithms

---

## 🧩 Core Functionality (Basic Implementation)

### 🔹 Maze Modelling
- Grid-based maze representation
- Internal horizontal and vertical walls
- Boundary wall handling
- Dynamic maze size support

### 🔹 File Parsing
- Reads maze configuration from file input
- Constructs maze programmatically
- Supports different maze layouts

### 🔹 Runner Navigation
- Orientation-based movement (N, E, S, W)
- Wall sensing (left, front, right)
- Forward, turn, and backtracking movement logic

### 🔹 Exploration System
- Left-wall (wall-hug) exploration strategy
- Step-by-step movement tracking
- Exploration log generation
- Position and orientation tracking

### 🔹 Path Optimisation
- Loop detection and removal
- Cleaned minimal traversal path
- Path reconstruction

---

## 🚀 Extension: Advanced Pathfinding Algorithms

### 🔹 Breadth-First Search (BFS)
- Guaranteed shortest path in unweighted mazes

### 🔹 Dijkstra’s Algorithm
- Computes optimal path in weighted environments
- Priority-based node expansion

### 🔹 A* Search (Manhattan Heuristic)
- Heuristic-guided optimal search
- Uses Manhattan distance for grid optimisation
- Improves efficiency over Dijkstra in large mazes

---

## 📊 Statistics & Output

The system can:

- Report total exploration steps
- Compare exploration vs shortest-path steps
- Output movement logs
- Analyse path efficiency

---

## 🧠 Algorithms Implemented

| Algorithm | Purpose |
|------------|----------|
| Left-wall (Wall-hug) | Exploration strategy |
| BFS | Shortest path (unweighted) |
| Dijkstra | Weighted shortest path |
| A* (Manhattan) | Heuristic-based optimal search |

---

## 🏗 Project Structure
