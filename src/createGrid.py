import pygame
import json
import datetime

def txtOutput():

  filename_txt = "stats--" + datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S") + ".txt"

  file1 = open(filename_txt,"w")

  ts = datetime.datetime.now().timestamp()
  ts_str = "Current Timestamp: " + str(ts) + "\n"
  file1.write(ts_str)

  readable = datetime.datetime.fromtimestamp(ts).isoformat()
  rd_str = "Current Date and Time: " + str(readable) + "\n"
  file1.write(rd_str)

  robots_count = len(json_data["robots"])
  robots_str = "Number of Robots: " + str(robots_count) + "\n"
  file1.write(robots_str)

  movements_count = 0

  for i in range(len(json_data["robots_movements"])):
    movements_count += len(json_data["robots_movements"][i]["move"])

  movements_str = "Number of Movements: " + str(movements_count) + "\n"
  file1.write(movements_str)

  print("Stats saved as: ", filename_txt)


def pars_json(file):
    
  f = open(file)
  
  data = json.load(f)

  f.close()

  return data


json_data = pars_json("../data/json.json")


DISPLAY = True


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the margin between each cell
MARGIN = 1
#This sets the default size of each cell on the grid
GRID_SIZE = json_data["grid_size"]

#Set the dimensions of the grid
y_dimension = json_data["ydimension"]+1
x_dimension = json_data["xdimension"]+1

if (x_dimension or y_dimension) > 2000:
  DISPLAY = False


win_x = GRID_SIZE * x_dimension + MARGIN*x_dimension
win_y = GRID_SIZE * y_dimension + MARGIN*y_dimension +GRID_SIZE*2

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = GRID_SIZE
HEIGHT = GRID_SIZE

if DISPLAY==True:

  # Create a 2 dimensional array. A two dimensional
  # array is simply a list of lists.
  grid = []
  for row in range(y_dimension):
      # Add an empty array that will hold each cell
      # in this row
      grid.append([])
      for column in range(x_dimension):
          grid[row].append((255, 255, 255))  # Append a cell

  #INIT AXIS
  for i in range(y_dimension):
    grid[i][0] = i

  for i in range(x_dimension):
    grid[0][i] = i


  #INIT OBSTACLES
  temp_row_obs = 0
  temp_col_obs = 0


  num_of_groups = len(json_data["obstacle"])


  for i in range(num_of_groups):

    num_of_obs = len(json_data["obstacle"][i]["group_pos"])
    color = json_data["obstacle"][i]["group_color"]
    color = color.split("(")
    color = color[1].split(")")
    #print(color[0])
    color1, color2, color3 = color[0].split(",")

    for j in range(num_of_obs):
      temp_row_obs = json_data["obstacle"][i]["group_pos"][j][0]
      temp_col_obs = json_data["obstacle"][i]["group_pos"][j][1]
      #print(type(temp_col_obs))
      grid[temp_row_obs][temp_col_obs] = (int(color1),int(color2),int(color3))


  #INIT ROBOTS
  temp_row_rob = 0
  temp_col_rob = 0

  num_of_robots = len(json_data["robots"])

  for i in range(num_of_robots):
    temp_row_rob = json_data["robots"][i]["robot_pos_x"]
    temp_col_rob = json_data["robots"][i]["robot_pos_y"]
    grid[temp_row_rob][temp_col_rob] = json_data["robots"][i]["robot_name"]



  # Initialize pygame
  pygame.init()

  # Set the HEIGHT and WIDTH of the screen
  WINDOW_SIZE = [int(win_x), int(win_y)]


  DISPLAY_SIZE = (1, 1)
  DEPTH = 32
  FLAGS = 0
  screen = pygame.display.set_mode(DISPLAY_SIZE, FLAGS, DEPTH)

  work_surface  = pygame.Surface((int(win_x), int(win_y)))

   
  # Set title of screen
  pygame.display.set_caption("Grid")
   
  # Loop until the user clicks the close button.
  done = True

  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()

  
  pygame.font.init() # you have to call this at the start, 
                     # if you want to use this module.
  myfont = pygame.font.SysFont('Arial', 7)

  textsurface = myfont.render('r1', False, RED)
  

  saved_counter = 1


# -------- Main Program Loop -----------
while DISPLAY:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            DISPLAY = False
 
    # Set the screen background
    work_surface.fill(BLACK)
 
    # Draw the grid
    for row in range(y_dimension):
        for column in range(x_dimension):

            #case tile is GRID AXIS
            if type(grid[row][column]) == int:
              color = (0, 0, 0)
            #case tile is ROBOT
            elif type(grid[row][column]) == str:
              color = (0, 0, 0)
            #case tile is OBSTACLE
            else:
              color = grid[row][column]

            pygame.draw.rect(work_surface,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                               WIDTH,
                               HEIGHT])

            #text in case tile is GRID AXIS
            if type(grid[row][column]) == int:
              textsurface = myfont.render(str(grid[row][column]), False, RED)
              axis_y = GRID_SIZE*row + MARGIN*row
              axis_x = GRID_SIZE*column + MARGIN*column +2
              work_surface.blit(textsurface,(axis_x,axis_y))

            #text in case tile is ROBOT
            if type(grid[row][column]) == str:
              textsurface = myfont.render(grid[row][column], False, RED)
              rob_y = GRID_SIZE*row + MARGIN*row
              rob_x = GRID_SIZE*column + MARGIN*column +2
              work_surface.blit(textsurface,(rob_x,rob_y))    

    # Draw the lines
    num_of_rob = len(json_data["robots_movements"])

    for k in range(num_of_rob):

      num_of_moves = len(json_data["robots_movements"][k-1]["move"])-1
      line_color = json_data["robots_movements"][k-1]["line_color"]
      line_color = line_color.split("(")
      line_color = line_color[1].split(")")
      color1, color2, color3 = line_color[0].split(",")
      line_color = (int(color1),int(color2),int(color3))

      for i in range(num_of_moves):
        temp_move_y1 = json_data["robots_movements"][k-1]["move"][i][0]
        temp_move_y2 = json_data["robots_movements"][k-1]["move"][i+1][0]
        temp_move_x1 = json_data["robots_movements"][k-1]["move"][i][1]
        temp_move_x2 = json_data["robots_movements"][k-1]["move"][i+1][1]

        move_y1 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_y1)) + MARGIN*temp_move_y1 + k*1
        move_y2 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_y2)) + MARGIN*temp_move_y2 + k*1
        move_x1 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_x1)) + MARGIN*temp_move_x1 + k*1
        move_x2 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_x2)) + MARGIN*temp_move_x2 + k*1

        pygame.draw.line(work_surface, line_color, (move_x1,move_y1), (move_x2,move_y2), 1)


    label_x = 0+35
    label_y = GRID_SIZE*y_dimension+MARGIN*y_dimension+2

    myfont = pygame.font.SysFont('Arial', 20)
    textsurface = myfont.render(str(json_data["label"]), False, RED)
    work_surface.blit(textsurface,(label_x,label_y))  


    filename_grid = "grid--" + datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S") + ".png"

    pygame.image.save(work_surface, filename_grid)

     
    if saved_counter==1:
      print("\nGrid saved as: " + filename_grid)
    saved_counter+=1

    DISPLAY = False

    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

txtOutput()

import heatmap