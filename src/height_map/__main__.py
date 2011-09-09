'''
Created on 5 Jun 2011

@author: SASHMAN
'''

import random, sys
from PIL import Image, ImageDraw
import math
size = 257
#size = 9
map = range(0,size)

hill = {'x':int(size/2),'y':int(size/2)}
hill_size = 0 


#return an average of the surrounding square + random offset
def get_sqr_avg(map, x, y, l, random_offset):
    return (map[x-l][y-l] + map[x+l][y-l] + map[x-l][y+l] + map[x+l][y+l]) /4 + get_val(random_offset,x,y)

#return an average of the surrounding diamond + random offset
def get_dia_avg(map, x, y, l, random_offset):
#    .   a   .
#    b   .   c
#    .   d   .
    sum = 0
    n = 0
    if x-l >= 0: #a
        sum += map[x-l][y]
        n+=1
    if y-l >= 0: #b
        sum += map[x][y-l]
        n+=1
    if y+l <= len(map)-1: #c
        sum += map[x][y+l]
        n+=1
    if x+l <= len(map)-1: #d
        sum += map[x+l][y]
        n+=1
    
    r = sum/n + get_val(random_offset,x,y)
    return r

def run():
    for m in range(0,size):
        map[m] = range(0,size)
        for j in range(0,size):
            map[m][j] = 0 
            
    if len(sys.argv)>1:
    	random.seed(sys.argv[1])

    seed = 5
    random_offset = 5
    l = 0     
    h = len(map)-1 #sub size
    m = int(h/2) #stride
    stride = m
    
    #square
    map[l][l] += seed#get_val(random_offset)
    map[h][l] += seed#get_val(random_offset)
    map[l][h] += seed#get_val(random_offset)
    map[h][h] += seed#get_val(random_offset)
    
    #diamond
#    map[l][m] += get_val(random_offset)
#    map[m][l] += get_val(random_offset)
#    map[m][h] += get_val(random_offset)
#    map[h][m] += get_val(random_offset)
    
    while h > 1:
        
        #print h
        m = int(h/2) #stride
        i = m
        
        #print "square h=" + str(h) + " m=" + str(m)
        while i < len(map)-1:
            j = m
            while j < len(map)-1:
            
                #print "\ti=" + str(i) + " j=" + str(j)
                map[i][j]=get_sqr_avg(map, i, j, m, random_offset)
                ##print ".",
                j+=(m*2) 
            
            i+=(m*2)
            
        #print_map(map)
            
        
        odd = False
        
        i = 0
        #print "diamond h=" + str(h) + " m=" + str(m)
        while i <= len(map)-1:
            if not odd:
                j = m
            else:
                j = 0
                
            while j <= len(map)-1:
            
                #print "\ti=" + str(i) + " j=" + str(j)
                map[i][j]=get_dia_avg(map, i, j, m, random_offset)
                ##print ".",
                j+=(m*2)
            
            i+=(m)
            
            if odd: odd = False
            else: odd = True
            
        #print_map(map)
        
        #random_offset = math.pow(random_offset, .9) 
        random_offset *= .8
        #random_offset -= 1
        
        h /= 2
    
    #print_map(map)

    img = Image.new("RGB", (size,size), (256,256,256))
    xsize,ysize = size,size
    draw = ImageDraw.Draw(img)
    for x, i in enumerate(map):
        for y, j in enumerate(i): 
            
            j *= 20
            draw.point((x,y), fill = (j,j,j))
    del draw
    img.save("out.png")
    img.show()
   
def print_map(map):
    print "-------------------"
    for i in map:
        print i,
        print
    print "-------------------"

def get_val(random_offset,x,y):
	hill_offset = 0
	x_dist = abs(x-hill['x'])
	y_dist = abs(y-hill['y'])
	h_dist = math.sqrt(math.pow(x_dist,2) + math.pow(y_dist,2))
	if(h_dist < 1):
		h_dist = 1
	hill_offset = int(hill_size*(1/math.pow(abs(h_dist),1)))
	return int(random.randint(int(-random_offset+hill_offset), int(random_offset+hill_offset)))
    #return int(random_offset)


if __name__ == '__main__':
    run()
