import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os

def pointWithinGrid(x, y):
    if (not (0 <= x <= 5)) or (not (0 <= y <= 5)) :
        return False
    else:
        return True

# Graphing Helper Function

fixed_colormap = {
    0: "white",
    1: "red",
    2: "yellow",
    3: "blue",
    4: "purple"
}

# Function to generate dynamic colors for undefined values
def get_dynamic_colormap(start_index, num_colors):
    cmap = plt.cm.tab20  # Use a colormap with a large number of unique colors
    dynamic_colors = [mcolors.rgb2hex(cmap(i / cmap.N)) for i in range(start_index, start_index + num_colors)]
    return dynamic_colors

# Create a combined colormap for the grids
def create_combined_colormap(grid):
    unique_values = np.unique(grid)
    combined_colormap = {}

    # Assign fixed colors for predefined values
    for val in fixed_colormap:
        combined_colormap[val] = fixed_colormap[val]

    # Assign dynamic colors for the remaining values
    undefined_values = [val for val in unique_values if val not in combined_colormap]
    dynamic_colors = get_dynamic_colormap(0, len(undefined_values))

    for val, color in zip(undefined_values, dynamic_colors):
        combined_colormap[val] = color

    return combined_colormap

def visualizeSteps(grids, outputDir):
    os.makedirs(outputDir, exist_ok=True)
    # Visualize each step and save as an image
    for i, grid in enumerate(grids):
        # Create a combined colormap for the current grid
        colormap = create_combined_colormap(grid)

        # Map grid values to color indices
        color_grid = np.array([[mcolors.to_rgba(colormap[val]) for val in row] for row in grid])

        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(color_grid, extent=[0, 6, 0, 6])

        # Add grid lines
        ax.set_xticks(np.arange(0, 6, 1))
        ax.set_yticks(np.arange(0, 6, 1))
        ax.grid(color="black", linestyle="-", linewidth=1)

        # Remove axis labels
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Title for visualization
        title = "init" if i == 0 else f"step{i}"
        ax.set_title(title.capitalize())

        # Save the figure
        plt.savefig(os.path.join(outputDir, f"{title}.png"))
        plt.close(fig)