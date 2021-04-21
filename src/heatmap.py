import json

def pars_json(file):
    
  f = open(file)
  
  data = json.load(f)

  f.close()

  return data

json_data = pars_json("/Users/petros/Desktop/robotEmulator/data/json.json")

#Set the dimensions of the grid
y_dimension = json_data["ydimension"]
x_dimension = json_data["xdimension"]

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(y_dimension):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(x_dimension):
        grid[row].append(0)  # Append a cell

'''
num_of_rob = len(json_data["robots_movements"])

for k in range(num_of_rob):

	num_of_moves = len(json_data["robots_movements"][k-1]["move"])

	for j in range(num_of_moves):
'''


