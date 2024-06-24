# pip install pandas opencv-python
# visit pyGuru on YouTube

import cv2
import pandas as pd

# --------------------------------------------------------------------------

# Path to the image and CSV file
img_path = 'pic2.jpg'
csv_path = 'colors.csv'

# Reading the CSV file into a DataFrame
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Reading the image and resizing it
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ''
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d < minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Creating a window and setting a mouse callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        # Drawing a filled rectangle to display the color name and RGB values
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

        # Creating text string to display color name and RGB values
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # Displaying text with white color
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # Break the loop when 'Esc' key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
