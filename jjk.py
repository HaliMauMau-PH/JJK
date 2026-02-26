import cv2
import mediapipe as mp
import numpy as np
import time
import math
import random

print("Booting up...")

# setup mediapipe
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

num_particles = 1000  
COOLDOWN = 1.5

positions = np.zeros((num_particles, 3), dtype=np.float32)
colors = np.zeros((num_particles, 3), dtype=np.float32) 
sizes = np.ones(num_particles, dtype=np.float32) * 2

targetPositions = np.zeros((num_particles, 3), dtype=np.float32)
targetColors = np.zeros((num_particles, 3), dtype=np.float32)
targetSizes = np.ones(num_particles, dtype=np.float32) * 2

current_state = 'neutral'
pending_state = 'neutral'
hold_time = 0
rot_angle = 0.0

# --- Functions for drawing techniques ---

def makeNeutral():
    global targetPositions, targetColors, targetSizes
    for i in range(num_particles):
        if i < num_particles * 0.1:
            r = 100 + np.random.rand() * 150
            t = np.random.rand() * math.pi * 2
            p = np.random.rand() * math.pi
            targetPositions[i] = [r * math.sin(p) * math.cos(t), r * math.sin(p) * math.sin(t), r * math.cos(p)]
            targetColors[i] = [50, 25, 25] # BGR format! NOT RGB
            targetSizes[i] = 1
        else:
            targetPositions[i] = [0, 0, 0]
            targetColors[i] = [0, 0, 0]
            targetSizes[i] = 0

def doRed():
    global targetPositions, targetColors, targetSizes
    for i in range(num_particles):
        if i < num_particles * 0.2:
            r = np.random.rand() * 40
            t = np.random.rand() * math.pi * 2
            p = math.acos(2 * np.random.rand() - 1)
            targetPositions[i] = [r * math.sin(p) * math.cos(t), r * math.sin(p) * math.sin(t), r * math.cos(p)]
            targetColors[i] = [50, 50, 255] # red
            targetSizes[i] = 5
        else:
        
            arms = 3
            t = i / num_particles
            angle = t * 15 + ((i % arms) * (math.pi * 2 / arms))
            radius = 20 + (t * 300)
            targetPositions[i] = [radius * math.cos(angle), radius * math.sin(angle), (np.random.rand() - 0.5) * 50 * t]
            targetColors[i] = [0, 0, 200]
            targetSizes[i] = 2

def doVoid():
    global targetPositions, targetColors, targetSizes
    for i in range(num_particles):
        if i < num_particles * 0.2:
            angle = np.random.rand() * math.pi * 2
            targetPositions[i] = [150 * math.cos(angle), 150 * math.sin(angle), (np.random.rand()-0.5) * 10]
            targetColors[i] = [255, 255, 255]
            targetSizes[i] = 3
        else:
            radius = 200 + np.random.rand() * 400
            theta = np.random.rand() * math.pi * 2
            phi = math.acos(2 * np.random.rand() - 1)
            targetPositions[i] = [radius * math.sin(phi) * math.cos(theta), radius * math.sin(phi) * math.sin(theta), radius * math.cos(phi)]
            targetColors[i] = [255, 200, 50] 
            targetSizes[i] = 1

def doPurple():
    for i in range(num_particles):
        if np.random.rand() > 0.8:
            targetPositions[i] = [(np.random.rand() - 0.5) * 600, (np.random.rand() - 0.5) * 600, (np.random.rand() - 0.5) * 600]
            targetColors[i] = [180, 100, 100]
            targetSizes[i] = 1
        else:
            r = 120
            theta = np.random.rand() * math.pi * 2
            phi = math.acos(2 * np.random.rand() - 1)
            targetPositions[i] = [r * math.sin(phi) * math.cos(theta), r * math.sin(phi) * math.sin(theta), r * math.cos(phi)]
            targetColors[i] = [255, 0, 200] # purple
            targetSizes[i] = 4

def doShrine():
    for i in range(num_particles):
        if i < num_particles * 0.4:
            targetPositions[i] = [(np.random.rand()-0.5)*500, -100, (np.random.rand()-0.5)*500]
            targetColors[i] = [0, 0, 100] 
            targetSizes[i] = 2
        else:
            t = np.random.rand() * math.pi * 2
            rad = np.random.rand() * 200
            # parabola math for the shrine arches
            curve = (rad/200)**2 * 50
            targetPositions[i] = [rad*math.cos(t), 100 - curve + (np.random.rand()*10), rad*math.sin(t)*0.6]
            targetColors[i] = [0, 0, 150]
            targetSizes[i] = 2

def doShadow():
    for i in range(num_particles):
        if i < num_particles * 0.15:
            # Mahoraga Wheel
            is_rim = np.random.rand() > 0.2
            cy = 150
            cz = -50
            R = 100
            if is_rim:
                theta = np.random.rand() * math.pi * 2
                targetPositions[i] = [R * math.cos(theta), cy + R * math.sin(theta), cz]
            else:
                spoke = np.random.randint(0, 8)
                angle = spoke * (math.pi / 4)
                r_dist = np.random.rand() * R
                targetPositions[i] = [r_dist * math.cos(angle), cy + r_dist * math.sin(angle), cz]
            targetColors[i] = [0, 215, 255] 
            targetSizes[i] = 3
        else:
            radius = 50 + np.random.rand() * 400
            angle = np.random.rand() * math.pi * 2
            is_spike = np.random.rand() > 0.92
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = -150 + (np.random.rand() * 30)
            
            if is_spike:
                y += np.random.rand() * 200
                targetColors[i] = [100, 200, 50] 
                targetSizes[i] = 2
            else:
                targetColors[i] = [30, 40, 0] 
                targetSizes[i] = 4
            targetPositions[i] = [x, y, z]

