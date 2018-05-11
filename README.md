# Emotional NBack
Emotional NBack is one of three tasks used in the Adolescent Brain and Cognitive Development fMRI battery.  This project is unique from previous iterations in that it uses the flexibility of Python and PsychoPy to account for various interuptions that experimenters face, including but not limited to adjusting parameters to complete Run2, incorporating Practice and RecMem in one script, and easily incorporating multiple attempts at the task with the same participants among other benefits.

## Prerequisites
* PsychoPy
* Numpy
* Pandas
* Matplotlib
* Pyglet

## How to run
Open NBack_Final.py in Coder view and  click "Run".  A dialog box will open and ask for the participant information, session, run number, and handedness in dropdown menus.

Changes for different sites should be made in the siteConfig.yaml file.  Changes can be made regarding which keys can be used throughout the experiment, size of text, dimensions of the screen, and details about the MRI Scanner.

## Credits
_**Psychopy implementation by Tariq R. Cannonier**_

Tested with Psychopy 1.83.04; 
  _Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13._  
  _Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi:  
      10.3389/neuro.11.010.2008_  
      
## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

