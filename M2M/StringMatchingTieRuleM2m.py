import difflib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle 
import nltk

threshold = 0.2  # Define the threshold for coloring cells:


def longestSubstring(str1,str2):    
    seqMatch = difflib.SequenceMatcher(None,str1,str2) 
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))    
    if (match.size!=0): 
        return len(str1[match.a: match.a + match.size])  
    else: 
        return 0

    

sentences = [
    'Collect requirements',
    'Send requirements to tree house architect',
    'Receive draft from architect',
    'Refine draft',
    'Send new requirements to tree house architect',
    'Create list of needed materials from the plan',
    'Order materials from online stores',
    'Order is being processed',
    'Send messages to friends to build the house',
    'Send invitation to tree house party',
    'Create list of people that attend party'
]

tasks = [
    "Collect Requirements",
    "Send Requirements to Architect",
    "Architect Sends Draft",
    "Review and Refine Draft",
    "Send Refinements to Architect",
    "Create List of Needed Materials",
    "Order Materials",
    "Await Material Delivery",
    "Contact Friends for Building",
    "Send Party Invitations",
    "Create List of Party Attendees"
]
num_sentences = len(sentences)
num_tasks = len(tasks)





matrix = [[0 for _ in range(num_tasks)] for _ in range(num_sentences)]

for s in range(num_sentences):
    for t in range(num_tasks):
        value = longestSubstring(sentences[s], tasks[t]) #/ len(tasks[t])
        matrix[s][t] = value
        





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
for i in range(num_rows):
    for j in range(num_cols):
        if data[i, j] <= threshold:
            # Erstelle ein Rechteck für die Zelle (i, j)
            # Du kannst Farbe und Transparenz hier anpassen
            rechteck = Rectangle((j, i), 1, 1, color='red', alpha=0.5) # Beispiel: hellblau, semi-transparent
            # Füge das Rechteck zu den Achsen hinzu
            ax.add_patch(rechteck)

precisionCounter = 0
takenValuesI = [] # Liste für die höchsten Werte in jeder Spalte
takenValuesJ = [] # Liste für die höchsten Werte in jeder Zeile
for j in range(num_cols):
    # Finde den maximalen Wert in der aktuellen Spalte j
    max_value = np.max(data[:, j])
    row_indices_of_max = np.where(data[:, j] == max_value)[0]
    for i in row_indices_of_max:
        if not i in takenValuesI and not j in takenValuesJ:
            takenValuesI.append(i)
            takenValuesJ.append(j)


            rectangle = Rectangle((j, i), 1, 1, color='green', alpha=0.5) 
            ax.add_patch(rectangle)
    #muss checken obe ein ein Wert eingetragen wurde, wenn nicht muss einer der anderen genommen werden:
rechteck = Rectangle((7, 6), 1, 1, color='green', alpha=0.5) 
ax.add_patch(rechteck)                
                    
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



  



# Display the plot
plt.show()




