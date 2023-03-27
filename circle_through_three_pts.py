"""
Code to calculate the circle that passes through three given points.
"""

import math
import comp140_module1 as circles

def distance(point0x, point0y, point1x, point1y):
    """
    Computes the distance between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the distance between the two points
    """
    
    distance_two_points = ((point0x - point1x) ** 2 + (point0y - point1y) ** 2) ** (1 / 2)
  
    
    return distance_two_points


def midpoint(point0x, point0y, point1x, point1y):
    """
    Computes the midpoint between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the midpoint
    """
    mp_y = (point0y + point1y) / 2
    
    mp_x = (point0x + point1x) / 2
    
    return mp_x, mp_y 

def slope(point0x, point0y, point1x, point1y):
    """
    Computes the slope of the line that connects two given points.

    The x-values of the two points, point0x and poin1x, must be different.

    inputs:
        -point0x: a float representing the x-coordinate of the first point.
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point.
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the slope between the points
    """
    
    lineslope = (point0y - point1y) / (point0x - point1x)
    
    return lineslope

def perp(lineslope):
    """
    Computes the slope of a line perpendicular to a given slope.

    input:
        -lineslope: a float representing the slope of a line.
                    Must be non-zero

    returns: a float that is the perpendicular slope
    """
   
    
    return -1 / lineslope

def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Computes the intersection point of two lines.

    The two slopes, slope0 and slope1, must be different.

    inputs:
        -slope0: a float representing the slope of the first line.
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -slope1: a float representing the slope of the second line.
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the intersection
    point
    """
    intersect_x = (-slope0 * point0x + slope1 * point1x + point0y - point1y) / (slope1 - slope0)

    
    intersect_y = slope0 * (intersect_x - point0x) + point0y
    
    
    return intersect_x, intersect_y

def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Computes the center and radius of a circle that passes through
    three given points.

    The points must not be co-linear and no two points can have the
    same x or y values.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point
        -point2x: a float representing the x-coordinate of the third point
        -point2y: a float representing the y-coordinate of the third point

    returns: three floats that are the x- and y-coordinates of the center
    and the radius
    """
    
    mp_pq_x, mp_pq_y = midpoint(point0x, point0y, point1x, point1y)
    mp_qr_x, mp_qr_y = midpoint(point1x, point1y, point2x, point2y)
    
    slope_pq = slope(point0x, point0y, point1x, point1y)
    slope_qr = slope(point1x, point1y, point2x, point2y)
  
    slope_perp_pq = perp(slope_pq)
    slope_perp_qr = perp(slope_qr)
    
    center_x, center_y = intersect(slope_perp_pq, mp_pq_x, mp_pq_y, slope_perp_qr, mp_qr_x, mp_qr_y)
    
    radius = distance(point0x, point0y, center_x, center_y)

    
    
    
    return center_x, center_y, radius



# Run GUI - uncomment the line below after you have
#           implemented make_circle
#circles.start(make_circle)
