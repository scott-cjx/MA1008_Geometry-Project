#---------------------------------------------------------------------------------
import turtle as T
import time
import random

points = []
polygons = []

def get_point(i, j):  # Return polygon vertex as left mouse button pressed
   global points
   canvas_width = 500
   canvas_height = 400
   
   i = max(-canvas_width, min(canvas_width, i))
   j = max(-canvas_height, min(canvas_height, j))
   
   T.goto(i, j)
   points.append((i, j))
   T.pd()  # T.pd() same as T.pendown()
   T.dot(5)
   

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
                finish_polygon(points[-1][0], points[-1][1])
                
                cont = input("Add another polygon (y/n)? ")
                if cont.lower() != 'y':
                    break
        
                
                          

def finish_polygon(i, j):
   global polygons
   global points
   # End polygon input, display and store it.
   T.pu()  
   T.color(random_color())
   print("points currently: ", points)
   #Warning Message Feature for points less than 3 (user validation)
   if len(points) < 3:
      warning_message(points)
      return
   else: 
      for p in points: 
         T.goto(p)
         T.pd()
   T.goto(points[0])
   
   # T.end_fill()
   polygons.append(points) # store the polygon
   points = []          # Re-initialise points for new polygon
   T.pu()
      
def input_event():
   Sc.onclick(get_point, 1)  # Left mouse button press
   Sc.onclick(finish_polygon, 3)    # Right mouse button press
   Sc.onclick(Quit, 2)
   Sc.listen()               # Listen for event 

def input_mode_menu():
    print("================= Polygon Input Mode ================")
    print("1. Mouse-click (left-click points, right-click finish polygon)")
    print("2. Manual input (type point coordinates) (x, y): ")
    mode = int(input("Select input mode (1 or 2): "))

'''             
HELPER FUNCTIONS FOR POLYGON PROCESSING
'''
#---------------------------------------------------------------------------------

def Quit():
   key = input("Press Q again to quit graphics. Any other key to continue: ")
   if key == "Q":
      print("\nExiting graphics.")
      
def random_color():
   return (random.random(), random.random(), random.random())


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


def draw_dashed_line(x1, y1, x2, y2, dash_length=5, gap_length=5):
    #calc eucledian dist.
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    if distance == 0:
        return

    num_dashes = int(distance / (dash_length + gap_length))
    dx = (x2 - x1) / distance
    dy = (y2 - y1) / distance
    
    for i in range(num_dashes):
        start_x = x1 + (dash_length + gap_length) * i * dx
        start_y = y1 + (dash_length + gap_length) * i * dy
        end_x = start_x + dash_length * dx
        end_y = start_y + dash_length * dy
        
        T.pu()
        T.goto(start_x, start_y)
        T.pd()
        T.goto(end_x, end_y)

#---------------------------------------------------------------------------------
def get_edges(poly):
    edges = []
    n = len(poly)
    for i in range(n):
        x = poly[i]
        y = poly[(i + 1) % n] # wrap around
        edges.append((x, y))
    return edges
#---------------------------------------------------------------------------------

'''
Each edge of the polygon is ((xi1, yi1), (xi2, yi2))
i is the polygon number, where i = 1 refers to polygon number 1, i = 2 polygon number 2 etc. 
By having two distinct points, we can turn it into parametric equation, where
- V (direction vector) is from xi2-xi1 and yi2-yi1 from same polygon
- t1 = ((A2xV2y – A2yV2x) – (A1xV2y – A1yV2x)) / (V1xV2y – V1yV2x) 
- t2 = ((A2xV1y – A2yV1x) – (A1xV1y – A1yV1x)) / (V1xV2y – V1yV2x)
- Check values, if both t1 t2  >= 0 and <= 1 then intersection point.
- Hence this function is meant to take in each one pair of edges. Implemented using a nested loop so it can cycle through all possible edge combinations between two polygons 
'''
def edge_intersections(e1, e2, eps=1e-9):
    (x11, y11), (x12, y12) = e1  # e1(P11, P12)
    (x21, y21), (x22, y22) = e2  # e2(P21, P22)
    
    #Direction Vectors
    v1x, v1y = x12-x11, y12-y11
    v2x, v2y = x22-x21, y22-y21
    
    #Denominator & Error Handling
    denominator = (v1x*v2y - v1y*v2x)
    if abs(denominator) < eps:
        print("Denominator is Approximately Zero. Lines are Parallel/Colinear")
    
    #If not parallel then can calculate
    t1 = ((x21 * v2y - y21 * v2x) - (x11 * v2y - y11 * v2x)) / denominator
    t2 = ((x21 * v1y - y21 * v1x) - (x11 * v1y - y11 * v1x)) / denominator
    
    #Check if t values satisfy condition for intersection
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        ix = x11 + v1x * t1 #x11 is starting point, v1x is x-length * t, where t is a "percentage" of the line
        iy = y11 + v1y * t1
        return (ix, iy)  # intersection point
    else:
        return None

