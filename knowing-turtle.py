#getting to know turtle using turtle documentation https://docs.python.org/3/library/turtle.html#turtle.pendown

import turtle as T

#drawing triangle?
T.forward(100) #move 100 pixels??
T.left(120) #turn 120 degrees?, so have inner angle of 60 
T.forward(100)
T.left(120)
T.forward(100)

#drawing square
T.forward(100)
T.left(90)
T.forward(100)
T.left(90)
T.forward(100)
T.left(90)
T.forward(100)

#drew a circle
for _ in range(360):
        T.forward(1)
        T.left(1)


screen = T.Screen()
screen.exitonclick()