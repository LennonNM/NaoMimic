# NaoMimic
## General description
To allow a Nao humanoid robot to Mimic the motion of a human by optical motion tracking.
### Author
Lennon NM
Pattern Recognition and Intelligent Systems Laboratory (PRIS-Lab)
CORE division. 
### Equipment
- Optical Motion Capture System (MoCap): 
-- HW: Prime 41, Optitrack.
-- SW: Motive, Optitrack.
- Humanoid Robot Nao: H25, Aldebaran Robotics.
- Choregraphy: Aldebaran Robotics.
- Coding on Python: V 3.7
## Description
This project uses motion tracking data collected by a MoCap system, exported in CSV format.
The motion data corresponds to center of mass (COM) of the virtual 3D representation of a human's upper body sections as: Head, Torso, RArm (right arm) and LArm (left arm). The body's sections are mapped each with a Rigid Body on Motive.
The Nao robot's body is also segmented in the same parts (Head, Torso, RArm, LArm), these segments correspond to the chain effectors of the robot, whose positions are controlled by space placing the end-effector of the chain (placing the COM of the Head, Torso, Right hand and Left arm of the robot). The spacial placing of the robot's end effectors is to be mapped with the 3D rigid bodies.
The relation within a specific rigid body spacial data (X, Y and Z axis and its rotations wX, wY and wZ) and the Nao robot's corresponding end-effector desired placing is obtained using linear regression (polyfit numpy's function for a first order degree polynom). The coefficients obtained are stored in a CSV file, which corresponds to the calibration results for a specific person, therefore called the Person's Calibration Profile.
To start the mimicking, it is needed to have stored the Calibration Profile of the person to mimic and the CSV file with the motion tracking data from MoCap.
## Version Status
Development versions are maintained on Dev_Files directory.
- Ver_5: Calibration process requires a lot of human interaction (running the animations in Choregraphy, start recording in Motive, changing the animation to run on Choregraphy). Time coupling of the motion data (to make Human data comparable in time with the Nao's reference data for the calibration process) is done manually. Mimic is done from a stored choreography file in CSV format, no real-time streaming of data is used yet. 