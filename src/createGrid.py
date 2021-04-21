import pygame
import json
from AppKit import NSScreen

def pars_json(file):
    
  f = open(file)
  
  data = json.load(f)

  f.close()

  return data


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the margin between each cell
MARGIN = 2
#This sets the default size of each cell on the grid
GRID_SIZE = 40

json_data = pars_json("../data/json.json")

#Set the dimensions of the grid
y_dimension = json_data["ydimension"]
x_dimension = json_data["xdimension"]

#Find the larger dimension for the fit of the screen
if y_dimension > x_dimension:
  large_dimension = y_dimension
else:
  large_dimension = x_dimension

win_x = (GRID_SIZE * x_dimension) + (large_dimension if x_dimension>y_dimension else x_dimension)*MARGIN
win_y = (GRID_SIZE * y_dimension) + (large_dimension if y_dimension>x_dimension else y_dimension)*MARGIN

screen_limit = 800-(large_dimension * MARGIN)

if win_x > screen_limit or win_y > screen_limit:
  GRID_SIZE = int(screen_limit / large_dimension)
  win_x = (GRID_SIZE * x_dimension) + (large_dimension if x_dimension>y_dimension else x_dimension)*MARGIN
  win_y = (GRID_SIZE * y_dimension) + (large_dimension if y_dimension>x_dimension else y_dimension)*MARGIN


# This sets the WIDTH and HEIGHT of each grid location
WIDTH = GRID_SIZE
HEIGHT = GRID_SIZE

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(y_dimension):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(x_dimension):
        grid[row].append((255, 255, 255))  # Append a cell

#print(len(grid))

#INIT OBSTACLES
temp_row_obs = 0
temp_col_obs = 0


num_of_groups = len(json_data["obstacle"])


for i in range(num_of_groups):

  num_of_obs = len(json_data["obstacle"][i]["tile_size"])
  color = json_data["obstacle"][i]["tile_color"]
  color = color.split("(")
  color = color[1].split(")")
  #print(color[0])
  color1, color2, color3 = color[0].split(",")

  for j in range(num_of_obs):
    temp_row_obs = json_data["obstacle"][i]["tile_size"][j][0]
    temp_col_obs = json_data["obstacle"][i]["tile_size"][j][1]
    #print(type(temp_col_obs))
    grid[temp_row_obs-1][temp_col_obs-1] = (int(color1),int(color2),int(color3))


#INIT ROBOTS
temp_row_rob = 0
temp_col_rob = 0

num_of_robots = len(json_data["robots"])

for i in range(num_of_robots):
  temp_row_rob = json_data["robots"][i]["robot_pos_x"]
  temp_col_rob = json_data["robots"][i]["robot_pos_y"]
  grid[temp_row_rob-1][temp_col_rob-1] = json_data["robots"][i]["robot_name"]



# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [int(win_x), int(win_y)]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for row in range(y_dimension):
        for column in range(x_dimension):
            if type(grid[row][column]) == str:
              color = (0, 0, 0)
            else:
              color = grid[row][column]
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                               WIDTH,
                               HEIGHT])
            #pygame.draw.line(screen, RED, (600,300), (200,300), 3)

    # Draw the lines
    num_of_rob = len(json_data["robots_movements"])

    for k in range(num_of_rob):

      num_of_moves = len(json_data["robots_movements"][k-1]["move"])-1

      for i in range(num_of_moves):
        temp_move_y1 = json_data["robots_movements"][k-1]["move"][i][0]
        temp_move_y2 = json_data["robots_movements"][k-1]["move"][i+1][0]
        temp_move_x1 = json_data["robots_movements"][k-1]["move"][i][1]
        temp_move_x2 = json_data["robots_movements"][k-1]["move"][i+1][1]

        move_y1 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_y1-1)) + MARGIN*temp_move_y1
        move_y2 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_y2-1)) + MARGIN*temp_move_y2
        move_x1 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_x1-1)) + MARGIN*temp_move_x1
        move_x2 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_x2-1)) + MARGIN*temp_move_x2

        pygame.draw.line(screen, RED, (move_x1,move_y1), (move_x2,move_y2), 3)

    pygame.image.save(screen, "im.jpeg")

    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()