# FBref 2026 World Cup Stats Dashboard

## Overview
An interactive analytics hub built to track elite international performers, compare top nations, and explore premium football data visualizations from the 2026 World Cup. The application provides a seamless, responsive dark-mode UI with "glass-card" styling for an optimal viewing experience.

## Features
* **Player & Team Leaderboards:** Track the highest performers across goals, assists, tackles, and saves.
* **Interactive Visualizations:** Dynamically generated 3D scatter plots, player heatmaps, and team-contribution pie charts using Plotly.
* **Live FBref Scouting:** Real-time data retrieval and metric calculations for players and goalkeepers.
* **Custom UI:** Beautifully styled frontend with dynamic country flag mapping and responsive data grids.

## Project Structure
The repository is organized as follows:
* `main.py`: The core Streamlit application script[cite: 2].
* `pyproject.toml`: Defines the project dependencies and Python version requirements[cite: 2].
* `uv.lock`: Ensures strict, reproducible package resolution[cite: 2].
* `run_app.bat`: A batch script for executing the application locally in Windows environments[cite: 2].
* `.streamlit/config.toml`: Contains the custom configuration and thematic settings for the Streamlit interface[cite: 2].
* `downloaded_files/`: A directory storing cache or driver files, including `driver_fixing.lock`[cite: 2].
* `.idea/`: Configuration files for IDE environments like PyCharm[cite: 2].

## Getting Started

### Prerequisites
Ensure you have Python 3.13+ installed and a package manager like `uv` for handling the dependencies. 

### Installation
1. Clone the repository.
2. Install the required dependencies using the configuration in `pyproject.toml`[cite: 2].

### Running the App
For Windows users, you can launch the dashboard immediately by double-clicking the `run_app.bat` file[cite: 2]. 
Alternatively, run the following command in your terminal:
```bash
streamlit run main.py
