import pygame
import json
import datetime
import sys
from threading import Thread
#import server
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def pars_json(file):
    
  f = open(file)
  
  data = json.load(f)

  f.close()

  return data


def reloadJson():
  global json_data 
  json_data = pars_json("../data/json.json")

def reloadJson1():
  global json_data 
  json_data = pars_json("../data/json1.json")



#json_data = pars_json("../data/json.json")
json_data = pars_json("../data/json.json")


# Initialize pygame
pygame.init()
 
# Set title of screen
pygame.display.set_caption("Grid")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Arial', 20)

textsurface = myfont.render('r1', False, RED)

screen = pygame.display.set_mode((0,0), 0, 0)



# This sets the margin between each cell
MARGIN = 2
#This sets the default size of each cell on the grid
GRID_SIZE = json_data["grid_size"]

TILE_SCROLL = 3

#Set the dimensions of the grid
y_dimension = json_data["ydimension"]+1
x_dimension = json_data["xdimension"]+1

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = GRID_SIZE
HEIGHT = GRID_SIZE


map_width = GRID_SIZE*x_dimension + MARGIN*x_dimension
map_height = GRID_SIZE*y_dimension + MARGIN*y_dimension
main_map = pygame.Surface((map_width, map_height))
main_map = main_map.convert()
done = False


scroll_x = 0
scroll_y = 0

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


def gridOutput():
  filename_grid = "grid--" + datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S") + ".png"
  pygame.image.save(main_map, filename_grid)
  print("\nGrid saved as: " + filename_grid)


def initWindow():

  win_x = GRID_SIZE * x_dimension + MARGIN*x_dimension
  win_y = GRID_SIZE * y_dimension + MARGIN*y_dimension

  DISPLAY_SIZE = (int(win_x), int(win_y))
  DEPTH = 32
  FLAGS = 0
  #screen = pygame.display.set_mode(DISPLAY_SIZE, FLAGS, DEPTH)
  screen = pygame.display.set_mode((800,800))



def initGrid():
  global grid
  #fill grid
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

  # Set the screen background
  screen.fill(BLACK)

def init_objects():
  initObstacles()
  initRobots()

def initObstacles():

  #INIT OBSTACLES
  temp_row_obs = 0
  temp_col_obs = 0

  try: 
    num_of_groups = len(json_data["obstacle"])
  except:
    num_of_groups = 0

  for i in range(num_of_groups):

    num_of_obs = len(json_data["obstacle"][i]["group_pos"])
    color = json_data["obstacle"][i]["group_color"]
    color = color.split("(")
    color = color[1].split(")")
    color1, color2, color3 = color[0].split(",")

    for j in range(num_of_obs):
      temp_row_obs = json_data["obstacle"][i]["group_pos"][j][0]
      temp_col_obs = json_data["obstacle"][i]["group_pos"][j][1]
      grid[temp_row_obs][temp_col_obs] = (int(color1),int(color2),int(color3))


def initRobots():


  #INIT ROBOTS
  temp_row_rob = 0
  temp_col_rob = 0

  try:
    num_of_robots = len(json_data["robots"])
  except:
    num_of_robots = 0

  for i in range(num_of_robots):
    temp_row_rob = json_data["robots"][i]["robot_pos_x"]
    temp_col_rob = json_data["robots"][i]["robot_pos_y"]
    grid[temp_row_rob][temp_col_rob] = json_data["robots"][i]["robot_name"]


def eventLoop():
  global done
  global scroll_x
  global scroll_y
  for event in pygame.event.get():  # User did something
      if event.type == pygame.QUIT:  # If user clicked close
          done = True
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          #print("up")
          #scroll_y = scroll_y + (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL)
          scroll_y = min(scroll_y + (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL), 0)
        elif event.key == pygame.K_DOWN:
          #print("down")
          #scroll_y = scroll_y - (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL)
          scroll_y = max(scroll_y - (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL), -(TILE_SCROLL*800))
        elif event.key == pygame.K_LEFT:
          #print("left")
          #scroll_x = scroll_x + (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL)
          scroll_x = min(scroll_x + (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL), 0)
        elif event.key == pygame.K_RIGHT:
          #print("right")
          #scroll_x = scroll_x - (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL)
          scroll_x = max(scroll_x - (GRID_SIZE*TILE_SCROLL+MARGIN*TILE_SCROLL), -(TILE_SCROLL*800))

def draw():

  global num_of_rob
  global num_of_moves

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

      pygame.draw.rect(main_map,
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
        main_map.blit(textsurface,(axis_x,axis_y))

      #text in case tile is ROBOT
      if type(grid[row][column]) == str:
        textsurface = myfont.render(grid[row][column], False, RED)
        rob_y = GRID_SIZE*row + MARGIN*row
        rob_x = GRID_SIZE*column + MARGIN*column +2
        main_map.blit(textsurface,(rob_x,rob_y))  

  # Draw the lines
  try:
    num_of_rob = len(json_data["robots_movements"])
    no_moves = 0
  except:
    no_moves = 1

  for k in range(num_of_rob):

    if no_moves==0:
      num_of_moves = len(json_data["robots_movements"][k-1]["move"])-1
      line_color = json_data["robots_movements"][k-1]["line_color"]
      line_color = line_color.split("(")
      line_color = line_color[1].split(")")
      color1, color2, color3 = line_color[0].split(",")
      line_color = (int(color1),int(color2),int(color3))

    for i in range(num_of_moves):

      if no_moves==0:
        temp_move_y1 = json_data["robots_movements"][k-1]["move"][i][0]
        temp_move_y2 = json_data["robots_movements"][k-1]["move"][i+1][0]
        temp_move_x1 = json_data["robots_movements"][k-1]["move"][i][1]
        temp_move_x2 = json_data["robots_movements"][k-1]["move"][i+1][1]

        move_y1 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_y1)) + MARGIN*temp_move_y1 + k*1
        move_y2 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_y2)) + MARGIN*temp_move_y2 + k*1
        move_x1 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_x1)) + MARGIN*temp_move_x1 + k*1
        move_x2 = GRID_SIZE/2 + (GRID_SIZE*(temp_move_x2)) + MARGIN*temp_move_x2 + k*1

      pygame.draw.line(main_map, line_color, (move_x1,move_y1), (move_x2,move_y2), 3)   

  screen.blit(main_map, (scroll_x, scroll_y))
  pygame.display.flip()


def run():
  global clock
  #global json_data
  while not done:
    # Limit to 60 frames per second
    clock.tick()

    eventLoop()
    reloadJson()
    initObstacles()
    initRobots()

    draw()



'''
def runTCP():
  global PORT
  while True:
    temp = server.run_server(PORT)
'''

# -------- Main Program Loop -----------
if __name__ == "__main__":
  '''
  if len(sys.argv) > 1:
    global PORT
    PORT = sys.argv[1]
    t = Thread(target = runTCP).start() 
  '''
  reloadJson()

  initWindow()
  initGrid()
  run()

  gridOutput()
  txtOutput()

  pygame.quit()

  import heatmap