#---------------------------------------------------------------------------------

'''
Now that the Edge has been identified along with its intersection pointsn
Need to divide the edge into sections based on the intersection points
This function segments takes in the edge of ONE polygon and its subsequent intersection points
To make sure that its dividing by the correct points, it should divide by the closest points based on eucledian distance
'''

def to_segment(edge, intersect_points):
    #Each Singular Edge is Edge (P1, P2)
    (x1, y1), (x2, y2) = edge
    
    all_points = [(x1, y1)] + intersect_points + [(x2, y2)]
    
    def euclid_dist_from_ref(p, p_ref=(x1, y1)):
        (px, py) = p #point being tested
        (x, y) = p_ref #reference point
        return ((px - x)**2 + (py - y)**2)**0.5 
    
    all_points.sort(key=euclid_dist_from_ref)
    
    #A segment, just like edge is Segment((x1,y1), (x2, y2)), so Just need to append the sorted points
    segments = []
    for i in range(len(all_points) - 1):
        segments.append((all_points[i], all_points[i+1]))
    return segments
    
#---------------------------------------------------------------------------------
#Main Function
def pre_process_polygon(poly1, poly2):
    #get the edges of both polygons
    edges_poly1 = get_edges(poly1)
    edges_poly2 = get_edges(poly2)
    
    #Intersections per Polygon
    intersections_on_poly1 = [[] for _ in range(len(edges_poly1))]
    intersections_on_poly2 = [[] for _ in range(len(edges_poly2))]
    intersections = []
    
    for i in range(len(edges_poly1)):
        for j in range(len(edges_poly2)):
            p = edge_intersections(edges_poly1[i], edges_poly2[j])
            if p is not None:
                intersections_on_poly1[i].append(p) #i 
                intersections_on_poly2[j].append(p) #j correspond to the edge-index
                intersections.append(p)

    segments_poly1 = []
    for i in range(len(edges_poly1)):
        segments_poly1.append(to_segment(edges_poly1[i], intersections_on_poly1[i]))
    segments_poly2 = []
    for i in range(len(edges_poly2)):
        segments_poly2.append(to_segment(edges_poly2[i], intersections_on_poly2[i]))

    return segments_poly1, segments_poly2, intersections
#---------------------------------------------------------------------------------
'''
After defining segments from the intersection points
Take Midpoint of each segment and then use an infinitely long line
This function takes in JUST a segment
'''
def insideout_check(segments, other_poly):
    #Identify Reference point (midpoint)
    results = []
    counts = []
    for i in range(len(segments)):
        results_per_edge = []
        count_per_edge = []
        for j in range(len(segments[i])):
            #Because the way these points are structured, need two four loops. One to iterate between edges, another between segments
            segment = segments[i][j]        #i for edges, j for segments within a specific edge
            (x1, y1), (x2, y2) = segment
            # print("Segment:", segment)
            #Reference from Midpoint P = A + Vt
            
            #Given/Reference Point (mid_x, mid_y)
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            A = (mid_x, mid_y)
            v = (1, 0)  #horizontal
            
            #Find Random End Point P
            px = mid_x + 1 * 1e6
            py = mid_y + 0 * 1e6
            P = (px, py)
            
            #The infinite line as a "edge"
            line_edge = (A, P)
            # print(line_edge)
            
            #count
            count = 0
            other_edges = get_edges(other_poly)
            for other_edge in other_edges:
                (x1, y1), (x2, y2) = other_edge
                # print("Other Poly:", other_edge)
                if edge_intersections(line_edge, other_edge) is not None: 
                    count += 1
                    # print(f"Intersection Found in {other_edge}")

            
            io_check = count % 2 == 1
            # results.append(io_check)
            results_per_edge.append(io_check)
            count_per_edge.append(count)
        counts.append(count_per_edge)
        results.append(results_per_edge)
        
    return counts, results

