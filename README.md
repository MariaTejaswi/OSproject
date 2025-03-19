Advanced Disk Scheduling Simulator
Project Overview
This project implements an Advanced Disk Scheduling Simulator that simulates various disk scheduling algorithms:

FCFS (First Come First Serve)
SSTF (Shortest Seek Time First)
SCAN (Elevator Algorithm)
C-SCAN (Circular SCAN)
The goal of this project is to understand how different disk scheduling algorithms work and compare their efficiency in terms of seek time. The simulator takes user inputs for the initial head position and the request sequence and then executes the selected algorithm to calculate the total seek time and display the order of execution.
Features
✅ Simple input handling for requests and head position
✅ Implementation of four scheduling algorithms:
FCFS
SSTF
SCAN
C-SCAN
✅ Calculation of total seek time for performance comparison
✅ Clear output showing the order of execution
Algorithms Explained
1. FCFS (First Come First Serve)
Processes requests in the order they arrive.
Simple and easy to implement.
2. SSTF (Shortest Seek Time First)
Selects the request closest to the current head position.
Minimizes seek time but can lead to starvation of far-away requests.
3. SCAN (Elevator Algorithm)
Moves the head in one direction, servicing requests along the way.
After reaching the last request in one direction, reverses and services requests in the opposite direction.
4. C-SCAN (Circular SCAN)
Similar to SCAN but after reaching the last request, jumps to the beginning of the disk without reversing.
Technologies Used
Programming Language: C++
Libraries:
<iostream> – for input/output
<vector> – for storing requests
<algorithm> – for sorting and finding minimum values
<cmath> – for calculating absolute values
Execution Plan
Take user input for the number of requests, request values, and initial head position.
Display the menu for algorithm selection.
Execute the selected algorithm:
FCFS
SSTF
SCAN
C-SCAN
Calculate and display total seek time.

