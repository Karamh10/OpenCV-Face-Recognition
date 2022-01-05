# OpenCV-Face-Recognition:

- This program was written to recognize the existence of a face in a video stream from the front camera of a laptop.
- It was originally built on Windows and tested on Windows. It should work on Linux as well but however it might present some problems depending on the system. I do not have access to a Linux machine therefore I do not know what sort of problems it will present.
- The program also assumes that the user is being cooperative by looking at the camera and being in the frame.

## How it works: 
- To run the program, you need to install OpenCV-Python, [here](https://www.geeksforgeeks.org/how-to-install-opencv-for-python-in-windows/) is the link for Windows.  [Here](https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html) is the link for Linux.
- After that you need to make sure to run ``` pip install dlib ```.
- After that you run the code by running ```python FacialExp.py```.

### The program will:
- print "yes" at the terminal when you nod.
- print "no" at the terminal when you shake the head.
- print "mouth open" when you open your mouth.
- print "mouth closed" when you close your mouth.
- print "blink" when you blink.
