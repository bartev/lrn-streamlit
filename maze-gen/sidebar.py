import streamlit as st
from matplotlib.figure import Figure
from py_wanderer import ALGORITHMS, HEURISTICS
from py_wanderer.plotter import plot_maze_with_paths

from utils import generate_maze, solve_maze, MazeConfig


def configure_page() -> None:
    st.set_page_config(page_title="Maze and Pathfinding Visualizer", layout="wide")


def configure_overview() -> None:
    st.markdown("## Overview")
    st.markdown(
        "This app generates a maze and visualizes the pathfinding algorithms solving it."
    )
    st.markdown(
        "The aim is to compare the performance of different algorithms and heuristics."
    )


def configure_available_algo_heuristics() -> None:
    st.markdown("## Algorithms and Heuristics")
    st.markdown("The following algorithms and heuristics are available:")

    with st.expander("Algorithms and Heuristics"):
        left, right = st.columns(2)
        left.markdown("### Algorithms")
        for algorithm in ALGORITHMS:
            left.markdown(f"- {algorithm.__name__}")

        right.markdown("### Heuristics")
        for heuristic in HEURISTICS:
            right.markdown(f"- {heuristic.__name__.title()}")


def configure_sidebar() -> MazeConfig:
    seed = st.sidebar.number_input("Seed", 0, 10, 0)
    width = st.sidebar.slider("Width", 5, 25, 11)
    height = st.sidebar.slider("Height", 5, 25, 11)
    num_rooms = st.sidebar.slider("Number of rooms", 0, 5, 0)
    room_size_range = st.sidebar.slider(
        "Room size range", 1, min(width, height) // 4, (3, 6)
    )
    return MazeConfig(seed, width, height, num_rooms, room_size_range)


def create_plot(maze_config: MazeConfig) -> Figure:
    maze = generate_maze(
        maze_config.seed,
        maze_config.width,
        maze_config.height,
        maze_config.num_rooms,
        maze_config.room_size_range,
    )
    paths = solve_maze(maze, ((ALGORITHMS[0], HEURISTICS[0]),))
    fig = plot_maze_with_paths(maze, paths)
    return fig


def main() -> None:
    configure_page()
    configure_overview()
    configure_available_algo_heuristics()
    maze_config = configure_sidebar()
    fig = create_plot(maze_config)
    st.pyplot(fig)


if __name__ == "__main__":
    main()
