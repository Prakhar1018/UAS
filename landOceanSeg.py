import cv2 
import numpy as np

def overlap(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    land_lower = np.array([45, 100, 80])   # lower green
    land_upper = np.array([75, 255, 255]) # upper green
    ocean_lower = np.array((89, 127, 83))  # lower blue
    ocean_upper = np.array((116, 219, 118)) # upper blue
    pink_lower = np.array([140, 60, 200])
    pink_upper = np.array([160, 100, 255])
    lower_blue = np.array([90, 50, 150]) 
    upper_blue = np.array([120, 255, 255]) 
    lower_grey = np.array([0, 0, 180])    
    upper_grey = np.array([180, 30, 255]) 
    lower_green = np.array([35, 50, 100])   # H, S, V
    upper_green = np.array([75, 255, 255])
    lower_red =np.array([0, 70, 200])  
    upper_red = np.array([10, 130, 255])     
    lower_yellow = np.array([22, 110, 180])   
    upper_yellow = np.array([38, 255, 255])   



    land_mask = cv2.inRange(hsv, land_lower, land_upper)
    ocean_mask = cv2.inRange(hsv, ocean_lower, ocean_upper)
    pink_mask = cv2.inRange(hsv, pink_lower, pink_upper)
    blue_mask = cv2.inRange(hsv,lower_blue,upper_blue)
    grey_mask = cv2.inRange(hsv, lower_grey, upper_grey)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    overlay = img.copy()
    overlay[land_mask > 0] = (0, 255, 255)   # yellow for land
    overlay[ocean_mask > 0] = (255, 0, 0)  # bright blue for ocean

    output = cv2.addWeighted(img, 0.5, overlay, 0.5, 0)
    output[pink_mask>0] = (255, 0, 255)        #setting all the pixels to same color
    output[grey_mask>0] = (128, 128, 128)
    output[blue_mask>0] = (255, 0 , 0)
    output[green_mask>0] = (0, 255 , 0)
    output[red_mask>0] = (0, 0 , 255)
    output[yellow_mask>0] = (0, 255, 255)
    # cv2.imwrite("land_mask.jpg",land_mask)
    # cv2.imwrite("ocean_mask.jpg",ocean_mask)
    # cv2.imwrite("pink_mask.jpg",pink_mask)
    # cv2.imwrite("grey_mask.jpg",grey_mask)
    cv2.imwrite("blue_mask.jpg",blue_mask)
    return output
