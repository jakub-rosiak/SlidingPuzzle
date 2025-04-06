import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Function to parse the filename and extract metadata
def parse_filename(filename):
    # Pattern: [width]x[height]_[depth]_[grid_id]_[algorithm]_[move_order]_stats.txt
    pattern = r"(\d+)x(\d+)_(\d+)_(\d+)_(\w+)_(\w+)_stats\.txt"
    match = re.match(pattern, filename)

    if match:
        width, height, depth, grid_id, algorithm, algorithm_options = match.groups()
        return {
            'width': int(width),
            'height': int(height),
            'depth': int(depth),
            'grid_id': int(grid_id),
            'algorithm': algorithm,
            'algorithm_options': algorithm_options
        }
    return None


# Function to read the content of a stats file
def read_stats_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.read().strip().split('\n')

    if len(lines) >= 5:
        # Process solution length, states visited, states processed
        solution_length = int(lines[0])
        states_visited = int(lines[1])
        states_processed = int(lines[2])

        # Handle max_depth which could be 'n/a'
        try:
            max_depth = int(lines[3])
        except ValueError:
            max_depth = 0  # Keep as string "n/a"

        time_ms = float(lines[4])

        return {
            'solution_length': solution_length,
            'states_visited': states_visited,
            'states_processed': states_processed,
            'max_depth': max_depth,
            'time_ms': time_ms
        }
    return None


def create_plots(plot_directory, df, group_by='algorithm', filter_value=None, filename_prefix=''):
    """
    Consolidated plotting function that handles all types of grouping

    Parameters:
    - plot_directory: Directory to save plots
    - df: DataFrame containing the data
    - group_by: Column to group by (default: 'algorithm')
    - filter_value: Optional filter to apply on 'algorithm' column
    - filename_prefix: Prefix for the output filenames
    """
    # Filter data if needed
    if filter_value:
        filtered_df = df[df['algorithm'] == filter_value]
    else:
        filtered_df = df

    # Define metrics to plot
    metrics = [
        {"column": "solution_length", "label": "Długość rozwiązania"},
        {"column": "states_visited", "label": "Liczba stanów odwiedzonych"},
        {"column": "states_processed", "label": "Liczba Stanów przetworzonych"},
        {"column": "max_depth", "label": "Maksymalna osiągnięta głębokość"},
        {"column": "time_ms", "label": "Czas trwania (ms)"}
    ]

    # Legend mappings
    legend_labels = {
        'bfs': 'BFS',
        'dfs': 'DFS',
        'astr': 'A*',
        'manh': "Manhattan",
        'hamm': 'Hamming'
    }

    # Create plots for each metric
    for metric in metrics:
        column = metric["column"]
        ylabel = metric["label"]

        # Group the data
        grouped_data = filtered_df.groupby(['depth', group_by])[column].mean().reset_index()

        # Create and save the plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='depth', y=column, hue=group_by, data=grouped_data)

        # Apply log scale only in specific cases as in the original code
        if (column in ["states_visited", "states_processed", "time_ms"] and
                (filter_value is None or filter_value in ['bfs', 'dfs'])):
            plt.yscale('log')

        plt.xlabel("Głębokość")
        plt.ylabel(ylabel)

        # Update legend labels if available
        if group_by in ['algorithm', 'algorithm_options']:
            handles, labels = plt.gca().get_legend_handles_labels()
            new_labels = [legend_labels.get(label, label) for label in labels]
            plt.legend(handles=handles, labels=new_labels, title=None, loc='upper left')
        else:
            plt.legend(title=None, loc='upper left')

        output_filename = f"{plot_directory}/{column}_{filename_prefix}.png"
        plt.savefig(output_filename)
        plt.close()


if __name__ == "__main__":
    data_directory = "./output"
    plot_directory = "./plots"

    # Ensure plot directory exists
    os.makedirs(plot_directory, exist_ok=True)

    # Load and process data
    data_list = []
    for filename in os.listdir(data_directory):
        if filename.endswith('_stats.txt'):
            file_metadata = parse_filename(filename)

            if file_metadata:
                filepath = os.path.join(data_directory, filename)
                file_stats = read_stats_file(filepath)

                if file_stats:
                    data_entry = {**file_metadata, **file_stats}
                    data_list.append(data_entry)

    df = pd.DataFrame(data_list)
    if df.empty:
        print("No valid data files found.")
        exit(0)

    # Create all the plot groups using the consolidated function
    create_plots(plot_directory, df, group_by='algorithm', filename_prefix='general_grouping')
    create_plots(plot_directory, df, group_by='algorithm_options', filter_value='astr',
                 filename_prefix='astar_grouping')
    create_plots(plot_directory, df, group_by='algorithm_options', filter_value='bfs', filename_prefix='bfs_grouping')
    create_plots(plot_directory, df, group_by='algorithm_options', filter_value='dfs', filename_prefix='dfs_grouping')