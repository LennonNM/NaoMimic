# NaoMimic
## General description
To allow a Nao humanoid robot to Mimic the motion of a human by optical motion tracking.

For development: Use sepparate branch.
To clone stable release: Clone StableRelease branch.
For hsitory reference: Master branch (be careful!).

### Author
Lennon NM\
Pattern Recognition and Intelligent Systems Laboratory (PRIS-Lab)\
CORE division. 

### Equipment
* Optical Motion Capture System (MoCap): 
** HW: Prime 41, Optitrack.
** SW: Motive, Optitrack.
* Humanoid Robot Nao: H25, Aldebaran Robotics.
* Choregraphy: Aldebaran Robotics.
* Coding on Python: V 3.7

## Description
This project uses motion tracking data collected by a MoCap system, exported in CSV format.

The motion data corresponds to center of mass (COM) of the virtual 3D representation of a human's upper body sections as: Head, Torso, RArm (right arm) and LArm (left arm). The body's sections are mapped each with a Rigid Body on Motive. The Nao robot's body is also segmented in the same parts (Head, Torso, RArm, LArm), these segments correspond to the chain effectors of the robot, whose positions are controlled by space placing the end-effector of the chain (placing the COM of the Head, Torso, Right hand and Left arm of the robot). The spacial placing of the robot's end effectors is to be mapped with the 3D rigid bodies.

The relation within a specific rigid body spacial data (X, Y and Z axis and its rotations wX, wY and wZ) and the Nao robot's corresponding end-effector desired placing is obtained using linear regression (polyfit numpy's function for a first order degree polynom). The coefficients obtained are stored in a CSV file, which corresponds to the calibration results for a specific person, therefore called the Person's Calibration Profile.

To start the mimicking, it is needed to have stored the Calibration Profile of the person to mimic and the CSV file with the motion tracking data from MoCap.

The calibration process involves capturing the motion tracking data of a human immitating a Nao's choreography (executed using Choregraphy), this data is used to create the Calibration Profile. The reference for the calibration process is obtained by reading the sensing values from the Nao's motion sensors while it executes the calibration choreography (this part is needed to do only once, the reference files are applicable independently of the user).

## File Managing
### File Location
* **Dev_files:** Includes development files. Use only for reference.
** Aldebaran_Examples: Scripts with examples on Naoqi usage. Files can be obtained from oficial website: http://doc.aldebaran.com/1-14/naoqi/index.html
** Test_Data_MoCap: Choregraphy routines and motion tracking session files from Motive.
** Version_History: Development versions history. Each single version is stored in a single directory with the name "Ver_VersionNumber".
* **Current_Version:** Current version of NaoMimic. Follows the general structure of the mimicking tool.

### Nao Mimic structure
* **Mimicking tool scripts**
** Move.py: Main file. Connects to the Nao robot and send the motion instructions. Requires the Calibration Profile and the Choreography to run.
** CSVMOCAP_Func.py: Functions to manage CSV files to generate the data required to send to the Nao robot for the motion.
** Calibration.py: Creates the Calibration Profile CSV file. Requires the CSV files with the Nao reference data for each chain end-effector and the corresponding human data to calibrate.
** Calibrate_Func.py: Functions to support the calibration process.
** GetPositions.py: Used to export data sensed by the Nao's motion sensors to a CSV file to store the motion reference files for the calibration process.
** OffsetFile_Func.py: Functions to support reading and writting of calibration coefficients of the Calibration Profile.
** Error_Func.py: To support the management of some software usage errors with user friendly messages.
* **MoCap:** Stores the MoCap recording sessions files. 
* **Comparisons:** Stores files to graphically compare the motion data of a person with Nao's data. Helps to visualize the behavior of the data for specific motion. Use to compare the data in time to manually make adjustments to the CSV files used for the calibration process.
* **Choreography:** Stores the CSV files for the different choreographies to run on the Nao robot. Some examples are included.
* **Calbration:** Stores the calibration files.
** Human: Data to be calibrated. Store a single CSV file with data of a single rigid body (Head, Torso, RArm, LArm) for each rigid body for a single subject in a distinguishable directory. This data is used for the creation of a Calibration Profile. Some examples are included.
** NAO: Reference data of the motion of the Nao for the calibration process. Includes the default reference files, other files can be used.
** Profiles: Stores the Calibration Profiles.
** Routines: Stores the calibration routines from Choregraphy for the Nao to execute. Each routine focusses on generating useful motion information for a body section.

### Branch Management
* To collaborate on development: Clone from *StableRelease* branch and create a separate branch. Each new approved version is to be stored on Dev_Files/Version_History. 
* Stable release: The newest working version of the Mimicking tool will be maintained in the branch *StableRelease* for light cloning. 
* Full history: The *Master* branch will store the main versioning of the tool. Use only for reference or if a specific version different from the latest current stable is to be used.
** README.md will be updated with a summary of the main changes of each new version.
** Dev_Files will include different versions of the tool.
** Current_Version will contain the latest working version of the tool.
