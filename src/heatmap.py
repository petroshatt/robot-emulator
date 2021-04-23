import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np
import random
import json

def pars_json(file):
    
  f = open(file)
  
  data = json.load(f)

  f.close()

  return data

json_data = pars_json("../data/json.json")

#Set the dimensions of the grid
y_dimension = json_data["ydimension"]
x_dimension = json_data["xdimension"]

grid = np.zeros((y_dimension,x_dimension))


num_of_rob = len(json_data["robots_movements"])

for k in range(num_of_rob):

  num_of_moves = len(json_data["robots_movements"][k]["move"])

  for j in range(num_of_moves):

    y = json_data["robots_movements"][k]["move"][j][0]
    x = json_data["robots_movements"][k]["move"][j][1]
    grid[y-1][x-1] += 1


dataset = pd.DataFrame(grid)


fig, ax = plt.subplots(figsize=(11, 9))
# plot heatmap
sb.heatmap(dataset, cmap="Blues", vmin= 0, vmax=np.amax(grid),
           linewidth=0.3, cbar_kws={"shrink": .8}, square=True)
plt.savefig("out_heatmap.png")
plt.show()

