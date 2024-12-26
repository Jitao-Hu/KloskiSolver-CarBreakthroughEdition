import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

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