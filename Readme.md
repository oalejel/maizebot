# EECS 467 Maizebot project 

Modules / Classes 
<!-- * .py 
   - **Gets data from:** 
   - **Purpose:** 
   - **Functions** 
   - **Forwards results to:**
   - **Output:**  -->
* gui.py

* video_reader.py 
   - **Gets data from:** USB camera through OpenCV VideoCapture object
   - **Purpose:** uses video stream API to read webcam data and sends signals to ___ to process the next frame  
   - **Functions** probably just a single function here
   - **Forwards results to:** homography.py
   - **Output:** the single most recent camera frame as a numpy array
* homography.py
    - **Gets data from** video_reader.py as a numpy array
    - **Purpose:** performs CV homography transformations on camera frames to adjust for angles 
                  - We will have four markers on the corners of the maze, which can be used for reference
                  - the first frame captured will be assumed to be flat, and will be discretized into the map, with marker locations stored
                  - future frames will have their marker locations detected, and markers associated with those from the reference frame
                  - we now have 4 pairs of points, enough to calculate the homography
                  - the new frame is now transformed into the reference frame's POV, so the discretized map should align properly
    - **Functions** 
      - getMarkerLocations
      - calculateHomography
      - warpImage
    - **Forwards results to:** map_discretization.py
                               localization.py
    - **Output:** the single most recent camera frame transformed to the reference as a numpy array
* mapping.py
    - **Gets data from** homography.py
    - **Purpose:** processes the first camera frame to produce a discrete map of the maze
    - **Functions** 
      - filter_map(): filter the image 
      - detect_corners(): detect the corners of the maze
      - fit_homography(): find homography to transform image to uniform dimensions and flat orientation
      - apply_homography(): transform image
      - discretize(): discretize the image into cells
      - detect_holes(): detect holes in the image
      - detect_walls(): detect walls in the image
    - **Forwards results to:** planning.py 
    -  **Output:** path 
* localization.py 
   - **Gets data from:** homography.py
   - **Purpose:** processes camera frames to determine position and velocity of pinball   
   - **Functions** localize_pinball(), get_ball_vector()
   - **Forwards results to:** planning.py
   - **Output:** 
* planning.py 
   - **Gets data from:** mapping.py, localization.py
   - **Purpose:** plans path for ball to take given the path and the current position
   - **Functions** 
     - generate_path()
   - **Forwards results to:** controller.py
   - **Output:** list of coordinates?
* controls.py
   - **Gets data from:** planning.py, localization.py
   - **Purpose:** converts intended path to motor commands, using PID and other control algorithms
   - **Functions** 
        - 
   - **Forwards results to:** serial.py
   - **Output:** motor command
* serial.py
   - **Gets data from:** control.py
   - **Purpose:** sends motor controls to the arduino
   - **Functions** 
        - send_motor_commands()
   - **Forwards results to:** Arduino
   - **Output:** motor command

* motor_controller.ino
   - **Gets data from:** control.py
   - **Purpose:** sends motor controls to the arduino
   - **Functions** 
        - send_motor_commands()
   - **Forwards results to:** servos
   - **Output:** motor command

Datatype Classes: 
- `pose`: x, y, vx, vy

