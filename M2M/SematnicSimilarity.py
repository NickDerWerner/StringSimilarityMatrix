import difflib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle 
import nltk
import GTEM2M





matrix = GTEM2M.matrix



# Define the row and column labels
row_labels = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11']
col_labels = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11']

data = np.array(matrix)

# Get the dimensions of the matrix
num_rows, num_cols = data.shape

# Create a figure and axes
fig, ax = plt.subplots(figsize=(6, 6)) # Adjust figure size as needed

# Hide the default axes (the box around the plot)
ax.axis('off')

# Draw the grid lines explicitly
# Vertical lines: from x=0 to x=num_cols
for j in range(num_cols + 1):
    ax.vlines(j, 0, num_rows, color='gray', linewidth=1)

# Horizontal lines: from y=0 to y=num_rows
for i in range(num_rows + 1):
    ax.hlines(i, 0, num_cols, color='gray', linewidth=1)

#Color cells lower than threashold
threshold = 0  # Define the threshold for coloring cells:
for i in range(num_rows):
    for j in range(num_cols):
        if data[i, j] <= threshold:
            # Erstelle ein Rechteck für die Zelle (i, j)
            # Du kannst Farbe und Transparenz hier anpassen
            rechteck = Rectangle((j, i), 1, 1, color='red', alpha=0.5) # Beispiel: hellblau, semi-transparent
            # Füge das Rechteck zu den Achsen hinzu
            ax.add_patch(rechteck)

precisionCounter = 0
greenPointsSValues = [] 
for j in range(num_cols):
    # Finde den maximalen Wert in der aktuellen Spalte j
    max_value = np.max(data[:, j])

    if max_value > threshold:
        precisionCounter+=1
        row_indices_of_max = np.where(data[:, j] == max_value)[0]
        for i in row_indices_of_max:
            greenPointsSValues.append(i)
            rectangle = Rectangle((j, i), 1, 1, color='green', alpha=0.5) 
            ax.add_patch(rectangle)

# Place the text (numbers) inside each cell
# The center of cell (i, j) in this coordinate system is at (j + 0.5, i + 0.5)
for i in range(num_rows):
    for j in range(num_cols):
        #text = data[i, j]
        text = f"{data[i, j]:.2f}"
        # Add text to the plot
        ax.text(j + 0.5, i + 0.5, text,
                ha='center', va='center', # Center align the text
                fontsize=11) # Adjust font size as needed

# Place the row and column labels
# Column labels above the top row
for j, label in enumerate(col_labels):
    # Position the label centered above the column, slightly above the top line (y=0)
    ax.text(j + 0.5, -0.25, label,
            ha='center', va='bottom', # Center horizontally, align to bottom vertically
            fontsize=14)

# Row labels to the left of the first column
for i, label in enumerate(row_labels):
    # Position the label centered next to the row, slightly left of the left line (x=0)
    ax.text(-0.25, i + 0.5, label,
            ha='right', va='center', # Align to right horizontally, center vertically
            fontsize=14)

# Adjust plot limits to make space for the labels
ax.set_xlim(-1, num_cols + 0.5)
ax.set_ylim(-1, num_rows + 0.5) # Initial limit, will be adjusted by invert_yaxis

# Invert the y-axis so the first row (index 0) appears at the top
ax.invert_yaxis()

# Set aspect ratio to make cells square
ax.set_aspect('equal', adjustable='box')

# Use tight_layout to automatically adjust plot parameters for a tight layout
plt.tight_layout()


#Calculate recall
recallCounter = 0
for i in range(num_rows):
    if i in greenPointsSValues:
        recallCounter += 1
recall = recallCounter / num_rows 
  

info_string1 = "Precision:"
info_number1 = precisionCounter / num_cols # Berechne die Präzision als Verhältnis der Spalten mit einem Wert über dem Schwellenwert
info_string2 = "    Recall:"
info_number2 = recall # Recall ist bereits berechnet
info_string3 = "    Threshold:"
info_number3 = threshold # Der Schwellenwert, der für die Färbung verwendet wurde
text_to_display = f"{info_string1} {info_number1:.5f} {info_string2} {info_number2:.5f} {info_string3} {info_number3}" # Formatiere die Zahl auf 3 Dezimalstellen

# Platziere den Text unterhalb der Achsen
# fig.text(x, y, text, **kwargs)
# x und y sind Koordinaten relativ zur Figur (0,0 ist links unten, 1,1 ist rechts oben)
# Wir wählen einen kleinen y-Wert (z.B. 0.05), um den Text unten zu platzieren
# Wir wählen einen x-Wert (z.B. 0.1), um den Text links zu platzieren, oder 0.5 für die Mitte
fig.text(0.15, 0.01, text_to_display, ha='left', va='bottom', fontsize=10,fontdict={'weight': 'bold'})


# Display the plot
plt.show()




