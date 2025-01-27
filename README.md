# GUI_Software_Submission_2025

```
Create a fork
Push your code in that repo
Finally create a pull request
```
## docs:

### https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
Hyperloop Control Dashboard - README

Approach and Thought Process
Project Overview
The Hyperloop Control Dashboard is designed to simulate various aspects of a hyperloop system, including monitoring pods, managing energy efficiency, and providing weather-based route monitoring. The app integrates various modules such as Pod Tracker, Route Monitoring, Energy Optimization, Pod Health Insights, and Did You Know? sections. Each section utilizes live data (weather and energy tips) and provides useful insights for controlling and managing the hyperloop pods.

Approach
Pod Tracker:

Generates a random set of data for 5 pods including their current speed, battery percentage, and status (Operational, Maintenance, Docked).
Displays this data in a sortable and filterable table, enabling the user to monitor pod status and performance.

Route Monitoring:

Fetches live weather data using the Weather API for a user-specified city.
Based on the weather conditions, the system suggests safe speed limits for the hyperloop pods to ensure safety during operation.

Energy Optimization:

Fetches a random energy-saving tip from a mock API.
Provides a helpful energy tip to optimize the pod's performance and reduce energy consumption.

Pod Health Insights:

Allows users to compare the health data (speed, battery percentage, and status) of two pods at a time.
Displays a side-by-side comparison of selected pods for better decision-making.

Did You Know?:

Fetches a random fun fact related to hyperloop technology or transportation in general(from a mock API), enhancing the interactive experience for the user.

Thought Process
The key goal of the project is to simulate and provide a user-friendly interface for managing a hyperloop system using real-time data. I used Streamlit, a Python library for creating interactive web apps, to develop the dashboard, as it provides an easy way to display real-time data and visual elements. The requests library is used to fetch live data from APIs, and Pandas helps manage and display tabular data.
