#This is a test code to learn how to use turtle to draw a polygon
#still learning


import turtle as T

#Now that I've defined polygon, I guess make function? to make it easy to access

def draw_poly(points, colour ="black"):
    T.color(colour)
    T.penup() #so that the robot doesnt draw, when going to starting pos.
    T.goto(points[0]) #initialize starting pos
    T.pendown() #movement from starting pos will be drawn
    for p in points[1:]:
        T.goto(p) #goto expects x,y coordinates
    T.goto(points[0]) #to get close shape, draw and return to original positino



#A polygon is defined by lines connected by vertices which are defined as x-y coordinates?
# I think, idea is to store coordinates in 2D list
polygon = [[0, 110], [100, 100], [120,85], [-40, -40]] 
polygon2 = [[0, 0], [100, 200], [200, 300], [300, 400]]
draw_poly(polygon)
draw_poly(polygon2)

screen = T.Screen()
screen.exitonclick()

