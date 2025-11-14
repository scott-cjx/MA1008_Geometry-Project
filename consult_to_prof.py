#Testing Polygons: Two Triangles Puncturing Two of its three Edges.
# A = [(-149.0, 236.0), (-310.0, -75.0), (28.0, -58.0)]
# B = [(61.0, 206.0), (-215.0, -148.0), (255.0, 97.0)]

A = [(-416.0, 173.0), (-355.0, -130.0), (42.0, -139.0), (-6.0, 170.0)]

B = [(-147.0, 39.0), (-88.0, -329.0), (338.0, -261.0), (259.0, 92.0)]

#------------------------------------------------------------------------------
#Display the Polygons
import turtle as T

T.hideturtle()
Sc = T.Screen()

def display_polygon(poly):
    T.pu()                # pen up          
    T.goto(poly[0])     # go to first point
    T.pd()                # pen down
    for p in poly[1:]:
        T.goto(p)
    T.goto(poly[0])     # Close Poly
    T.update()          # Update   

display_polygon(A)
display_polygon(B)
T.done()


#------------------------------------------------------------------------------
#Function to turn each Edge of Polygon into ((x1, y1), (x2, y2))
def get_edges(poly):
    edges = []
    n = len(poly)
    for i in range(n):
        x = poly[i]
        y = poly[(i + 1) % n] # wrap around
        edges.append((x, y))
    return edges


#Debug Purposes, shld display three for each
edges_poly1 = get_edges(A)
edges_poly2 = get_edges(B)
print(edges_poly1)
print(edges_poly2)

#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
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
    
#------------------------------------------------------------------------------
    
    
def intersection_check(e1, e2, eps=1e-9):
    '''
    Each edge is ((x11, y11), (x12, y12))
    '''
    
    (x11, y11), (x12, y12) = e1  # Edge 1 endpoints: P11, P12
    (x21, y21), (x22, y22) = e2  # Edge 2 endpoints: P21, P22
    
     # Direction vectors V1 = P12 - P11, V2 = P22 - P21
    v1x, v1y = x12 - x11, y12 - y11
    v2x, v2y = x22 - x21, y22 - y21
    
    denominator = v1x * v2y - v1y * v2x
    
    #Parallel case
    if abs(denominator) < eps: 
        return None
    
    # Numerators from Appendix B (Eqns 5 and 6)
    # A1 = (x11, y11), A2 = (x21, y21)
    t1 = ((x21 * v2y - y21 * v2x) - (x11 * v2y - y11 * v2x)) / denominator
    t2 = ((x21 * v1y - y21 * v1x) - (x11 * v1y - y11 * v1x)) / denominator

    # Check if intersection lies within both segments (0 <= t <= 1)
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        ix = x11 + v1x * t1
        iy = y11 + v1y * t1
        return (ix, iy)  # intersection point
    else:
        return None
    
intersection_check(edges_poly1[0], edges_poly2[0])  

#------------------------------------------------------------------------------

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
            p = intersection_check(edges_poly1[i], edges_poly2[j])
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
 
segments_poly1, segments_poly2, intersections = pre_process_polygon(A, B)

print("=== Polygon A Segmented Edges ===")
print(segments_poly1)
print("\n=== Polygon B Segmented Edges ===")
print(segments_poly2)
print("\n=== Intersection Points ===")
print(intersections)

#------------------------------------------------------------------------------

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
                if intersection_check(line_edge, other_edge) is not None: 
                    count += 1
                    # print(f"Intersection Found in {other_edge}")

            
            io_check = count % 2 == 1
            # results.append(io_check)
            results_per_edge.append(io_check)
            count_per_edge.append(count)
        counts.append(count_per_edge)
        results.append(results_per_edge)
        
    return counts, results


#------------------------------------------------------------------------------

#Code to determine keep or nah 
segments_poly1, segments_poly2, intersections = pre_process_polygon(A, B)
counts, insideout_results1 = insideout_check(segments_poly1, B)
counts, insideout_results2 = insideout_check(segments_poly2, A)

'''
I guess now that I have generated the segments, intersections, and inside-out checks
I can use the table and start making the discarding/keep function
'''
print("Inside-Out Results for Polygon 1 (M):", insideout_results1) #False is outside
print("Inside-Out Results for Polygon 2 (N):", insideout_results2) #True is inside
print("Segments Polygon 1:", segments_poly1)
print("Segments Polygon 2:", segments_poly2)

#First, try to find where the True/False change occurs along the segments
for i in range(len(segments_poly1)):
        for j in range(len(segments_poly1[i])):
                io_check = insideout_results1[i][j]
                segment = segments_poly1[i][j]
                print(f"Segment: {segment}, Inside-Out: {io_check}")
                if io_check == True:
                        segments_poly1[i][j] = ((0,0), (0,0)) #Mark for Deletion
                else:
                        print("Keep this Segment")
                        
for i in range(len(segments_poly2)):
        for j in range(len(segments_poly2[i])):
                io_check = insideout_results2[i][j]
                segment = segments_poly2[i][j]
                print(f"Segment: {segment}, Inside-Out: {io_check}")
                if io_check == True:
                        segments_poly2[i][j] = ((0,0), (0,0))
                else:
                        print("Keep this Segment")
                        
print("Post-Processing Segments Polygon 1:", segments_poly1)
print("Post-Processing Segments Polygon 2:", segments_poly2)


#------------------------------------------------------------------------------
# BROKEN

def operation(segments_poly1, segments_poly2, insideout_results1, insideout_results2, operation):
        print("Segment poly1: ", segments_poly1)
        print("Segment poly2: ", segments_poly2)
        print(insideout_results1)
        print(insideout_results2)
        print(operation)
        final_segments_poly1 = []
        final_segments_poly2 = []

        for i in range(len(segments_poly1)):
                for j in range(len(segments_poly1[i])):
                        io_check1 = insideout_results1[i][j]
                        segment1 = segments_poly1[i][j]
                        print(f"Segment: {segment1}, Inside-Out: {io_check1}")
                        if operation == "u":
                                if io_check1 == False:
                                # segments_poly1[i][j] = ((0,0), (0,0)) #Mark for Deletion
                                        final_segments_poly1.append(segment)
                        elif operation == "-":
                                if io_check1 == False:
                                        final_segments_poly1.append(segment1)
                        elif operation == "n":
                                if io_check1 == True:
                                        final_segments_poly1.append(segment1)
                        
        for i in range(len(segments_poly2)):
                for j in range(len(segments_poly2[i])):
                        io_check2 = insideout_results2[i][j]
                        segment2 = segments_poly2[i][j]
                        print(f"Segment: {segment2}, Inside-Out: {io_check2}")
                        if operation == "u":
                                if io_check2 == False:
                                # segments_poly1[i][j] = ((0,0), (0,0)) #Mark for Deletion
                                        final_segments_poly2.append(segment2)
                        elif operation == "-":
                                if io_check2 == True:
                                        final_segments_poly2.append(segment2)
                        elif operation == "n":
                                if io_check2 == True:
                                        final_segments_poly2.append(segment2)
                                        
        return final_segments_poly1, final_segments_poly2
    
segments_poly1, segments_poly2, intersections = pre_process_polygon(A, B)
counts, insideout_results1 = insideout_check(segments_poly1, B)
counts, insideout_results2 = insideout_check(segments_poly2, A)
final_segments_poly1, final_segments_poly2 = operation(segments_poly1, segments_poly2, insideout_results1, insideout_results2, "u")
print(final_segments_poly1)
print(final_segments_poly2)