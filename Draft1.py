# Program demosntrating using the mouse to input and display a polygon

import turtle as T
import time
import random

T.hideturtle()
Sc = T.Screen()

def random_color():
   return (random.random(), random.random(), random.random())

def get_point(i, j):  # Return polygon vertex as left mouse button pressed
   T.goto(i, j)
   points.append((i, j))
   T.pd()  # T.pd() same as T.pendown()
   T.dot(5)

def polygon(i, j):  # End polygon input, display and store it.
   global points
   T.pu()  # T.pu() same as T.penup()
   T.color(random_color())
   # T.begin_fill()
   if len(points) < 3:
      #if there are less than 3 points, display an error message below the last point
      last_point = points[-1]
      msg_x = last_point[0]
      msg_y = last_point[1]

      #screen dimensions
      screen_w = Sc.window_width() / 2
      screen_h = Sc.window_height() /2 

      #adjust if too close
      margin = 50 #pixels from edge
      alignment = "left"
      if msg_y < -screen_h + margin: 
         msg_y = -screen_h + margin
         alignment = "left"
      if msg_y > screen_h - margin:   
         msg_y = screen_h - margin
         alignment = "right"
      if msg_x < -screen_w + margin:  
         msg_x = -screen_w + margin
         alignment = "left"
      if msg_x > screen_w - margin:   
         msg_x = screen_w - margin
         alignment = "right"

      #message should only popup for a bit
      T.goto(msg_x, msg_y)
      T.color("black")
      T.write("need at least 3 points, next point continue", align=alignment, font=("Arial", 12, "normal"))
      time.sleep(1.5)
      T.undo()
      return
   else: 
      for p in points:
         T.goto(p)
         T.pd()
   T.goto(points[0])
   # T.end_fill()
   polys.append(points) # store the polygon
   points = []          # Re-initialise points for new polygon
   T.pu()

def Quit():
   key = input("Press Q again to quit graphics. Any other key to continue. ")
   if key == "Q":
      T.bye()
      print("\nExiting graphics.")

def main():
   
   Sc.onclick(get_point, 1)  # Left mouse button press
   Sc.onclick(polygon, 3)    # Right mouse button press
   Sc.onkey(Quit, "Q")       # Q key press  
   Sc.listen()               # Listen for event 
   Sc.mainloop()             # Stay in graphical interation

   print("\nHere are the polygons: ")
   for P in polys:   # List the polygons entered
      print("\n", P)

# Do some initialisation
points = []
polys = []
T.color(random_color())
T.pu()
T.penup()
T.goto(0, 290)  # near top
T.color("black")
T.write("Left-click: add point | Right-click: finish polygon | Q: quit", 
        align="center", font=("Arial", 12, "normal"))
#for debugging
T.goto(0, 0)
T.color("black")
T.write(".", align="center", font=("Arial", 12, "normal"))


main()  # The main program