#AFTER PRE-PROCESSING
#---------------------------------------------------------------------------------
def keep_or_discard(segments_poly1, segments_poly2, insideout_results1, insideout_results2, operation):
    for i in range(len(segments_poly1)):
        for j in range(len(segments_poly1[i])):
            io_check = insideout_results1[i][j]
            if operation == "u":
                if io_check: #If inside
                    segments_poly1[i][j] = ((0,0), (0,0))
            elif operation == "i":
                if not io_check: #If outside
                    segments_poly1[i][j] = ((0,0), (0,0))
            elif operation == "-":
                if io_check: 
                    segments_poly1[i][j] = ((0,0), (0,0))
                    
    for i in range(len(segments_poly2)):
        for j in range(len(segments_poly2[i])):
            io_check = insideout_results2[i][j]
            if operation == "u":
                if io_check: #If inside
                    segments_poly2[i][j] = ((0,0), (0,0))
            elif operation == "i":
                if not io_check: #If outside
                    segments_poly2[i][j] = ((0,0), (0,0))
            elif operation == "-":
                if not io_check: 
                    segments_poly2[i][j] = ((0,0), (0,0))
                    
    return segments_poly1, segments_poly2
#---------------------------------------------------------------------------------------------------------------------------------
def flatten(segments):
    """Flatten and order segments into a continuous path"""
    
    flattened = []
    for i in range(len(segments)):
        for j in range(len(segments[i])):
            if segments[i][j] != ((0, 0), (0, 0)):
                flattened.append(segments[i][j])
    print("Flattened Segments:", flattened)
    
    return flattened

def ordered_segments(flat_poly1, flat_poly2):
    if flat_poly1 != []:
        ordered = [flat_poly1[0]]
        remaining = flat_poly1[1:] + flat_poly2[:]
        print("ordered: ",ordered)
        print("remaining: ", remaining)
    else:
        ordered = [flat_poly2[0]]
        remaining = flat_poly2[1:] + flat_poly1[:]
        print("ordered initially: ",ordered)
        print("remaining: ", remaining)

    while remaining:
        last_end = ordered[-1][1]
        
        matching_seg = None       
        for seg in remaining:
            if seg[0] == last_end:
                matching_seg = seg
                break
            elif seg[1] == last_end:
                matching_seg = (seg[1], seg[0])  # reverse segment
                break
        if matching_seg:
            ordered.append(matching_seg)
            remaining.remove(seg) #remove is apparently object sensitive
        else:
            break
        print("remaining", remaining)
        
    if remaining:
        ordered.extend(remaining)
    print("ordered final: ",ordered)
    return ordered

#--------------------------------------------------------------------------------------------------------------------------------------------------
import turtle as T

def display_segments(polygon):
    # Displaying segments
    T.begin_fill()
    for segment in polygon:
        (x1, y1), (x2, y2) = segment
        T.pu()
        T.goto(x1, y1)
        T.pd()
        T.goto(x2, y2)
        position = T.pos()
        print(position)
    if polygon:
        start_point = polygon[0][0]  # First point of first segment
        T.goto(start_point[0], start_point[1])
        
    T.end_fill()
    T.update()

#--------------------------------------------------------------------------------------------------------------------------------------------------
def screen_setup():
    
    T.hideturtle()
    
    T.setup(width=0.75, height=0.6)
    T.screensize(1000, 800)

    # Draw canvas outline for debugging
    T.pencolor("red")
    T.pensize(2)
    T.pu()
    T.goto(-500, -400)  # Bottom-left corner
    T.pd()
    T.goto(500, -400)   # Bottom-right
    T.goto(500, 400)    # Top-right
    T.goto(-500, 400)   # Top-left
    T.goto(-500, -400)  # Back to start
    T.pu()

    #Screen setup
    T.color(random_color())
    T.pu()
    T.penup()
    T.goto(0, 290)  # near top
    T.color("black")
    T.write("Left-click: add point | Right-click: finish polygon | Q: quit", 
            align="center", font=("Arial", 12, "normal"))

screen_setup()
Sc = T.Screen()
input_event()  # The main program
print("Program is successfull uptil now, polygons:", polygons)

def main_program(polygons):
    for i in range(len(polygons)-1):
        poly1 = polygons[i]
        poly2 = polygons[i+1]
        
        segments_poly1, segments_poly2, intersections = pre_process_polygon(poly1, poly2)
        counts, insideout_results1 = insideout_check(segments_poly1, poly2)
        counts, insideout_results2 = insideout_check(segments_poly2, poly1)
        final_segments_poly1, final_segments_poly2 = keep_or_discard(segments_poly1, segments_poly2, insideout_results1, insideout_results2, "u")
        # final_segments_poly1, final_segments_poly2 = keep_or_discard(segments_poly2, segments_poly1, insideout_results1, insideout_results2, "-")
        print("final_segments_poly1:", final_segments_poly1)
        print("final_segments_poly2:", final_segments_poly2)

        flat1 = flatten(final_segments_poly1)
        flat2 = flatten(final_segments_poly2)
        unified_polygon = ordered_segments(flat1, flat2)
        print("Unified Polygon Segments:", unified_polygon)
        display_segments(unified_polygon)

main_program(polygons)

T.done()