def doVolcano():
    for i in range(num_particles):
        if i < num_particles * 0.5:
            t = np.random.rand()
            y = -150 + t * 250
            r = 60 + (1 - t) * 200 + (np.random.rand() - 0.5) * 20
            angle = np.random.rand() * math.pi * 2
            is_hot = t > 0.7 and np.random.rand() > 0.5
            targetPositions[i] = [r * math.cos(angle), y, r * math.sin(angle)]
            if is_hot:
                targetColors[i] = [0, 100, 255]
                targetSizes[i] = 3
            else:
                targetColors[i] = [20, 20, 50]
                targetSizes[i] = 2
        else:
            targetPositions[i] = [(np.random.rand()-0.5)*300, 100 + np.random.rand()*300, (np.random.rand()-0.5)*300]
            targetColors[i] = [0, 140, 255] 
            targetSizes[i] = 2

# Helper function to see if a finger is up
def checkFingerUp(handLms, tipID, pipID):
    if handLms.landmark[tipID].y < handLms.landmark[pipID].y:
        return True
    else:
        return False

# Open Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera broken or blocked.")
    exit()

makeNeutral()

print("Running main loop...")
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    height, width, _ = img.shape
    cx = width // 2
    cy = height // 2

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    detected_tech = 'neutral'
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            
            # get thumb and index finger coords
            thumb_x = handLms.landmark[4].x
            thumb_y = handLms.landmark[4].y
            index_x = handLms.landmark[8].x
            index_y = handLms.landmark[8].y
            
            # standard distance formula
            pinchDist = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)
            
            # check all fingers
            isIndexUp = checkFingerUp(handLms, 8, 6)
            isMidUp = checkFingerUp(handLms, 12, 10)
            isRingUp = checkFingerUp(handLms, 16, 14)
            isPinkyUp = checkFingerUp(handLms, 20, 18)

            if pinchDist < 0.04: 
                detected_tech = 'purple'
            elif isIndexUp and isMidUp and isRingUp and isPinkyUp: 
                detected_tech = 'shrine'
            elif isIndexUp and isMidUp and not isRingUp and not isPinkyUp: 
                detected_tech = 'void'
            elif isIndexUp and not isMidUp and not isRingUp and isPinkyUp: 
                detected_tech = 'shadow'
            elif isIndexUp and not isMidUp and not isRingUp and not isPinkyUp: 
                detected_tech = 'red'
            elif not isIndexUp and not isMidUp and not isRingUp and not isPinkyUp: 
                detected_tech = 'volcano'

    if detected_tech != pending_state:
        pending_state = detected_tech
        hold_time = time.time()
        
    if detected_tech != 'neutral':
        if time.time() - hold_time > COOLDOWN:
            if current_state != detected_tech:
                current_state = detected_tech
                # print("Technique activated!") 
                
                if detected_tech == 'red': 
                    doRed()
                elif detected_tech == 'void': 
                    doVoid()
                elif detected_tech == 'purple': 
                    doPurple()
                elif detected_tech == 'shrine': 
                    doShrine()
                elif detected_tech == 'shadow': 
                    doShadow()
                elif detected_tech == 'volcano': 
                    doVolcano()
        else:
            cv2.putText(img, "CHARGING...", (width//2 - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        if current_state != 'neutral':
            current_state = 'neutral'
            makeNeutral()

    # --- Draw the particles ---
    overlay = np.zeros_like(img, dtype=np.uint8)
    
    # rotate depending on the state
    if current_state == 'red': 
        rot_angle -= 0.05
    elif current_state == 'purple': 
        rot_angle += 0.08
    elif current_state == 'shrine' or current_state == 'shadow' or current_state == 'volcano': 
        rot_angle = 0 
    else: 
        rot_angle += 0.02

    cos_val = math.cos(rot_angle)
    sin_val = math.sin(rot_angle)

    # lerp formula to make it smooth
    positions += (targetPositions - positions) * 0.1
    colors += (targetColors - colors) * 0.1
    sizes += (targetSizes - sizes) * 0.1

    for i in range(num_particles):
        if sizes[i] < 0.5: 
            continue # skip small ones to save lag
            
        px = positions[i][0]
        py = positions[i][1]
        pz = positions[i][2]
        
        # 3d rotation math
        rx = px * cos_val - pz * sin_val
        rz = px * sin_val + pz * cos_val
        ry = py

        # project to 2D screen
        screen_x = int(rx + cx)
        screen_y = int(-ry + cy) 

        # only draw if its on screen
        if screen_x > 0 and screen_x < width and screen_y > 0 and screen_y < height:
            my_color = (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))
            cv2.circle(overlay, (screen_x, screen_y), int(sizes[i]), my_color, -1)

    # blend images together
    img = cv2.addWeighted(img, 0.7, overlay, 1.0, 0)

    display_str = ""
    if current_state == 'neutral':
        display_str = 'CURSED ENERGY'
    elif current_state == 'red':
        display_str = 'REVERSAL: RED'
    elif current_state == 'void':
        display_str = 'INFINITE VOID'
    elif current_state == 'purple':
        display_str = 'HOLLOW PURPLE'
    elif current_state == 'shrine':
        display_str = 'MALEVOLENT SHRINE'
    elif current_state == 'shadow':
        display_str = 'CHIMERA SHADOW GARDEN'
    elif current_state == 'volcano':
        display_str = 'COFFIN OF IRON MOUNTAIN'

    cv2.putText(img, display_str, (30, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow('Final Project - SAT0RU', img)
    
    # 27 is the ESC key
    if cv2.waitKey(1) & 0xFF == 27: 
        break

print("Exiting program.")
cap.release()
cv2.destroyAllWindows()