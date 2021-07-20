import sys
import json 


if __name__ == "__main__":

    xdimension = 40
    ydimension = 40
    grid_size = 25
    label = "Start..."
    
    data = {}
    data['xdimension'] = xdimension
    data['ydimension'] = ydimension
    data['grid_size'] = grid_size
    data['label'] = label
    data['obstacle'] = []
    data['robots'] = []
    data['robots_movements'] = []
    data['exits'] = []
    data['end'] = "true"
    
    #data['obstacle'] = []
    data['obstacle'].append({
        "group_color": "(255,0,250)",
        "group_pos": []
    })
    tiles_draw = 3
    col_dist = 3  #h apostash met3i ton stilon
    row_dist = 3 

    tiles_counter = 0 
    col_counter = 0
    row_counter = 0

    
    draw_col = True
    draw_row = True
    draw = True

    for i in range(1, xdimension):
        if row_counter == row_dist:
            row_counter=0
            if draw_row:
                draw_row = False
            elif draw_row==False:
                draw_row= True
            
        if draw_row:    
            for j in range(1, ydimension):

                if tiles_counter == tiles_draw:
                    draw = False
                    col_counter = 0
                    tiles_counter = 0  #san flag gia na mhn 3anampei

                if col_counter == col_dist:
                    draw = True

                if draw:
                    tiles_counter+=1
                    data['obstacle'][0]["group_pos"].append(
                        [i,j]
                    )

                col_counter+=1

        row_counter+=1 
        col_counter = 0
        tiles_counter = 0
        draw = True

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
