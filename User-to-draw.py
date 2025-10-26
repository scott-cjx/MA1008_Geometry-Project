import turtle as T

def draw_poly(points, colour ="black"):
    T.color(colour)
    T.penup() #so that the robot doesnt draw, when going to starting pos.
    T.goto(points[0]) #initialize starting pos
    T.pendown() #movement from starting pos will be drawn
    for p in points[1:]:
        T.goto(p) #goto expects x,y coordinates
    T.goto(points[0]) #to get close shape, draw and return to original position

#get user input
#future plan is to get so that the user can draw on interface, so that there is a "drawing stage" either through points, or either through mouse-drag

#define list first, while cannot store more than one polygon, this is sufficient for prototyping first
cont = ""
polygon = []
while cont != "N": #no input validation yet
    x = int(input("enter x:"))
    y = int(input("enter y:"))
    cont = input("enter Y or N: ")
    points = list([x, y])
    polygon.append(points)
print(polygon) # for debugging 
draw_poly(polygon) #it works

screen = T.Screen()
screen.exitonclick()

