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
    data['end'] = "false"
    
    #data['obstacle'] = []
    data['obstacle'].append({
        "group_color": "(255,0,250)",
        "group_pos": []
    })
    tiles_draw_row = 2
    tiles_draw_col = 6
    col_dist = 4
    row_dist = 3 
    
    check_row = 0
    check_col = 0
    
    check_row_other = 0
    check_col_other = 0

    for i in range(2, xdimension):

        if check_row < tiles_draw_row:
           for j in range(3, ydimension):
                if check_col < tiles_draw_col:
                    data['obstacle'][0]["group_pos"].append(
                        [i,j]
                    )
                else:
                    #do nothing
                    check_col_other += 1
                    if check_col_other == col_dist:
                        check_col = -1
                        check_col_other = 0
                check_col += 1  
        else:
            #do nothing
            check_row_other += 1
            if check_row_other == row_dist:
                check_row = -1
                check_row_other = 0

        check_row += 1
        check_col = 0
        check_col_other = 0


with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
