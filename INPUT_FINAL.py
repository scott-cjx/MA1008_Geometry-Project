#Remaking Input because it failed miserably
import turtle as T
import random
import time 

Sc = T.Screen()
points = []
all_polygons = []

def random_color():
    #turtle accepts rgb values from 0.0 to 1.0
    return (random.random(), random.random(), random.random())

def screen_setup():
    T.hideturtle()
    T.setup(width=0.75, height=0.6)  # Window Size
    T.screensize(1000, 800)          # Canvas Size

    #Screen setup
    T.penup()
    T.goto(0, 500)  # near top
    T.color("black")
    T.write("Left-click: add point | Right-click: finish polygon | Scroll Wheel Click: Clear", 
            align="center", font=("Arial", 12, "normal"))
    
    #Draw box over canvas size
    T.pu()
    T.goto(-500, -400)
    T.pd()
    T.goto(500, -400)
    T.goto(500, 400)
    T.goto(-500, 400)
    T.goto(-500, -400)
    T.pu()


def input_mode_selector():
    print("================= Polygon Input Mode ================")
    print("1. Mouse-click (left-click points, right-click finish polygon)")
    print("2. Manual input (type point coordinates) (x, y): ")
    mode = input("Select input mode (1 or 2): ")
    if mode == "1":
        print("Selected mode 1: Mouse-click input")
    elif mode == "2":
        print("Selected mode 2: Manual input")
    return mode
#keyboard input

def input_event_manual():
    global points, polygons
    
    while True:
        try:
            print("================== Manual Point Input Mode ================")
            print("Enter Coordinates as x,y (type 'done' to finish current polygon, 'quit' to exit): ")
            print("Canvas Size is 1000 x 800 (x: -500 to 500, y: -400 to 400), Any values Beyond will be Clamped")
            
            x = float(input("Enter x coordinate (or 'done'/'quit'): "))
            y = float(input("Enter y coordinate (or 'done'/'quit'): "))
            
            # Clamp values to canvas size
            x = max(-500, min(500, x))
            y = max(-400, min(400, y))
            
            points.append((x, y))
            T.goto(x, y)
            T.pd()
            T.dot(5)
            print(f"Point added: ({x}, {y})")

        except ValueError as e:
            if "could not convert" in str(e).lower() or x == 'done' or y == 'done':
                print("Invalid input. Please enter coordinates as x,y or type 'done' or 'quit'.")
                finish_polygon_mouse(points[-1][0], points[-1][1])
                
                cont = input("Add another polygon (y/n)? ")
                if cont.lower() != 'y':
                    break
        


#-----------------------------------------------------------------------------------------------
def warning_message(points):
    global Sc
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

#Final Drawing Polygon Function
#Remember all mouseclicks return x, y values denoted as i, j
def get_points(i, j):
    global points
    canvas_width = 500
    canvas_height = 400
    
    i = max(-canvas_width, min(canvas_width, i))
    j = max(-canvas_height, min(canvas_height, j))
    print("Point Clicked, Coordinates: ", (i, j))
    T.goto(i, j)
    points.append((i, j))
    print("Current Points List: ", points)
    T.pd()  # T.pd() same as T.pendown()
    T.dot(5)
    #clamp canvas, in case user clicks outside

def warning_message(points):
    global Sc
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

#Although function doesn't take in coordinates, it still needs to accept i, j from mouseclick
def finish_polygon_mouse(i, j):
    global points
    global all_polygons
    #add in user validation
    if len(points) < 3:
        warning_message(points)
    else:
        T.pu()
        T.color(random_color())
        T.goto(points[0]) #each points is a (x, y) tuple. Goto takes in (x, y) input
        for point in points:
            T.pd()
            T.goto(point)
        T.goto(points[0])
        all_polygons.append(points)
        points = []  #reset points for next polygon
        T.pu()

def clear_screen(i, j):
    global points
    global all_polygons
    T.clear()
    screen_setup()
    points = []
        
def delete_last_points(i, j):
    global points
    if points:
        points.pop()
        T.undo()  # Remove the last dot drawn
        T.undo()  # Remove the last goto action
        print("Last point deleted. Current Points List: ", points)

def done_input():
    global all_polygons
    global points
    if len(points) >= 3:
        print("Points remaining: ", points)
        
        isfinish = input("Press Y to  finalize the current polygon: ")
        while not isfinish:
            isfinish = input("Press Y to finalize the current polygon: ")
        
        if isfinish.lower() == 'y':
            finish_polygon_mouse(0, 0)  # Complete the current polygon if valid
        else:
            print("Current polygon not finalized.")
            
    if len(points) < 3 and len(points) > 0:
        print("Incomplete polygon with less than 3 points will be discarded.")
        isclear = input("Press Y to discard the incomplete polygon:")
        while not isclear:
            isclear = input("Press Y to discard the incomplete polygon: ")
        
        if isclear.lower() == 'y':
            points = []  # Complete the current polygon if valid
            print("Incomplete polygon discarded., points: ", points)
            print("`Final Polygons: ", all_polygons)
        else:
            print("Current polygon not finalized. please continue")
        
    if len(all_polygons) > 0 and len(all_polygons) < 2:
        print("================= WARNING =================")
        isclear = input("You only have 1 polygon drawn. Are you sure you want to finish?")
        
        while not isclear:
            isclear = input("Press Y to finalize the current polygon: ")
        
        if isclear.lower() == 'y':
            print("Final Polygons: ", all_polygons)
            clear_screen(0, 0)  # Clear screen
            
        else:
            pass

def mouse_input():
    Sc.onclick(get_points, 1)  # Left mouse button press
    Sc.onclick(finish_polygon_mouse, 3)  # Right mouse button press
    Sc.onclick(delete_last_points, 2)  # Middle mouse button press
    Sc.onkey(done_input, "q")  # Press 'q' to quit input mode
    Sc.onkey(done_input, "Q")  # Press 'Q' to quit input mode
    # setup_debug_keys()
    Sc.listen()
    
    
screen_setup() 
mouse_input()
T.done()
    