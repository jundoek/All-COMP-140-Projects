"""
Code to implement the game of Spot it!

http://www.blueorangegames.com/spotit/
"""

import comp140_module2 as spotit

def equivalent( point1, point2, mod):
    """
    Determines if the two given points are equivalent in the projective
    geometric space in the finite field with the given modulus.

    Each input point, point1 and point2, must be valid within the
    finite field with the given modulus.

    inputs:
        - point1: a tuple of 3 integers representing the first point
        - point2: a tuple of 3 integers representing the second point
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the points are equivalent
    """
    cp_points=(point1[1] * point2[2] - point1[2] * point2[1], \
               point1[2] * point2[0] - point1[0] * point2[2], \
               point1[0] * point2[1] - point1[1] * point2[0])
    
    return bool(cp_points[0] % mod ==0 and cp_points[1] % mod == 0 and cp_points[2] % mod == 0)
     

    

def incident(point, line, mod):
    """
    Determines if a point lies on a line in the projective
    geometric space in the finite field with the given modulus.

    The inputs point and line must be valid within the finite field
    with the given modulus.

    inputs:
        - point: a tuple of 3 integers representing a point
        - line: a tuple of 3 integers representing a line
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the point lies on the line
    """
    
    return bool((point[0] * line[0] + point[1] * line[1] + point[2] * line[2]) % mod == 0)
  

def generate_all_points(mod):
    """
    Generate all unique points in the projective geometric space in
    the finite field with the given modulus.

    inputs:
        - mod: an integer representing the modulus

    Returns: a list of unique points, each is a tuple of 3 elements
    """
    pt_unique=[]
    for number_0 in range (mod):
        for number_1 in range (mod):
            for number_2 in range (mod):
                if(number_0 != 0 or number_1 != 0 or number_2 != 0):
                    total_points = (number_0, number_1, number_2)
                    pt_unique.append(total_points)
                    
                    for coord_1 in range(0,len(pt_unique)-1):
                        for coord_2 in range(coord_1 + 1,len(pt_unique)):
                            if equivalent(pt_unique[coord_1], pt_unique[coord_2], mod) == True:
                                pt_unique.pop(coord_2)
    return pt_unique
    

    

def create_cards(points, lines, mod):
    """
    Create a list of unique cards.

    Each point and line within the inputs, points and lines, must be
    valid within the finite field with the given modulus.

    inputs:
        - points: a list of unique points, each represented as a tuple of 3 integers
        - lines: a list of unique lines, each represented as a tuple of 3 integers
        - mod: an integer representing the modulus

    returns: a list of lists of integers, where each nested list represents a card.
    """
    deck = []
        
    for cards in lines:
        new_lines=[]
        for images in points:
            if incident(images, cards, mod) == True:
                new_lines.append(points.index(images))

        deck.append(new_lines)


    return deck

def run():
    """
    Create the deck and play the game.
    """
    # Prime modulus
    # Set to 2 or 3 during development
    # Set to 7 for the actual game
    
    modulus = 7

    # Generate all unique points for the given modulus
    
    points = generate_all_points(modulus)

    # Lines are the same as points, so make a copy
    
    lines = points[:]

    # Generate a deck of cards given the points and lines
    
    deck = create_cards(points, lines, modulus)

    # Run GUI - uncomment the line below after you have implemented
    #           everything and you can play your game.  The GUI does
    #           not work if the modulus is larger than 7.

    spotit.start(deck)
    

run()