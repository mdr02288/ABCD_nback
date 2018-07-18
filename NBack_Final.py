#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Part of the ABCD - fMRI Battery
Psychopy implementation by Tariq R. Cannonier
**********************************************************************************************
Tested with Psychopy 1.86.6; Psyexp Experiment Builder XML available upon request
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
import datetime
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui, info
from psychopy.constants import *  # things like STARTED, FINISHED
from psychopy.hardware.emulator import launchScan
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os, glob, sys, yaml, itertools  # handy system and path functions

## Escape from script with button combination.
## Adding assertions in case Taking too long to load frames
## Add assertion to check randomization 
## Place assumed refresh rate into logFile

# # Record Git Status in Subject Logs
# from subprocess import check_output, check_call, CalledProcessError
# try:
#     revision = check_output(['git','rev-parse', '--short', 'HEAD'])
#     revision = revision.strip()
#     gitInstalled = True
# except:
#     if os.path.exists('VERSION'):
#         with open('VERSION', 'r') as f:
#             revision = f.read()
#     else:
#         revision = ''
#     gitInstalled = False
# 
# if gitInstalled:
#     try:
#         check_call(['git', 'diff-files', '--quiet'])
#     except CalledProcessError:
#         revision = 'Task changes detected. Nearest head: %s' % revision
#         status_msg = check_output(['git', 'status'])
#         msg ="""%s
# 
# Warning: the experiment has unexpected changes.
# """ % status_msg
#         logging.critical(msg)
#         # core.quit()
# expInfo['git-revision'] = revision


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)
sys.getfilesystemencoding()

# Store info about the experiment session. 

# PLACE IN WHILE LOOP TO PREVENT EXPERIMENTER FROM MOVING ON WITH BLANK FIELDS
dlgCorrect = False
while not dlgCorrect:
    print "Please be sure to check you have the correct pGUID and Version before running the script!!"
    expName = 'Emo_Nback_20180527'  # from the Builder filename that created this script
    expInfo = {u'NARGUID': u'ABCD1234', u'Session': [u'Behavioral',u'MRI',u'Practice',u'RecMem'], u'Run': [u'All',u'Run2'],u'Handedness': [u'Right',u'Left'], u'Debugging':[True, False], u'Goggles':[False, True],u'Version':range(1,5)}
    #expInfo = {u'NARGUID': u'ABCD1234', u'Session': [u'Practice',u'Behavioral',u'MRI',u'RecMem'], u'Run': [u'All',u'Run2'],u'Handedness': [u'Right',u'Left'], u'Goggles':[True, False],u'Version':range(1,5)}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel

    # Confirm that information entered is correct
    dCorrect = gui.Dlg()
    dCorrect.addText('Is this information correct?')
    for i in expInfo.keys():
        dCorrect.addText('%s: %s' % (i, expInfo[i]))
    dCorrect.addField("Correct: ", choices=['No','Yes'])
    ok_data = dCorrect.show()
    
    # Check if the entered fields are valid.
    if len(expInfo['NARGUID']) != 8: # Make sure NARGUID is 8 chars long
        print "NARGUID must be 8 characters long!"
        dlgCorrect = False
    elif 'Yes' in ok_data: # Experimenter verified that information entered is correct
        dlgCorrect = True

# Preserve data fields to be the same as EPrime scripts
try:
    expInfo['DataFile.Basename'] = '%s_v%d-%s' % (expName,expInfo[u'Version'],expInfo['NARGUID'])
except TypeError:
    print "Task Ended early"
expInfo['Subject'] = 1
expInfo['ExperimentName'] = expName

# I don't know what any of these fields are...
# Preserving data fields to be the same as EPrime scripts
expInfo['Clock.Information'] = 0
expInfo['ConsecNonResp[Session]'] = 0
expInfo['ConsecRTLess200[Session]'] = 0 
expInfo['ExperimentVersion'] = '1.0.0.1180' 
expInfo['FontStyle'] = 'Verdana'; expInfo['Group'] = 1; expInfo['RunNumber'] = expInfo['Version']; 
expInfo['RuntimeCapabilities'] = 'Professional'; expInfo['RuntimeVersion'] = '2.0.10.356'; 
expInfo['RuntimeVersionExpected'] = '2.0.10.356'; 
expInfo['SessionDate'] = datetime.datetime.now().strftime(u'%m/%d/%Y'); expInfo['SessionStart'] = '';
expInfo['SessionTime'] = datetime.datetime.now().strftime(u'%H:%M:%S');
expInfo['StudioVersion'] = '2.0.10.252'; expInfo['SUBID'] = 0; expInfo['Target'] = 1; 
expInfo['TotalRespGreater200[Session]'] = 0; expInfo['TrialsPerRun[Session]'] = 160; 
expInfo['StimuliDir'] = 'Stimuli'+os.sep

expInfo['date'] = datetime.datetime.now().strftime(u'%Y-%m-%d_%H%M%S')  # add a simple timestamp

# Determine the file name and path to data file
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
pathname = os.path.join(os.getcwd(),u'data',u'NDAR_INV%s') % expInfo['NARGUID']
filename = os.path.join(pathname,u'NDAR_INV%s') % expInfo['NARGUID']

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# Create a different logFile for each of the tasks
if expInfo['Session'] in ['Behavioral','MRI']:
    filename = filename+'_WM'
    wildcard = '*WM*.csv'
elif expInfo['Session'] == 'Practice':
    filename = filename+'_NBack_Practice'
    wildcard = '*NBack_Practice*.csv'
else:
    filename = filename+'_REC'
    wildcard = '*REC*.csv'

# Make sure to avoid overwriting the previous logFile
if expInfo['Run'] == 'Run2':
    filename = filename+'-2'

#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Determine if siteConfig.yaml exists within the same directory as the task
# Edit paramters of the task to be site specificc
if os.path.exists('siteConfig.yaml'):
    with open('siteConfig.yaml') as f:
        config = yaml.safe_load(f)
else:
    copyMsg = ('Please copy configuration text file '
               '"siteConfig.yaml.example" to "siteConfig.yaml" '
               'and edit it with your trigger and buttons.')
    raise IOError(copyMsg)

# Print in log file Site Configuration
logging.exp('Using Site Configuration: %s' % config)

# Start Code - component code to be run before the window creation
## EKK Screen Edit of compiled script
import pyglet
display = pyglet.window.get_platform().get_default_display()
screens = display.get_screens()

# If we're debugging code, then make the window smaller
if expInfo['Debugging'] or expInfo['Goggles']:
    width = config['dimensions']['width']
    height = config['dimensions']['height']
    screenFull = False

    if expInfo['Debugging']:
        stimScale = .6
    elif expInfo['Goggles']:
        stimScale = (800*600.)/(1260*800) # Just scaling the screen down from standard size

else:
    width = screens[-1].width
    height = screens[-1].height
    screenFull = True
    stimScale = 1

# Create the window in which the stimuli will be presented
win = visual.Window(size=(width, height), fullscr=screenFull, screen=len(screens) - 1, allowGUI=False, allowStencil=False,
    monitor=u'testMonitor', color=128, colorSpace='rgb255',
    blendMode='avg', useFBO=True, units='deg')
    
# Record the frames that are dropped during the task
win.recordFrameIntervals = True

# store frame rate of monitor if we can measure it successfully
expInfo['Main.RefreshRate']=win.getActualFrameRate()

# Store frame rate of monitor if we can measure it successfully.  Make a rough guess if you cannot\
if not expInfo['Main.RefreshRate']:
    expInfo['Main.RefreshRate'] = 1.0/60.0
    notes = "Assuming default refresh rate: %f" % expInfo['Main.RefreshRate']
    log.exp(notes)

ISI = core.StaticPeriod(screenHz=expInfo['Main.RefreshRate'])

# Initialize components for Routine "intro"
introClock = core.Clock()

# Make text size in the displays using siteConfig.yaml
titleLetterSize = config['style']['titleLetterSize']*stimScale  # 3
textLetterSize = config['style']['textLetterSize']*stimScale  # 1.5
fixLetterSize = config['style']['fixLetterSize']*stimScale  # 2.5
wrapWidth = config['style']['wrapWidth']*stimScale  # 30
subtitleLetterSize = config['style']['subtitleLetterSize']*stimScale  # 1

# Create variables for events.  Use Title and Text.
events = []  # run, condition, onset, duration, value

# Create key for switching handedness.
if expInfo['Handedness'] == 'Right':
    hand = {'Match': config['keys']['Match'], 'NoMatch': config['keys']['NoMatch'], 'Next': config['keys']['Next'],'Quit': config['keys']['Quit']}
    handFlip = np.array([1,1])*stimScale
else:
    hand = {'Match': config['keys']['NoMatch'], 'NoMatch': config['keys']['Match'], 'Next': config['keys']['Next'],'Quit': config['keys']['Quit']}
    handFlip = np.array([-1,1])*stimScale
    
# Preserve EPrime data fields
expInfo['Nontarget'] = hand['NoMatch']
expInfo['Allowed'] = hand['Match']+hand['NoMatch']

###
### Defining variables.  Create image and text stimuli classes to make stimuli easier later.
###

# Create classes to easily instantiate text and image stimuli.
class nbackStim:
    def __init__(self,thisTrial,**kwargs):
        if not isinstance(thisTrial,dict):
            self.stim = visual.ImageStim(win=win, name=thisTrial,
                image=thisTrial, mask=None, ori=0, pos=np.array([0,0])*stimScale, size=np.array([10,10])*stimScale,
                color=[1,1,1],colorSpace='rgb', opacity=1,
                flipHoriz=False, flipVert=False,
                texRes=128, interpolate=True, depth=-1.0)
        else:
            if thisTrial['BlockType'] == 'Cue2Back':
                self.stim = visual.TextStim(win=win,ori=0,name='2Back',text='2-Back',font='Verdana',pos=[0,0],height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)
            elif thisTrial['BlockType'] == 'Fix15secProc':
                self.stim = []
            elif thisTrial['BlockType'] in ['0-Back','0Back','2-Back','2Back','Cue0Back','Rec']:
                if 'Stimuli' not in thisTrial['Stimulus']:
                    stimPath = expInfo['StimuliDir']+thisTrial['Stimulus']
                else:
                    stimPath = thisTrial['Stimulus']
                self.stim = visual.ImageStim(win=win, name=thisTrial['Stimulus'],
                    image=stimPath, mask=None, ori=0, pos=[0,0], size=np.array([10,10])*stimScale,#size=[10,10],
                    color=[1,1,1],colorSpace='rgb', opacity=1,
                    flipHoriz=False, flipVert=False,
                    texRes=128, interpolate=True, depth=-1.0)
#                self.stim = visual.ImageStim(win=win, name=thisTrial['Stimulus'],
#                    image=expInfo['StimuliDir']+thisTrial['Stimulus'], mask=None, ori=0, pos=[0,0], size=np.array([10,10])*stimScale,#size=[10,10],
#                    color=[1,1,1],colorSpace='rgb', opacity=1,
#                    flipHoriz=False, flipVert=False,
#                    texRes=128, interpolate=True, depth=-1.0)

        # Reusing the global stimuli with each class instance 
        self.pointerFingerPrompt = pointerFingerPrompt
        self.middleFingerPrompt = middleFingerPrompt
        self.pointerLabelPrompt = pointerLabelPrompt
        self.middleLabelPrompt = middleLabelPrompt
        self.target = target
        self.fixation = bFixation
        self.pfixation = pFixation
        self.alldone = allDone
        self.trial = thisTrial
        self.response = []
        self.time = {}
        self.frames = 0
        if kwargs is not None and 'ISI' in kwargs.keys():
            self.ISI = kwargs['ISI'] 

    def cue2Back(self,expHandler,tHandler):
        '''A method to introduce 2Back to participant.  Record the onset.'''

        # Set timing duration and record clock
        cue2BackDuration = 2.5
        cueFixDuration = 0.5
        stimRTTime = []
        routineTimer.add(cueFixDuration)
        cueFixStartTime = globalClock.getTime()
        
        # Draw and present purple fixation cross and record onset time
        self.pfixation.setAutoDraw(True)
        cueFixOnsetTime = globalClock.getTime()
        
        # Present purple fixation cross and allow experimenter to quit if needed
        while routineTimer.getTime() > 0:
            win.flip()
            
            # Allow experimenter to exit the script by pressing the quit key.  Will quit at the end of the stim presentation (is not immediate).
            if not self.response:
                self.response = event.getKeys(keyList=hand['Quit'],timeStamped=globalClock)
                if self.response: stimRTTime = globalClock.getTime()
        
        # Stop drawing fixation cross
        cueFixOffsetTime = globalClock.getTime()
        self.pfixation.setAutoDraw(False)
        cueFixFinishTime = globalClock.getTime()
        
        # Set clocks appropriately
        cue2BackStartTime = globalClock.getTime()
        routineTimer.add(cue2BackDuration) # For non-slip timings.  Add time for each trial so that script continues at the appropriately determined time.

        # Draw and present 2Back and record onset time
        self.stim.setAutoDraw(True)
        cue2BackOnsetTime = globalClock.getTime()

        # Present 2Back prompt and allow experimenter to quit if needed
        while routineTimer.getTime() > 0:
            win.flip()

            # Allow experimenter to exit the script by pressing the quit key. Will quit at the end of the trial (is not immediate).
            if not self.response:
                self.response = event.getKeys(keyList=hand['Quit'],timeStamped=globalClock)
                if self.response: stimRTTime = globalClock.getTime()
            
        # Stop drawing 2Back prompt and record offset time
        cue2BackOffsetTime = globalClock.getTime()
        self.stim.setAutoDraw(False)
        cue2BackFinishTime = globalClock.getTime()

        # Record times and save data
        self.time = {'CueFix.Duration': cueFixDuration, 'CueFix.OnsetTime': cueFixOnsetTime, 
            'CueFix.OffsetTime': cueFixOffsetTime, 'CueFix.StartTime': cueFixStartTime,
            'CueFix.FinishTime': cueFixFinishTime,
            'Cue2Back.Duration': cue2BackDuration, 'Cue2Back.OnsetTime': cue2BackOnsetTime, 
            'Cue2Back.OffsetTime': cue2BackOffsetTime,'Cue2Back.StartTime': cue2BackStartTime,
            'Cue2Back.FinishTime': cue2BackFinishTime}
        self.saveData(expHandler,tHandler)

    def cueTarget(self,expHandler,tHandler):
        '''A method to allow the stim to draw and flip the Target image.  Record the onset.'''

        # Set timing duration and record clock
        cueTargetDuration = 2.5
        cueFixDuration = 0.5
        cueFixStartTime = globalClock.getTime()
        routineTimer.add(cueFixDuration)

        # Draw and present purple fixation cross and record onset time
        self.pfixation.setAutoDraw(True)
        cueFixOnsetTime = globalClock.getTime()

        # Present purple fixation cross and allow experimenter to quit if needed
        while routineTimer.getTime() > 0:
            win.flip()

            # Allow experimenter to exit the script by pressing the quit key.  Will quit at the end of the stim presentation (is not immediate).
            if not self.response:
                self.response = event.getKeys(keyList=hand['Quit'],timeStamped=globalClock)
                if self.response: stimRTTime = globalClock.getTime()
                
        # Stop drawing the fixation cross
        cueFixOffsetTime = globalClock.getTime()
        self.pfixation.setAutoDraw(False)
        cueFixFinishTime = globalClock.getTime()
        
        # Draw and present 2Back and record onset time
        cueTargetStartTime = globalClock.getTime()
        routineTimer.add(cueTargetDuration) # For non-slip timings.  Add time for each trial so that script continues at the appropriately determined time.

        # Draw target stimuli and record onset time
        self.stim.pos += (3,0)
        self.target.setAutoDraw(True)
        self.stim.setAutoDraw(True)
        cueTargetOnsetTime = globalClock.getTime()

        # Present target stimuli and allow experimenter to quit if needed
        while routineTimer.getTime() > 0:
            win.flip()

            # Allow experimenter to exit the script by pressing the quit key. Will quit at the end of the trial (is not immediate).
            if not self.response:
                self.response = event.getKeys(keyList=hand['Quit'],timeStamped=globalClock)

        # Stop drawing the target stimuli and record offset time
        cueTargetOffsetTime = globalClock.getTime()
        self.target.setAutoDraw(False)
        self.stim.setAutoDraw(False)
        cueTargetFinishTime = globalClock.getTime()

        # Record times and save data
        self.time = {'CueFix.Duration':cueFixDuration, 'CueFix.OnsetTime': cueFixOnsetTime,
            'CueFix.OffsetTime': cueFixOffsetTime, 'CueFix.StartTime': cueFixStartTime,
            'CueFix.FinishTime': cueFixFinishTime,
            'CueTarget.Duration': cueTargetDuration, 'CueTarget.OnsetTime': cueTargetOnsetTime, 
            'CueTarget.OffsetTime': cueTargetOffsetTime, 'CueTarget.StartTime': cueTargetStartTime,
            'CueTarget.FinishTime': cueTargetFinishTime}
        self.saveData(expHandler,tHandler)

    def presentStim(self,expHandler,tHandler):
        '''A method to allow the stim to draw and flip stimuli.  Record onset time and button press.'''

        # Set timing durations and record clocks for accurate Trial timing
        stimDuration = 2.0
        fixDuration = 0.5
        stimRTTime = []
        routineTimer.add(stimDuration) # For non-slip timings.  Add time for each trial so that script continues at the appropriately determined time.
        stimStartTime = globalClock.getTime()

        # Draw stimuli and response prompts
        self.stim.setAutoDraw(True)
        self.middleLabelPrompt.setAutoDraw(True)
        self.middleFingerPrompt.setAutoDraw(True)
        self.pointerLabelPrompt.setAutoDraw(True)
        self.pointerFingerPrompt.setAutoDraw(True)

        # Clear keys and Get Stimulus Onset Time
        event.clearEvents()
        stimOnsetTime = globalClock.getTime()

        # Present stimuli and record responses
        while routineTimer.getTime() > 0: # Timer will go through for stimulus presented
            win.flip()

            # Allow experimenter to exit the script by pressing the quit key. Will quit at the end of the trial (is not immediate).
            if not self.response:
                self.response = event.getKeys(keyList=hand['Quit']+hand['Match']+hand['NoMatch'],timeStamped=globalClock)
                if self.response: stimRTTime = globalClock.getTime()
        if not stimRTTime: stimRTTime = 0

        # Record Stimuli Offset Time and stop drawing stimuli
        stimOffsetTime = globalClock.getTime()
        self.stim.setAutoDraw(False)
        self.middleLabelPrompt.setAutoDraw(False)
        self.middleFingerPrompt.setAutoDraw(False)
        self.pointerLabelPrompt.setAutoDraw(False)
        self.pointerFingerPrompt.setAutoDraw(False)
        stimFinishTime = globalClock.getTime()

        # Get Stimulus Start Time and start drawing stimuli on screen 
        fixStartTime = globalClock.getTime() 
        routineTimer.add(fixDuration) # For non-slip timings.  Add time for each trial so that script continues at the appropriately determined time.
        self.fixation.setAutoDraw(True)

        # Record fixation onset time and present fixation cross
        fixOnsetTime = globalClock.getTime()
        while routineTimer.getTime() > 0:
            win.flip()

        # Stop drawing fixation cross and record offset time
        fixOffsetTime = globalClock.getTime()
        self.fixation.setAutoDraw(False)
        fixFinishTime = globalClock.getTime()

        # Record times and save data
        self.time = {'Stim.Duration': stimDuration, 'Stim.FinishTime': stimFinishTime, 'Stim.RTTime':stimRTTime, 
            'Stim.OffsetTime': stimOffsetTime, 'Stim.OnsetTime': stimOnsetTime, 'Stim.StartTime': stimStartTime, 
            'Fix.Duration': fixDuration, 'Fix.FinishTime': fixFinishTime, 'Fix.OffsetTime': fixOffsetTime, 
            'Fix.OnsetTime': fixOnsetTime, 'Fix.StartTime': fixStartTime}
        self.saveData(expHandler,tHandler)

    def fixBlock(self,expHandler,tHandler):
        '''Present a block of a fixation cross to participant'''
        
        # Set and record clocks for accurate Trial timing
        fixDuration = 15.0
        routineTimer.add(fixDuration)
        fixStartTime = globalClock.getTime()

        # Draw fixation and record onset time
        self.fixation.setAutoDraw(True)
        fixOnsetTime = globalClock.getTime()
        event.clearEvents()

        # Present fixation cross and quit script if needed.
        while routineTimer.getTime() > 0:
            win.flip()

            # Allow experimenter to exit the script by pressing the quit key. Will quit at the end of the block (is not immediate).
            if not self.response:
                self.response = event.getKeys(keyList=hand['Quit'],timeStamped=globalClock)

        # Stop drawing fixation cross and record offset time
        fixOffsetTime = globalClock.getTime()
        self.fixation.setAutoDraw(False)
        fixFinishTime = globalClock.getTime()

        # Record times and save data
        self.time = {'Fix15sec.Duration': fixDuration, 'Fix15sec.StartTime': fixStartTime, 
            'Fix15sec.OnsetTime': fixOnsetTime, 'Fix15sec.OffsetTime': fixOffsetTime,
            'Fix15sec.FinishTime': fixFinishTime}
        self.saveData(expHandler,tHandler)

    def feedback(self):
        '''Evaluate participant responses and determine the correct feedback to give'''

        #Draw fixaton cross after stimulus presented
        fixationDuration = .5
        feedbackDuration = 1.0
        routineTimer.add(feedbackDuration+fixationDuration)
        self.fixation.setAutoDraw(True)

        # Present stimuli for timer and stop drawing stimuli
        while routineTimer.getTime() > 1.0:
            win.flip()
        self.fixation.setAutoDraw(False)

        # Determine type of feedback for participant
        if not self.response:
            feedback = tooslow
        elif (list(set(hand['Match']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'Match') or (list(set(hand['NoMatch']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'No Match') or (list(set(hand['Match']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'Old') or (list(set(hand['NoMatch']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'New'):
            feedback = correct
        else:
            feedback = incorrect

        # Present feedback
        feedback.setAutoDraw(True)
        while routineTimer.getTime() > 0:
            win.flip()
        feedback.setAutoDraw(False)

    def saveData(self,expHandler,tHandler):
        '''Save Data using data hander'''

        # Determine criteria for accuracy in WM and REC
        if self.trial['BlockType'] in ['Cue0Back','Cue2Back','Fix15secPROC']:
            # Should not have an accuracy rating during 15 second fixation presentation or Cueing 0- or 2-Back
            accuracy = ''
            
        elif not self.response:
            # No Response
            accuracy = 0

        elif (list(set(hand['Match']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'Match') or (list(set(hand['NoMatch']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'No Match'):
            # Determine criteria for accuracy in WM
            accuracy = 1

        elif (list(set(hand['Match']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'Old') or (list(set(hand['NoMatch']) & set(self.response[0])) and self.trial['Stim_CRESP'] == 'New'):
            # Determine criteria for accuracy in REC
            accuracy = 1
            
        else:
            # Otherwise, participant's response was incorrect
            accuracy = 0

        # Record participant responses
        if self.response:
            # Record the participant's response, reaction time, and Correct Response
            tHandler.addData('Stim.RESP',self.response[0][0])
            if self.response[0][0] != 'escape':
                tHandler.addData('Stim.RT',int((self.response[0][1]-self.time['Stim.OnsetTime'])*1000))
        else:
            tHandler.addData('Stim.RESP','')
            tHandler.addData('Stim.RT',0)

        # Record trial correct response
        if not self.trial['Stim_CRESP']:
            self.trial['Stim_CRESP'] = ''
        tHandler.addData('Stim.CRESP',self.trial['Stim_CRESP'])

        # Add fields for all time measurements in the time dictionary (i.e. StimOnset, fixationDuration, etc.)
        for i in self.time.keys():
            tHandler.addData(i,int(self.time[i]*1000))

        # Add participant accuracy and the correct response for the trial
        tHandler.addData('Stim.ACC',accuracy)
        expHandler.nextEntry()

        # Exit task if the escape key was pressed
        if self.response and 'escape' in self.response[0]:
            exitProtocol()

def nBackBlock(taskList,taskName):
    '''Iterate through a block of the nBack task.'''

    # Load the 2Back task list so that it can be presented to the participant
    nBack = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(taskList),
        seed=None, name=taskName)
    thisExp.addLoop(nBack)
    thisTrial = nBack.trialList[0]

    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial' + "['{0}']").format(paramName)

    # Iterate through each stimuli in the tasklist csv file
    if expInfo['Session'] == 'MRI':

        # Delay the task while the scanner starts
        if config['siteScanner']['scanner'] in ['Siemens','Phillips']:
            triggerCount = 0
            triggerToInitScan = 1
            scannerDelayTime = 6.4
            event.clearEvents()
            waitingScreen.setAutoDraw(True)
            
            while triggerCount < triggerToInitScan:
                win.flip()
                triggerReceived = event.getKeys(keyList=hand['Trigger']+hand['Quit'])
                
                if triggerReceived and triggerReceived[0] in hand['Trigger']:
                   triggerCount += 1
                   print triggerReceived, triggerCount
                   # Stop drawing waiting screen, draw black fixation cross while MRI starts
                   routineTimer.reset(t=scannerDelayTime)
                   while routineTimer.getTime() > 0:
                        win.flip()
                   waitingScreen.setAutoDraw(False)
                elif triggerReceived and 'escape' in triggerReceived:
                   print triggerReceived
                   exitProtocol()

        elif config['siteScanner']['scanner'] == 'GE': 

            # Define parameters to wait for scanner
            routineTimer.reset()
            triggerCount = 0
            triggerToInitScan = 16
            event.clearEvents()
            waitingScreen.setAutoDraw(True)

            # Present a black fixation cross and wait for the necessary number of trigger signals from scanner
            while triggerCount < triggerToInitScan:
                win.flip()
                triggerReceived = event.getKeys(keyList=hand['Trigger']+hand['Quit'])

                # If the trigger was received, increment the trigger counter. Exit while loop when counter is equal to triggerToInitScan
                if triggerReceived and triggerReceived[0] in hand['Trigger']:
                    triggerCount += 1
                    print triggerReceived, triggerCount
                elif triggerReceived and 'escape' in triggerReceived:
                    print triggerReceived
                    exitProtocol()
                    
            # Stop waiting for scanner and trigger the rest of the task
            waitingScreen.setAutoDraw(False)
            routineTimer.reset()

    else: # Task will be completed behaviorally (without Scanner)
        routineTimer.reset()

    # Iterate through all trials and present stimuli accordingly
    for thisTrial in nBack:
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial' + "['{0}']").format(paramName)

        # Evaluate the type of trial for each iteration.
        if 'Cue' in thisTrial['BlockType']:
            # Load stimuli
            nBackPresent = nbackStim(thisTrial,ISI=ISI)

            # If Present the target or indicate a 2Back trial to participant
            if thisTrial['BlockType'] == 'Cue2Back':
                nBackPresent.cue2Back(thisExp,nBack)
            elif thisTrial['BlockType'] == 'Cue0Back':
                nBackPresent.cueTarget(thisExp,nBack)

        elif 'Fix15secPROC' in thisTrial['BlockType']:
            # Present a block of a fixation cross for 15seconds
            nBackPresent = nbackStim(thisTrial)
            nBackPresent.fixBlock(thisExp,nBack)

        else:
            # Present the trials to participant
            nBackPresent = nbackStim(thisTrial)
            nBackPresent.presentStim(thisExp,nBack)

            # Present feedback if the participant is doing practice
            if expInfo['Session'] == 'Practice' or recPractice:
                nBackPresent.feedback()

def plotData(fname):
    '''A protocol to plot benchmark data when the script exits.  Will run at the end of the experiment.'''
    import pandas as pd
    import matplotlib.pyplot as plt
    
    plt.xkcd()
    
    # Import NBack data
    nbackData = pd.read_csv(fname)
    
    # Parse out NaN in dataset
    accuracy = nbackData['Stim.ACC']
    accuracy = accuracy.dropna(axis=0, how='any')
    rt = nbackData['Stim.RT']
    rt = rt.dropna(axis=0, how='any')
    
    x_vals = [1, 1]
    
    # Start plotting data
    fig, ax = plt.subplots(1,2)
    ax[0].bar(x_vals[0],np.mean(accuracy),align='center')
    ax[0].set_xlim([0,2])
    ax[0].set_ylim([0,1])
    ax[0].set_xticks([])
    ax[0].set_title('Accuracy')
    
    ax[1].bar(x_vals[1],np.mean(rt[rt>0]),align='center')
    ax[1].set_xlim([0,2])
    ax[1].set_xticks([])
    ax[1].set_title('Reaction Time (RT)')
    
    # Reveal data points
    print "Plotting Data"
    plt.show()
    print "Data plotted"
    
    


    print "Work in progress..."

def formatOutput(fname):
    '''A protocol to reorganize task output file to more closely mimic EPrime outputs.'''
    import pandas as pd
    
    # Create the list of headers that the script should reorganize and create the designated order from the EPrime Version
    if expInfo['Session'] in ['Behavioral','MRI']: 
        headerList = ['ExperimentName','Subject','Session','Allowed','Clock.Information',
            'ConsecNonResp[Session]','ConsecRTLess200[Session]','DataFile.Basename','ExperimentVersion','FontStyle','Group',
            'Handedness','Main.RefreshRate','NARGUID','Nontarget','RandomSeed','RunNumber','RuntimeCapabilities','RuntimeVersion',
            'RuntimeVersionExpected','RunTrialNumber[Session]','SessionDate','SessionStartDateTimeUtc','SessionTime','StimuliDir',
            'StudioVersion','SUBID','Target','TotalRespGreater200[Session]','TrialsPerRun[Session]','triggercode','Block',
            'BlockType','ConsecNonResp[Block]','ConsecRTLess200[Block]','ConsecSameResp','ControlAcc','CorrectResponse',
            'Cue2Back.Duration','Cue2Back.DurationError','Cue2Back.FinishTime','Cue2Back.OffsetDelay','Cue2Back.OffsetTime',
            'Cue2Back.OnsetDelay','Cue2Back.OnsetTime','Cue2Back.OnsetToOnsetTime','Cue2Back.StartTime','CueFix.Duration','CueFix.DurationError',
            'CueFix.FinishTime','CueFix.OffsetDelay','CueFix.OffsetTime','CueFix.OnsetDelay','CueFix.OnsetTime','CueFix.OnsetToOnsetTime',
            'CueFix.RTTime','CueFix.StartTime','CueTarget.Duration','CueTarget.DurationError','CueTarget.FinishTime','CueTarget.OffsetDelay',
            'CueTarget.OffsetTime','CueTarget.OnsetDelay','CueTarget.OnsetTime','CueTarget.OnsetToOnsetTime','CueTarget.StartTime','Fix.Duration',
            'Fix.DurationError','Fix.FinishTime','Fix.OffsetDelay','Fix.OffsetTime','Fix.OnsetDelay','Fix.OnsetTime','Fix.OnsetToOnsetTime',
            'Fix.StartTime','Fix15sec.Duration','Fix15sec.DurationError','Fix15sec.FinishTime','Fix15sec.OffsetDelay','Fix15sec.OffsetTime',
            'Fix15sec.OnsetDelay','Fix15sec.OnsetTime','Fix15sec.OnsetToOnsetTime','Fix15sec.StartTime','Procedure[Block]','Run1Block1','Run1Block2',
            'Run1Block3','Run1Block4','Run1Block5','Run1Block6','Run1Block7','Run1Block8','Run2Block1','Run2Block2','Run2Block3','Run2Block4','Run2Block5',
            'Run2Block6','Run2Block7','Run2Block8','Running[Block]','RunTrialNumber[Block]','Stim.ACC','Stim.CRESP','Stim.Duration','Stim.DurationError',
            'Stim.FinishTime','Stim.OffsetDelay','Stim.OffsetTime','Stim.OnsetDelay','Stim.OnsetTime','Stim.OnsetToOnsetTime','Stim.RESP','Stim.RT',
            'Stim.RTTime','Stim.StartTime','StimType','Stimulus','TargetType','TotalRespGreater200[Block]','TrialsPerRun[Block]','v1ProcList','v1ProcList.Cycle',
            'v1ProcList.Sample','Trial','GetReady.DurationError','GetReady.OffsetDelay','GetReady.OffsetTime','GetReady.OnsetDelay','GetReady.OnsetTime',
            'GetReady.OnsetToOnsetTime','GetReady.RTTime','GetReady2.DurationError','GetReady2.OffsetDelay','GetReady2.OffsetTime','GetReady2.OnsetDelay',
            'GetReady2.OnsetTime','GetReady2.OnsetToOnsetTime','GetReady2.RTTime','Procedure[Trial]','Running[Trial]','SiemensPad.FinishTime','SiemensPad.OffsetDelay',
            'SiemensPad.OffsetTime','SiemensPad.OnsetDelay','SiemensPad.OnsetTime','SiemensPad.OnsetToOnsetTime','SiemensPad.RTTime','Waiting4Scanner','Waiting4Scanner.Cycle',
            'Waiting4Scanner.Sample','Waiting4Scanner2','Waiting4Scanner2.Cycle','Waiting4Scanner2.Sample']
    elif expInfo['Session'] == 'RecMem':
        headerList = ['ExperimentName','Subject','Session','Allowed','Clock.Information','DataFile.Basename','ExperimentVersion','FontStyle','Group','Handedness',
        'Main.RefreshRate','NARGUID','NewResp','OldResp','RandomSeed','RunNumber','RuntimeCapabilities','RuntimeVersion','RuntimeVersionExpected','SessionDate',
        'SessionStartDateTimeUtc','SessionTime','StimuliDir','StudioVersion','SUBID','Block','Fix.Duration[Block]','Fix.DurationError[Block]','Fix.FinishTime[Block]',
        'Fix.OnsetDelay[Block]','Fix.OnsetTime[Block]','Fix.OnsetToOnsetTime[Block]','Fix.StartTime[Block]','GetReady.Duration','GetReady.DurationError','GetReady.FinishTime',
        'GetReady.OnsetDelay','GetReady.OnsetTime','GetReady.OnsetToOnsetTime','GetReady.RESP','GetReady.StartTime','Instruction1.DurationError','Instruction1.OnsetDelay',
        'Instruction1.OnsetTime','Instruction1.OnsetToOnsetTime','Instruction2.DurationError','Instruction2.OnsetDelay','Instruction2.OnsetTime','Instruction2.OnsetToOnsetTime',
        'Instruction7.DurationError','Instruction7.OnsetDelay','Instruction7.OnsetTime','Instruction7.OnsetToOnsetTime','Instruction8.DurationError','Instruction8.OnsetDelay',
        'Instruction8.OnsetTime','Instruction8.OnsetToOnsetTime','Instruction9.DurationError','Instruction9.OnsetDelay','Instruction9.OnsetTime','Instruction9.OnsetToOnsetTime',
        'IntroButtonMap.Duration','IntroButtonMap.DurationError','IntroButtonMap.FinishTime','IntroButtonMap.OnsetDelay','IntroButtonMap.OnsetTime','IntroButtonMap.OnsetToOnsetTime',
        'IntroButtonMap.RESP','IntroButtonMap.StartTime','Practice','PreStimFix.Duration[Block]','PreStimFix.DurationError[Block]','PreStimFix.FinishTime[Block]','PreStimFix.OnsetDelay[Block]',
        'PreStimFix.OnsetTime[Block]','PreStimFix.OnsetToOnsetTime[Block]','PreStimFix.StartTime[Block]','Procedure[Block]','Run1','Run2','Running[Block]','Stim.ACC[Block]',
        'Stim.CRESP[Block]','Stim.Duration[Block]','Stim.DurationError[Block]','Stim.FinishTime[Block]','Stim.OnsetDelay[Block]','Stim.OnsetTime[Block]','Stim.OnsetToOnsetTime[Block]',
        'Stim.RESP[Block]','Stim.RT[Block]','Stim.RTTime[Block]','Stim.StartTime[Block]','StimType[Block]','Stimulus[Block]','v1ProcList','v1ProcList.Cycle','v1ProcList.Sample','VFDuration[Block]',
        'Trial','CorrectResponse','Fix.Duration[Trial]','Fix.DurationError[Trial]','Fix.FinishTime[Trial]','Fix.OnsetDelay[Trial]','Fix.OnsetTime[Trial]','Fix.OnsetToOnsetTime[Trial]',
        'Fix.StartTime[Trial]','PracticeList','PracticeList.Cycle','PracticeList.Sample','PreStimFix.Duration[Trial]','PreStimFix.DurationError[Trial]','PreStimFix.FinishTime[Trial]',
        'PreStimFix.OnsetDelay[Trial]','PreStimFix.OnsetTime[Trial]','PreStimFix.OnsetToOnsetTime[Trial]','PreStimFix.StartTime[Trial]','Procedure[Trial]','ReadyList','ReadyList.Cycle',
        'ReadyList.Sample','Running[Trial]','Stim.ACC[Trial]','Stim.CRESP[Trial]','Stim.Duration[Trial]','Stim.DurationError[Trial]','Stim.FinishTime[Trial]','Stim.OnsetDelay[Trial]',
        'Stim.OnsetTime[Trial]','Stim.OnsetToOnsetTime[Trial]','Stim.RESP[Trial]','Stim.RT[Trial]','Stim.RTTime[Trial]','Stim.StartTime[Trial]','StimType[Trial]','Stimulus[Trial]',
        'SyncSlide.Duration','SyncSlide.DurationError','SyncSlide.FinishTime','SyncSlide.OnsetDelay','SyncSlide.OnsetTime','SyncSlide.OnsetToOnsetTime','SyncSlide.RESP','SyncSlide.StartTime',
        'SyncSlideDur','VFDuration[Trial]']
    elif expInfo['Session'] == 'Practice':
        print "Practice Files also need to be organized similarly to above lol"

    # Read in data from output
    rawData = pd.read_csv(fname)
    newFname = fname.replace('.csv','_Corrected.csv')
    validHeader = []

    # Iterate through headerList and create a new file with the reorganized information
    for colHeader in headerList:
        # Determine if the element in the headerList exists in the Data computed.
        # Create and extend a list of valid headers that work
        try:
            rawData[colHeader]
            validHeader.extend([colHeader])
        except KeyError:
            print "This column, %s, was not in the data file" % colHeader        

    # Reorder and save
    orgData = rawData[validHeader]
    orgData.to_csv(fname, index=False) # Remove index from output file

def endScreen():
        '''Present a fixation cross and "all done" message at end of experiment '''
        
        # Set and record clocks for accurate Trial timing
        fixDuration = 5.0
        routineTimer.add(fixDuration)
        fixStartTime = globalClock.getTime()

        # Draw fixation and record onset time
        bFixation.setAutoDraw(True)
        fixOnsetTime = globalClock.getTime()
        event.clearEvents()

        # Present fixation cross and quit script if needed.
        while routineTimer.getTime() > 0:
            win.flip()

        # Stop drawing fixation cross and record offset time
        fixOffsetTime = globalClock.getTime()
        bFixation.setAutoDraw(False)
        fixFinishTime = globalClock.getTime()
        
        # Draw "all done" screen and record onset time
        allDone.setAutoDraw(True)
        allDoneOnsetTime = globalClock.getTime()

        # Present "all done" screen and allow experimenter to quit if needed
        win.flip()
        theseKeys = event.waitKeys(keyList=['space'])
        if theseKeys > 0: 
            # Stop drawing the target stimuli and record offset time
            allDoneOffsetTime = globalClock.getTime()
            allDone.setAutoDraw(False)
            allDoneFinishTime = globalClock.getTime()
        
        # Record times and save data ** IS THIS DATA INCLUDED IN OUTPUT FILE? if so, need to edit.
        #self.time = {'Fix5sec.Duration': fixDuration, 'Fix5sec.StartTime': fixStartTime, 
        #    'Fix5sec.OnsetTime': fixOnsetTime, 'Fix5sec.OffsetTime': fixOffsetTime,
        #    'Fix5sec.FinishTime': fixFinishTime}
        #self.saveData(expHandler,tHandler)

def exitProtocol():
    '''A protocol to save all data  before the script exits.  Will run at the end of the script or when the 
    escape key is pressed during instructions or a participant's response.'''

    # If the subdirectory for the file does not exist, create it.
    if not os.path.exists(pathname):
        os.makedirs(pathname)

    # Save the data in wide format and in Pickle
    thisExp.saveAsWideText(filename+'.csv')
    thisExp.saveAsPickle(filename)
    
    # Find the last dataFile in the list of data
    listedFiles = glob.glob(pathname+os.sep+wildcard)
    fileNum = len(listedFiles)-1
    filename.replace('.csv','_%d.csv'%fileNum)

    print listedFiles
    print listedFiles[fileNum]

    # Format Output file to look like EPrime outputs
    formatOutput(listedFiles[fileNum])

    # Note the number of dropped frames and print to log file
    print('Overall, %i frames were dropped.' % win.nDroppedFrames)
    logging.flush()

    # make sure everything is closed down
    thisExp.abort() # or data files will save again on exit
    win.close()
    core.quit()

#    try:
#        plotData(fname)
#    except KeyError:
#        print "Experiment ended before data was collected.  Can't provide a plot :("

# Initialize Intro/End Screens
introTitle = visual.TextStim(win=win,ori=0,name='introTitle',text='N-Back',font='Verdana',pos=np.array([0,0])*stimScale,height=titleLetterSize, wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
blankScreen = visual.TextStim(win=win,ori=0,name='blankScreen',text='',font='Verdana',pos=np.array([0,0])*stimScale,height=titleLetterSize,wrapWidth=wrapWidth)
pFixation = visual.TextStim(win=win,ori=0,name='pFixation',text='+',font='Verdana',pos=np.array([0,0])*stimScale,height=fixLetterSize,wrapWidth=wrapWidth,color='#FF00FF',colorSpace='rgb',opacity=1,depth=1.0)
bFixation = visual.TextStim(win=win,ori=0,name='bFixation',text='+',font='Verdana',pos=np.array([0,0])*stimScale,height=fixLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)
allDone = visual.TextStim(win=win,ori=0,name='allDone',text='All done!',font='Verdana',pos=np.array([0,0])*stimScale,height=fixLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)

# Initialize various stimuli 
target = visual.TextStim(win=win,ori=0,name='target',text="Target = ",font='Verdana',pos=np.array([-5,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)
twoBack = visual.TextStim(win=win,ori=0,name='2Back',text='2-Back',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)
correct = visual.TextStim(win=win,ori=0,name='correct',text="Correct!",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='#00FF00',colorSpace='rgb',opacity=1,depth=1.0)
incorrect = visual.TextStim(win=win,ori=0,name='incorrect',text="Incorrect!",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='#FF0000',colorSpace='rgb',opacity=1,depth=1.0)
tooslow = visual.TextStim(win=win,ori=0,name='tooslow',text="Too Slow!",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='#FFFF00',colorSpace='rgb',opacity=1,depth=1.0)
pointerFingerPrompt = visual.TextStim(win=win,ori=0,text='POINTER',font='Verdana',pos=np.array([-4,-8])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
middleFingerPrompt = visual.TextStim(win=win,ori=0,text='MIDDLE',font='Verdana',pos=np.array([4,-8])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
if expInfo['Session'] == 'RecMem':
    pointerLabelPrompt = visual.TextStim(win=win,ori=0,text='OLD',font='Verdana',pos=np.array([-4,-7])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    middleLabelPrompt = visual.TextStim(win=win,ori=0,text='NEW',font='Verdana',pos=np.array([4,-7])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
else:
    pointerLabelPrompt = visual.TextStim(win=win,ori=0,text='MATCH',font='Verdana',pos=np.array([-4,-7])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    middleLabelPrompt = visual.TextStim(win=win,ori=0,text='NO MATCH',font='Verdana',pos=np.array([4,-7])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)

# Create some handy timers
instructionsClock = core.Clock()
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
recPractice = False

if expInfo['Session'] == 'Practice':

    # Initialize Images in Instruction screens
    practiceScreen1_1 = visual.TextStim(win=win,ori=0,name='practiceScreen1_1',text='In this game, you will see different pictures.',alignHoriz='center',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen1_2 = visual.TextStim(win=win,ori=0,name='practiceScreen1_2',text='These pictures will be...',alignHoriz='center',font='Verdana',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen2 = visual.TextStim(win=win,ori=0,name='practiceScreen2',text='Faces',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    PracticeNC1 = nbackStim(expInfo['StimuliDir']+'PracticeNC1.bmp') 
    practiceScreen3 = visual.TextStim(win=win,ori=0,name='practiceScreen3',text='Places',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    Place1 = nbackStim(expInfo['StimuliDir']+'Place1.bmp') 
    practiceScreen4_1 = visual.TextStim(win=win,ori=0,name='practiceScreen4_1',text='You will play two different games with these pictures:',alignHoriz='center',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen4_2 = visual.TextStim(win=win,ori=0,name='practiceScreen4_2',text='0-Back and 2-Back',alignHoriz='center',font='Verdana',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen5_1 = visual.TextStim(win=win,ori=0,name='practiceScreen5_1',text='At the begining of 0-Back, you will see a target picture.  Then,',alignHoriz='center',font='Verdana',pos=np.array([0,8])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1)
    practiceScreen5_2 = visual.TextStim(win=win,ori=0,name='practiceScreen5_2',text='pictures will appear one at a time.  Decide if each picture',alignHoriz='center',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1)
    practiceScreen5_3 = visual.TextStim(win=win,ori=0,name='practiceScreen5_3',text='matches the target. For example, if you see:',alignHoriz='center',font='Verdana',pos=np.array([0,6])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1)
    practiceScreen5_4 = visual.TextStim(win=win,ori=0,name='practiceScreen5_4',text='Press MATCH with your POINTER finger',alignHoriz='center',font='Verdana',pos=np.array([0,-7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen5_5 = visual.TextStim(win=win,ori=0,name='practiceScreen5_5',text='everytime you see that picture.  Please press it now.',alignHoriz='center',font='Verdana',pos=np.array([0,-8])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen6_1 = visual.TextStim(win=win,ori=0,name='practiceScreen6_1',text='Press NO MATCH with your MIDDLE finger for',alignHoriz='center',font='Verdana',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen6_2 = visual.TextStim(win=win,ori=0,name='practiceScreen6_2',text='every picture that is different from the target.',alignHoriz='center',font='Verdana',pos=np.array([0,1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen6_3 = visual.TextStim(win=win,ori=0,name='practiceScreen6_3',text='Please press it now.',alignHoriz='center',font='Verdana',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen7 = visual.TextStim(win=win,ori=0,name='practiceScreen7',text="Let's practice now!",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen8 = visual.TextStim(win=win,ori=0,name='practiceScreen8',text="Please wait for experimenter.",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen9 = visual.TextStim(win=win,ori=0,name='practiceScreen9',text='Press Space to continue.',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)

    practiceScreen10_1 = visual.TextStim(win=win,ori=0,name='practiceScreen10_1',text='For 2-Back, you will see pictures',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen10_2 = visual.TextStim(win=win,ori=0,name='practiceScreen10_2',text='one at a time on the screen.',font='Verdana',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen10_3 = visual.TextStim(win=win,ori=0,name='practiceScreen10_3',text='For each picture decide if it is the same as the one two pictures back.',font='Verdana',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen11_1 = visual.TextStim(win=win,ori=0,name='practiceScreen11_1',text='If it is the same, press MATCH with your POINTER finger.\n',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen11_2 = visual.TextStim(win=win,ori=0,name='practiceScreen11_2',text='Otherwise press NO MATCH with your MIDDLE finger.',font='Verdana',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen11_3 = visual.TextStim(win=win,ori=0,name='practiceScreen11_3',text='Here is an example:',font='Verdana',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen12 = visual.TextStim(win=win,ori=0,name='practiceScreen12',text='This is a NO MATCH because nothing was shown two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    PracticeFO1 = nbackStim(expInfo['StimuliDir']+'PracticeFO1.bmp') 
    practiceScreen13 = visual.TextStim(win=win,ori=0,name='practiceScreen13',text='Again, this is a NO MATCH because nothing was shown two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    PracticeFO2 = nbackStim(expInfo['StimuliDir']+'PracticeFO2.bmp') 
    practiceScreen14 = visual.TextStim(win=win,ori=0,name='practiceScreen14',text='This is a MATCH because it is the same as the picture shown two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen15 = visual.TextStim(win=win,ori=0,name='practiceScreen15',text='This is a NO MATCH because it is a different picture was shown two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    PracticeFO3 = nbackStim(expInfo['StimuliDir']+'PracticeFO3.bmp') 
    practiceScreen16 = visual.TextStim(win=win,ori=0,name='practiceScreen16',text='Let\'s try one together!',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)

    practiceScreen17 = visual.TextStim(win=win,ori=0,name='practiceScreen17',text='MATCH or NO MATCH?',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen18 = visual.TextStim(win=win,ori=0,name='practiceScreen18',text='This is a NO MATCH because nothing was shown two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen19 = visual.TextStim(win=win,ori=0,name='practiceScreen19',text='Again, this is a NO MATCH because nothing was shown two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen20 = visual.TextStim(win=win,ori=0,name='practiceScreen20',text='This is a NO MATCH because this picture is different from the one that was presented two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen21 = visual.TextStim(win=win,ori=0,name='practiceScreen21',text='Remember a match is only when the same picture was presented two back.',font='Verdana',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen22_1 = visual.TextStim(win=win,ori=0,name='practiceScreen22_1',text='In the game you will see pictures one at a time.',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen22_2 = visual.TextStim(win=win,ori=0,name='practiceScreen22_2',text='You need to remember what was shown two back.',font='Verdana',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen23 = visual.TextStim(win=win,ori=0,name='practiceScreen23',text='Let\'s practice!',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen24_1 = visual.TextStim(win=win,ori=0,name='practiceScreen24_1',text='Now let\'s practice switching between the two games.',font='Verdana',pos=np.array([0,1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen24_2 = visual.TextStim(win=win,ori=0,name='practiceScreen24_2',text='The plus sign will turn purple before the games switch.',font='Verdana',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen24_3 = visual.TextStim(win=win,ori=0,name='practiceScreen24_3',text='Make sure you pay attention to see if the game is the 0-back or 2-back!',font='Verdana',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen25_1 = visual.TextStim(win=win,ori=0,name='practiceScreen25_1',text='All Done!',font='Verdana',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen25_2 = visual.TextStim(win=win,ori=0,name='practiceScreen25_2',text='Please tell the experimenter you are finished.',font='Verdana',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    practiceScreen25_3 = visual.TextStim(win=win,ori=0,name='practiceScreen25_3',text='Press the SPACEBAR to exit',font='Verdana',pos=np.array([0,-3])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)

    # Create the number of screens to present to the participant for the practices
    screen1 = [practiceScreen1_1,practiceScreen1_2]
    screen4 = [practiceScreen4_1,practiceScreen4_2]
    screen5 = [practiceScreen5_1,practiceScreen5_2,practiceScreen5_3,practiceScreen5_4,practiceScreen5_5]
    screen6 = [practiceScreen6_1,practiceScreen6_2,practiceScreen6_3]
    screen10 = [practiceScreen10_1,practiceScreen10_2]
    screen11 = [practiceScreen11_1,practiceScreen11_2,practiceScreen11_3]
    screen22 = [practiceScreen22_1,practiceScreen22_2]
    screen24 = [practiceScreen24_1,practiceScreen24_2,practiceScreen24_3]
    screen25 = [practiceScreen25_1,practiceScreen25_2,practiceScreen25_3]

    # Initialize various stimuli 
    target = visual.TextStim(win=win,ori=0,name='target',text="Target = ",font='Verdana',pos=np.array([-5,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)
    twoBack = visual.TextStim(win=win,ori=0,name='2Back',text='2-Back',font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)
    correct = visual.TextStim(win=win,ori=0,name='correct',text="Correct!",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='#00FF00',colorSpace='rgb',opacity=1,depth=1.0)
    incorrect = visual.TextStim(win=win,ori=0,name='incorrect',text="Incorrect!",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='#FF0000',colorSpace='rgb',opacity=1,depth=1.0)
    tooslow = visual.TextStim(win=win,ori=0,name='tooslow',text="Too Slow!",font='Verdana',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='#FFFF00',colorSpace='rgb',opacity=1,depth=1.0)

    # Start the clocks
    globalClock.reset()
    routineTimer.reset()

    #------Prepare to start Routine "intro"-------
    t = 0
    introClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat

    introResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
    introResp.status = NOT_STARTED

    # keep track of which components have finished
    introComponents = []
    introComponents.append(introTitle)
    introComponents.append(introResp)

    for thisComponent in introComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "intro"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = introClock.getTime()
        #frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        frameN+=1

        # Presents Name of the task
        if t >= 0.0 and introTitle.status == NOT_STARTED:
            # keep track of start time/frame for later
            introTitle.tStart = t  # underestimates by a little under one frame
            introTitle.frameNStart = frameN  # exact frame index
            introTitle.setAutoDraw(True)

        # *introResp* updates
        if t >= 0.0 and introResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            introResp.tStart = t  # underestimates by a little under one frame
            introResp.frameNStart = frameN  # exact frame index
            introResp.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if introResp.status == STARTED:
            theseKeys = event.getKeys(keyList=hand['Next']+hand['Quit'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
                exitProtocol()
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False 

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in introComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "intro"-------
    for thisComponent in introComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #-------Instructions Loop------
    #instructionsComponent = [practiceScreen1,practiceScreen2,practiceScreen3,practiceScreen4,practiceScreen51,
    #    practiceScreen6,practiceScreen7]
    instructionsComponent = [screen1,practiceScreen2,practiceScreen3, screen4,screen5, screen6, practiceScreen7]

    # Reset the the clock before presenting instructions
    instructionsClock.reset()

    # Iterate through the instruction presentation
    nextScreen = True
    for i in instructionsComponent:
        t = instructionsClock.getTime()
        frameN += 1

        if t >= 0.0:
            if isinstance(i,list):
                for element in i:
                    element.tStart = t
                    element.frameNStart = frameN
                    element.draw()

                    # Present stimuli with practice screen
                    if element.name is 'practiceScreen2':
                        PracticeNC1.stim.draw()

                    if element.name is 'practiceScreen3':
                        Place1.stim.draw()

                    if element.name is 'practiceScreen5_3':
                        target.draw()
                        PracticeNC1.stim.pos += (3,0)
                        PracticeNC1.stim.draw()
                i = element
            else:
                i.tStart = t  # underestimates by a little under one frame
                i.frameNStart = frameN  # exact frame index
                i.draw()

                # Present
                if i.name is 'practiceScreen2':
                    PracticeNC1.stim.draw()

                if i.name is 'practiceScreen3':
                    Place1.stim.draw()

                if i.name is 'practiceScreen5_3':
                    target.draw()
                    PracticeNC1.stim.pos += (3,0)
                    PracticeNC1.stim.draw()
                    practiceScreen52.draw()

        # Present Stimuli
        win.flip()

        # Button press unique for certain instruction screens
        if i.name is 'practiceScreen5_5':
            keypress = event.waitKeys(keyList=hand['Quit']+hand['Match'])
        elif i.name is 'practiceScreen6_3':
            keypress = event.waitKeys(keyList=hand['Quit']+hand['NoMatch'])
        else:
            keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])

        # Add instructions and timestamps for each instruction slide.
        thisExp.addData('experimentTime',instructionsClock.getTime())

        # Save data and escape the program if the escape key is pressed
        if 'escape' in keypress:
            exitProtocol()

    # Present practice Block for the 0Back Faces
    #nBackBlock('Sets/Practice/0Back_Faces.csv','Faces0Back')
    testingBlock = ['0Back_Faces.csv','Faces0Back']
    nBackBlock(os.path.join('Sets','Practice',testingBlock[0]),testingBlock[1])

    # Present break to transition to 0Back Places
    practiceScreen8.draw()
    win.flip()

    # Wait until keypress to move on or exit.
    keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])

    # Safely exit and save practice data if exiting experiment early.
    if 'escape' in keypress:
        exitProtocol()

    # Present practice Block for 0Back Place
    testingBlock = ['0Back_Places.csv','Places0Back']
    nBackBlock(os.path.join('Sets','Practice',testingBlock[0]),testingBlock[1])

    # Start 2Back Task
    instructionsComponent = [screen10,screen11,practiceScreen12,practiceScreen13,practiceScreen14,practiceScreen15,
        practiceScreen16,practiceScreen17,practiceScreen18,practiceScreen17,practiceScreen19,practiceScreen17,practiceScreen20,practiceScreen21]

    exampleCounter = 1
    for i in instructionsComponent:
        t = instructionsClock.getTime()

        if t >= 0.0: #and i.status == NOT_STARTED:
            if isinstance(i,list):
                for element in i:
                    element.tStart = t
                    element.frameNStart = frameN
                    element.draw()
                i = element
            else:
                i.tStart = t
                i.frameNStart = frameN
                i.draw()

            # Present additional stimuli for instructions pages
            if i.name in ['practiceScreen10_2','practiceScreen11_3','practiceScreen12','practiceScreen13','practiceScreen14','practiceScreen15','practiceScreen16']:
                if i.name is 'practiceScreen12':
                    PracticeFO1.stim.draw()

                    # Provide instruction for how to respond
                    if expInfo['Handedness'] == 'Right':
                        PracticeFO1.middleLabelPrompt.color, PracticeFO1.middleFingerPrompt.color = ['#00FF00']*2
                    elif expInfo['Handedness'] == 'Left':
                        PracticeFO1.pointerLabelPrompt.color, PracticeFO1.pointerFingerPrompt.color = ['#00FF00']*2

                    # Draw the prompts on the screen, change the color back to black after drawing
                    PracticeFO1.pointerFingerPrompt.draw()
                    PracticeFO1.middleFingerPrompt.draw()
                    PracticeFO1.pointerLabelPrompt.draw()
                    PracticeFO1.middleLabelPrompt.draw()
                    PracticeFO1.middleLabelPrompt.color, PracticeFO1.middleFingerPrompt.color, PracticeFO1.pointerLabelPrompt.color, PracticeFO1.pointerFingerPrompt.color = ['black']*4

                elif i.name is 'practiceScreen13':
                    # Reformat previous practice images
                    PracticeFO1.stim.size = np.array([5,5])*stimScale
                    PracticeFO1.stim.pos -= np.array([8,0])*stimScale

                    # Provide instruction for how to respond
                    if expInfo['Handedness'] == 'Right':
                        PracticeFO2.middleLabelPrompt.color, PracticeFO2.middleFingerPrompt.color = ['#00FF00']*2
                    elif expInfo['Handedness'] == 'Left':
                        PracticeFO2.pointerLabelPrompt.color, PracticeFO2.pointerFingerPrompt.color = ['#00FF00']*2

                    # Draw the prompts on the screen, change the color back to black after drawing
                    PracticeFO2.pointerFingerPrompt.draw()
                    PracticeFO2.middleFingerPrompt.draw()
                    PracticeFO2.pointerLabelPrompt.draw()
                    PracticeFO2.middleLabelPrompt.draw()
                    PracticeFO2.middleLabelPrompt.color, PracticeFO2.middleFingerPrompt.color, PracticeFO2.pointerLabelPrompt.color, PracticeFO2.pointerFingerPrompt.color = ['black']*4

                    # Draw image stimuli
                    PracticeFO2.stim.draw()
                    PracticeFO1.stim.draw()
                elif i.name is 'practiceScreen14':
                    # Reformat previous practice images
                    PracticeFO1.stim.pos -= np.array([6,0])*stimScale
                    PracticeFO2.stim.pos -= np.array([8,0])*stimScale
                    PracticeFO2.stim.size = np.array([5,5])*stimScale

                    # Provide instruction for how to respond
                    if expInfo['Handedness'] == 'Left':
                        PracticeFO1.middleLabelPrompt.color, PracticeFO1.middleFingerPrompt.color = ['#00FF00']*2
                    elif expInfo['Handedness'] == 'Right':
                        PracticeFO1.pointerLabelPrompt.color, PracticeFO1.pointerFingerPrompt.color = ['#00FF00']*2

                    # Draw the prompts on the screen, change the color back to black after drawing
                    PracticeFO1.pointerFingerPrompt.draw()
                    PracticeFO1.middleFingerPrompt.draw()
                    PracticeFO1.pointerLabelPrompt.draw()
                    PracticeFO1.middleLabelPrompt.draw()
                    PracticeFO1.middleLabelPrompt.color, PracticeFO1.middleFingerPrompt.color, PracticeFO1.pointerLabelPrompt.color, PracticeFO1.pointerFingerPrompt.color = ['black']*4

                    # Draw the image stimuli
                    PracticeFO1.stim.draw()
                    PracticeFO2.stim.draw()

                    # Redraw the 2-Back Stimuli
                    PracticeFO1.stim.pos = np.array([0,0])*stimScale
                    PracticeFO1.stim.size = np.array([10,10])*stimScale
                    PracticeFO1.stim.draw()
                elif i.name is 'practiceScreen15':
                    # Reformat previous paractice images
                    PracticeFO2.stim.pos -= np.array([6,0])*stimScale
                    PracticeFO1.stim.size = np.array([5,5])*stimScale
                    PracticeFO1.stim.pos -= np.array([8,0])*stimScale

                    # Provide instruction for how to respond
                    if expInfo['Handedness'] == 'Left':
                        PracticeFO3.pointerLabelPrompt.color, PracticeFO3.pointerFingerPrompt.color = ['#00FF00']*2
                    elif expInfo['Handedness'] == 'Right':
                        PracticeFO3.middleLabelPrompt.color, PracticeFO3.middleFingerPrompt.color = ['#00FF00']*2

                    # Draw the prompts on the screen, change the color back to black after drawing
                    PracticeFO3.pointerFingerPrompt.draw()
                    PracticeFO3.middleFingerPrompt.draw()
                    PracticeFO3.pointerLabelPrompt.draw()
                    PracticeFO3.middleLabelPrompt.draw()
                    PracticeFO3.middleLabelPrompt.color, PracticeFO3.middleFingerPrompt.color, PracticeFO3.pointerLabelPrompt.color, PracticeFO3.pointerFingerPrompt.color = ['black']*4

                    # Draw the image stimuli
                    PracticeFO1.stim.draw()
                    PracticeFO2.stim.draw()
                    PracticeFO3.stim.draw()

                    # Redraw the 2-Back Stimuli
                    PracticeFO1.stim.pos, PracticeFO2.stim.pos = [(0,0),(0,0)]
                    PracticeFO1.stim.size, PracticeFO2.stim.size = np.array([(10,10),(10,10)])*stimScale

                # Present instructions screen
                win.flip()

                # Button press unique for certain instruction screens
                keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])

                # Exit the practice if the escape key is pressed
                if 'escape' in keypress:
                    exitProtocol()
            else:
                # Assisted Practice for 2Back

                # Display screen for participant response "Match or No Match"
                if i.name is 'practiceScreen17':

                    # Change the examples presented to the participant each time the "Match or No Match" screen is presented
                    if exampleCounter == 1:

                        # Draw the practice stimuli and the prompts
                        x = PracticeFO2 # Place stimuli into holding variable.  Makes subsequent code a bit easier
                        x.stim.draw()
                        x.pointerFingerPrompt.draw()
                        x.middleFingerPrompt.draw()
                        x.pointerLabelPrompt.draw()
                        x.middleLabelPrompt.draw()
                        exampleCounter += 1

                    elif exampleCounter == 2:
                        # Resize Previous stimuli to help learn the 2Back game.
                        PracticeFO2.stim.size = np.array([5,5])*stimScale
                        PracticeFO2.stim.pos -= np.array([8,0])*stimScale

                        # Draw the practice stimuli and the prompts
                        x = PracticeFO3
                        x.stim.draw()
                        x.pointerFingerPrompt.draw()
                        x.middleFingerPrompt.draw()
                        x.pointerLabelPrompt.draw()
                        x.middleLabelPrompt.draw()
                        exampleCounter += 1

                    elif exampleCounter == 3:
                        # Resize Previous stimuli to help learn the 2Back game.
                        PracticeFO2.stim.pos -= np.array([6,0])*stimScale
                        PracticeFO3.stim.size = np.array([5,5])*stimScale
                        PracticeFO3.stim.pos -= np.array([8,0])*stimScale

                        # Draw the practice stimuli and the prompts
                        x = PracticeFO1
                        x.stim.draw()
                        x.pointerFingerPrompt.draw()
                        x.middleFingerPrompt.draw()
                        x.pointerLabelPrompt.draw()
                        x.middleLabelPrompt.draw()
                        exampleCounter += 1

                elif i.name in ['practiceScreen18','practiceScreen19','practiceScreen20']:
                    if expInfo['Handedness'] == 'Right':
                        x.middleLabelPrompt.color, x.middleFingerPrompt.color = ['#00FF00'] * 2

                    elif expInfo['Handedness'] == 'Left':
                        x.pointerLabelPrompt.color, x.pointerFingerPrompt.color = ['#00FF00'] * 2

                    # Draw image stimuli
                    x.stim.draw()
                    x.pointerFingerPrompt.draw()
                    x.middleFingerPrompt.draw()
                    x.pointerLabelPrompt.draw()
                    x.middleLabelPrompt.draw()

                    # Draw the previous images presented to assist learning 2Back game.
                    if (exampleCounter-1) == 2:
                        PracticeFO2.stim.draw()
                    elif (exampleCounter-1) == 3:
                        PracticeFO2.stim.draw()
                        PracticeFO3.stim.draw()
                    x.pointerFingerPrompt.color, x.middleFingerPrompt.color, x.pointerLabelPrompt.color, x.middleLabelPrompt.color = ['black']*4
                elif i.name is 'practiceScreen21':

                    # Reformat stim to help with learning the 2Back game
                    PracticeFO3.stim.pos -= np.array([6,0])*stimScale
                    PracticeFO1.stim.size = np.array([5,5])*stimScale
                    PracticeFO1.stim.pos -= np.array([8,0])*stimScale

                    # Draw Stim
                    PracticeFO1.stim.draw()
                    PracticeFO3.stim.draw()

                    # Reformat and present a match Stim
                    PracticeFO3.stim.size = np.array([10,10])*stimScale
                    PracticeFO3.stim.pos = np.array([0,0])*stimScale
                    PracticeFO3.middleLabelPrompt.color, PracticeFO3.middleFingerPrompt.color, PracticeFO3.pointerLabelPrompt.color, PracticeFO3.pointerFingerPrompt.color = ['black','black','black','black']

                    # Mark the Match Button based if the participant is left or right handed
                    if expInfo['Handedness'] == 'Right':
                        PracticeFO3.pointerLabelPrompt.color, PracticeFO3.pointerFingerPrompt.color = ['#00FF00','#00FF00']
                    elif expInfo['Handedness'] == 'Left':
                        PracticeFO3.middleLabelPrompt.color, PracticeFO3.middleFingerPrompt.color = ['#00FF00','#00FF00']

                    PracticeFO3.stim.draw()
                    PracticeFO3.middleLabelPrompt.draw()
                    PracticeFO3.middleFingerPrompt.draw()
                    PracticeFO3.pointerLabelPrompt.draw()
                    PracticeFO3.pointerFingerPrompt.draw()
                    x.pointerFingerPrompt.color, x.middleFingerPrompt.color, x.pointerLabelPrompt.color, x.middleLabelPrompt.color = ['black']*4

                # Present instructions screen
                win.flip()

                # Button press unique for certain instruction screens
                if i.name is 'practiceScreen17':
                    keypress = event.waitKeys(keyList=hand['Quit']+hand['Match']+hand['NoMatch'])
                else:
                    keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])

                if 'escape' in keypress:
                    exitProtocol()

    # Present the instruction screen before the 2Back Trials
    practiceScreen22_1.draw()
    practiceScreen22_2.draw()
    win.flip()
    keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])

    # Quit the task if the escape key is pressed
    if 'escape' in keypress:
        exitProtocol()

    # Present 2Back Faces Trials
    #nBackBlock('Sets/Practice/2Back_Faces.csv','Faces2Back')
    testingBlock = ['2Back_Faces.csv','Faces2Back']
    nBackBlock(os.path.join('Sets','Practice',testingBlock[0]),testingBlock[1])

    # Present break to transitiokn to 2Back Places
    practiceScreen8.draw()
    win.flip()

    # Wait until keypress to move on or exit
    keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])

    # Safely exit and save practice data if exiting experiment early.
    if 'escape' in keypress:
        exitProtocol()

    # Present 2Back Places Trials
    #nBackBlock('Sets/Practice/2Back_Places.csv','Places2Back')
    testingBlock = ['2Back_Places.csv','Places2Back']
    nBackBlock(os.path.join('Sets','Practice',testingBlock[0]),testingBlock[1])

    # Present last instructions screen before final practice
    practiceScreen24_1.draw()
    practiceScreen24_2.draw()
    practiceScreen24_3.draw()
    win.flip()
    keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])

    # Present Final Practice Trials
    #nBackBlock('Sets/Practice/Final_Practice_Set.csv','FinalPractice')
    testingBlock = ['Final_Practice_Set.csv','FinalPractice']
    nBackBlock(os.path.join('Sets','Practice',testingBlock[0]),testingBlock[1])

    # Present final instructions screen and wait for experimenter to press the spacebar
    practiceScreen25_1.draw()
    practiceScreen25_3.draw()
    practiceScreen25_3.draw()
    win.flip()
    keypress = event.waitKeys(keyList=hand['Next'])

elif expInfo['Session'] == 'Behavioral' or expInfo['Session'] == 'MRI':

    # Creates the instructions screens for the tasks
    taskScreen1_1 = visual.TextStim(win=win,ori=0,name='taskScreen1_1',text='There are two games in this part of the study.',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen1_2 = visual.TextStim(win=win,ori=0,name='taskScreen1_2',text='They are "0-Back" and "2-Back".',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen1_3 = visual.TextStim(win=win,ori=0,name='taskScreen1_3',text='You will see the words "Target" or "2-Back" before each game starts.',font='Arial',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)

    taskScreen2_1 = visual.TextStim(win=win,ori=0,name='taskScreen2_1',text='For "0-Back", press MATCH if you see a picture that is the same as the target picture.',font='Arial',pos=np.array([0,8])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen2_2 = visual.TextStim(win=win,ori=0,name='taskScreen2_2',text='Press NO MATCH if it is not the same.',font='Arial',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen3_1 = visual.TextStim(win=win,ori=0,name='taskScreen3_1',text='For "2-Back", press MATCH if the picture you see is the same as two pictures back.',font='Arial',pos=np.array([0,8])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen3_2 = visual.TextStim(win=win,ori=0,name='taskScreen3_2',text='Press NO MATCH if not.',font='Arial',pos=np.array([0,7])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen5_1 = visual.TextStim(win=win,ori=0,name='taskScreen5_1',text='Pay close attention when the plus sign turns purple',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen5_2 = visual.TextStim(win=win,ori=0,name='taskScreen5_2',text='to see what game you are playing!',font='Arial',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen6_1 = visual.TextStim(win=win,ori=0,name='taskScreen6_1',text='Great Job!',font='Arial',pos=np.array([0,3])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen6_2 = visual.TextStim(win=win,ori=0,name='taskScreen6_2',text='Again, the games will switch.',font='Arial',pos=np.array([0,1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen6_3 = visual.TextStim(win=win,ori=0,name='taskScreen6_3',text='Pay close attention when the plus sign turns purple',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    taskScreen6_4 = visual.TextStim(win=win,ori=0,name='taskScreen6_4',text='to see what game you are playing!',font='Arial',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)

    # Group screens together by text stimuli presented on each screen
    screen1 = [taskScreen1_1,taskScreen1_2,taskScreen1_3]
    screen2 = [taskScreen2_1,taskScreen2_2]
    screen3 = [taskScreen3_1,taskScreen3_2]
    screen5 = [taskScreen5_1,taskScreen5_2]
    screen6 = [taskScreen6_1,taskScreen6_2,taskScreen6_3,taskScreen6_4]

    # Change instructions for Behavioral tasks to be different from MRI
    if expInfo['Session'] == 'Behavioral':
        taskScreen4_1 = visual.TextStim(win=win,ori=0,name='taskScreen4_1',text='Please respond while the picture is on the screen.',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen4_2 = visual.TextStim(win=win,ori=0,name='taskScreen4_2',text='Press your POINTER finger for MATCH.',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen4_3 = visual.TextStim(win=win,ori=0,name='taskScreen4_3',text='Press your MIDDLE finger for NO MATCH.',font='Arial',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen7_1 = visual.TextStim(win=win,ori=0,name='taskScreen7_1',text='Please respond while the picture is on the screen.',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen7_2 = visual.TextStim(win=win,ori=0,name='taskScreen7_2',text='Press your POINTER finger for match.',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen7_3 = visual.TextStim(win=win,ori=0,name='taskScreen7_3',text='Press your MIDDLE finger for NO MATCH.',font='Arial',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        waitingScreen = visual.TextStim(win=win,ori=0,name='waitingScreen',text='Waiting for experimenter...',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        waitingScreen2 = visual.TextStim(win=win,ori=0,name='waitingScreen2',text='Waiting for experimenter...',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        screen4 = [taskScreen4_1,taskScreen4_2,taskScreen4_3]
        screen7 = [taskScreen7_1,taskScreen7_2,taskScreen7_3]
    elif expInfo['Session'] == 'MRI':
        taskScreen4_1 = visual.TextStim(win=win,ori=0,name='taskScreen4_1',text='Please respond while the picture is on the screen.',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen4_2 = visual.TextStim(win=win,ori=0,name='taskScreen4_2',text='Press your POINTER finger for MATCH.',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen4_3 = visual.TextStim(win=win,ori=0,name='taskScreen4_3',text='Press your MIDDLE finger for NO MATCH.',font='Arial',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen4_4 = visual.TextStim(win=win,ori=0,name='taskScreen4_4',text='PLEASE REMEMBER TO KEEP YOUR HEAD STILL',font='Arial',pos=np.array([0,-3])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen7_1 = visual.TextStim(win=win,ori=0,name='taskScreen7_1',text='Please respond while the picture is on the screen.',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen7_2 = visual.TextStim(win=win,ori=0,name='taskScreen7_2',text='Press your POINTER finger for match.',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen7_3 = visual.TextStim(win=win,ori=0,name='taskScreen7_3',text='Press your MIDDLE finger for NO MATCH.',font='Arial',pos=np.array([0,-1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        taskScreen7_4 = visual.TextStim(win=win,ori=0,name='taskScreen7_4',text='PLEASE REMEMBER TO KEEP YOUR HEAD STILL',font='Arial',pos=np.array([0,-3])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        waitingScreen = visual.TextStim(win=win,ori=0,name='waitingScreen',text='Waiting for trigger...',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        waitingScreen2 = visual.TextStim(win=win,ori=0,name='waitingScreen2',text='Waiting for trigger...',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
        screen4 = [taskScreen4_1,taskScreen4_2,taskScreen4_3,taskScreen4_4]
        screen7 = [taskScreen7_1,taskScreen7_2,taskScreen7_3,taskScreen7_4]

    # Group all instructions together for all screens
    instructions = [screen1,screen2,screen3,screen4,screen5,screen6,screen7]
    run1Index = 5 # Index the instructions screen for the first run

    # Create instructions stimuli
    target = visual.TextStim(win=win,ori=0,name='target',text="Target = ",font='Arial',pos=np.array([-5,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=1.0)
    practiceFO1 = nbackStim(expInfo['StimuliDir']+'PracticeFO1.bmp')
    practiceFO3 = nbackStim(expInfo['StimuliDir']+'PracticeFO3.bmp') 

    # Create some handy timers
    instructionsClock.reset
    globalClock.reset()
    routineTimer.reset()

    #------Prepare to start Routine "intro"-------
    t = 0
    introClock.reset()  # clock 
    frameN = -1
    
    # update component parameters for each repeat
    introResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
    introResp.status = NOT_STARTED

    # keep track of which components have finished
    introComponents = []
    introComponents.append(introTitle)
    introComponents.append(introResp)

    for thisComponent in introComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "intro"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = introClock.getTime()
        frameN+=1

        # Presents Name of the task
        if t >= 0.0 and introTitle.status == NOT_STARTED:
            # keep track of start time/frame for later
            introTitle.tStart = t  # underestimates by a little under one frame
            introTitle.frameNStart = frameN  # exact frame index
            introTitle.setAutoDraw(True)

        # *introResp* updates
        if t >= 0.0 and introResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            introResp.tStart = t  # underestimates by a little under one frame
            introResp.frameNStart = frameN  # exact frame index
            introResp.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if introResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False 

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in introComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "intro"-------
    for thisComponent in introComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    # Present instructions for the task
    if expInfo['Session'] == 'MRI':
        hand['Trigger'] = config['trigger']

    elif expInfo['Session'] == 'Behavioral':
        hand['Trigger'] = config['keys']['Next']

    for i,j in enumerate(instructions):
        if not isinstance(j,list):
            print i, j.name

    # Record trigger code in output file
    expInfo['triggercode'] = hand['Trigger']

    # Allows you to skip to the second run of the task
    if expInfo['Run'] == 'All':
        run = [1,2]
    else:
        run = [2]

    # Iterate through the number of runs experimenter selected
    for j in run:

        # Determine the instruction slides to present by the number of runs experimenter selected
        if j == 1:
            instructionSlides = instructions[0:run1Index]
        else:
            instructionSlides = instructions[run1Index:]

        # Iterate through list of instructions slides
        for i in instructionSlides:
            t = instructionsClock.getTime()

            # Present instructions
            if not isinstance(i,list): # If element is not a list of more instructions
                i.tStart = t
                i.frameNStart = frameN
                i.draw()

            else: # There is a list that contains all elements for the screen
                for element in i:
                    # Create instructions on the screen
                    element.tStart = t
                    element.frameNStart = frameN
                    element.draw()

                    # Format images on the screen for the instructions
                    if element.name == 'taskScreen2_2':
                        practiceFO3.stim.pos = np.array([3,0])*stimScale
                        practiceFO3.stim.draw()
                        target.draw()
                    elif element.name == 'taskScreen3_2':
                        practiceFO3.stim.pos = np.array([0,0])*stimScale
                        practiceFO3.stim.draw()

                        # Instructions will be slightly different by participant's handedness
                        # edit the colors for the button prompts.
                        if expInfo['Handedness'] == 'right':
                            practiceFO3.pointerFingerPrompt.color, practiceFO3.pointerLabelPrompt.color = ('#00FF00','#00FF00')
                        elif expInfo['Handedness'] == 'left':
                            practiceFO3.middleFingerPrompt.color, practiceFO3.middleLabelPrompt.color = ('#00FF00','#00FF00')

                        # Draw all stimuli prompts presented
                        practiceFO3.middleFingerPrompt.draw()
                        practiceFO3.middleLabelPrompt.draw()
                        practiceFO3.pointerFingerPrompt.draw()
                        practiceFO3.pointerLabelPrompt.draw()

                        # Reformat the images and draw them for the example
                        practiceFO1.stim.size = np.array([5,5])*stimScale
                        practiceFO3.stim.size = np.array([5,5])*stimScale
                        practiceFO1.stim.pos -= np.array([8,0])*stimScale
                        practiceFO3.stim.pos -= np.array([14,0])*stimScale
                        practiceFO1.stim.draw()
                        practiceFO3.stim.draw()

            # Present the screen and wait for a keypress or trigger
            win.flip()

            # Present the instructions and wait for button press to continue or escape the game.
            if element.name == 'waitingScreen':
                trigger = hand['Trigger']
            else:
                trigger = hand['Next']

            # Wait for keypress or trigger.  If escape was pressed, exit the task
            keypress = event.waitKeys(keyList=hand['Quit']+trigger)
            if 'escape' in keypress:
                exitProtocol()

        #launchScan(win,{'TR':0.8,'volumes':370, 'sync':'5','skip':10,'sound':True},globalClock=globalClock,
        #    simResponses = x, mode='Test',wait_msg='waiting for scanner...', wait_timeout=120)
        nBackBlock(os.path.join('Sets','Task','Version%d_%d.csv' % (expInfo['Version'],j)),'nBack')
        

elif expInfo['Session'] == 'RecMem':
    # Create instructions stim to iterate through
    recScreen1_1 = visual.TextStim(win=win,ori=0,name='recScreen1_1',text='Now, we will test your memory for some of the',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen1_2 = visual.TextStim(win=win,ori=0,name='recScreen1_2',text='faces and places you saw during the 0-Back and 2-back games.',font='Arial',pos=np.array([0,1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen1_3 = visual.TextStim(win=win,ori=0,name='recScreen1_3',text='Press SPACE to continue',font='Arial',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen2_1 = visual.TextStim(win=win,ori=0,name='recScreen2_1',text='Pictures will appear one at a time on the screen.',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen2_2 = visual.TextStim(win=win,ori=0,name='recScreen2_2',text='For each picture, decide whether you saw it before or if it is new.',font='Arial',pos=np.array([0,1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen2_3 = visual.TextStim(win=win,ori=0,name='recScreen2_3',text='Press SPACE to continue',font='Arial',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen3_1 = visual.TextStim(win=win,ori=0,name='recScreen3_1',text='Press OLD under your POINTER finger if you think you have seen the picture before.',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen3_2 = visual.TextStim(win=win,ori=0,name='recScreen3_2',text='Press NEW under your MIDDLE finger if you think this is the first',font='Arial',pos=np.array([0,1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen3_3 = visual.TextStim(win=win,ori=0,name='recScreen3_2',text='time you have seen the picture.',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen3_4 = visual.TextStim(win=win,ori=0,name='recScreen3_3',text='Press SPACE to continue',font='Arial',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen4_1 = visual.TextStim(win=win,ori=0,name='recScreen4_1',text='Let\'s do some practice!',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen4_2 = visual.TextStim(win=win,ori=0,name='recScreen4_2',text='PLEASE RESPOND WHILE THE PICTURE IS ON THE SCREEN',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen4_3 = visual.TextStim(win=win,ori=0,name='recScreen4_3',text='Press SPACE to continue',font='Arial',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen5_1 = visual.TextStim(win=win,ori=0,name='recScreen5_1',text='The feedback you were just given',font='Arial',pos=np.array([0,3])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen5_2 = visual.TextStim(win=win,ori=0,name='recScreen5_2',text='(Correct, Incorrect, Too Slow),',font='Arial',pos=np.array([0,2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen5_3 = visual.TextStim(win=win,ori=0,name='recScreen5_3',text='was meant to help you understand the game.',font='Arial',pos=np.array([0,1])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen5_4 = visual.TextStim(win=win,ori=0,name='recScreen5_4',text='You WILL NOT get feedback in the real game.',font='Arial',pos=np.array([0,0])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen5_5 = visual.TextStim(win=win,ori=0,name='recScreen5_5',text='Press SPACE to continue',font='Arial',pos=np.array([0,-2])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen6_1 = visual.TextStim(win=win,ori=0,name='recScreen6_1',text='Please respond while the picture is on the screen',font='Arial',pos=np.array([0,3])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen6_2 = visual.TextStim(win=win,ori=0,name='recScreen6_2',text='OLD',font='Arial',pos=np.array([-4,0])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen6_3 = visual.TextStim(win=win,ori=0,name='recScreen6_3',text='POINTER',font='Arial',pos=np.array([-4,-1])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen6_4 = visual.TextStim(win=win,ori=0,name='recScreen6_4',text='NEW',font='Arial',pos=np.array([4,0])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen6_5 = visual.TextStim(win=win,ori=0,name='recScreen6_5',text='MIDDLE',font='Arial',pos=np.array([4,-1])*handFlip,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)
    recScreen6_6 = visual.TextStim(win=win,ori=0,name='recScreen6_6',text='Press SPACE to start the game',font='Arial',pos=np.array([0,-6])*stimScale,height=textLetterSize,wrapWidth=wrapWidth,color='black',colorSpace='rgb',opacity=1,depth=-1.0)

    # Create list of all elements that should be presented to the participant on one screen
    screen1 = [recScreen1_1, recScreen1_2, recScreen1_3]
    screen2 = [recScreen2_1, recScreen2_2, recScreen2_3]
    screen3 = [recScreen3_1, recScreen3_2, recScreen3_3, recScreen3_4]
    screen4 = [recScreen4_1, recScreen4_2, recScreen4_3]
    screen5 = [recScreen5_1, recScreen5_2, recScreen5_3, recScreen5_4, recScreen5_5]
    screen6 = [recScreen6_1, recScreen6_2, recScreen6_3, recScreen6_4, recScreen6_5, recScreen6_6]

    # Place all instructions into a list to iterate through
    instructionSlides = [screen1, screen2, screen3, screen4, screen5, screen6]
    practiceIndex = 4

    # Set timers
    recPractice = True
    instructionsClock.reset()
    globalClock.reset()
    routineTimer.reset()

    # Present instructions to participant
    for i in instructionSlides[:practiceIndex]:

        # Determine the number of elements to draw per screen and draw them sequentially
        if not isinstance(i,list):
            i.tStart = globalClock.getTime()
            i.draw()
        else:
            for element in i:
                element.tStart = globalClock.getTime()
                element.draw()

        # Present the element
        win.flip()

        # Wait for keypress or trigger.  If escape was pressed, exit the task
        keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])
        if 'escape' in keypress:
            exitProtocol()

    recPractice = True
    nBackBlock(os.path.join('Sets','RecMem','PracticeSet.csv'),'RecMemPractice')
        
    # Present instructions to participant
    for i in instructionSlides[practiceIndex:]:

        # Determine the number of elements to draw per screen and draw them sequentially
        if not isinstance(i,list):
            i.tStart = globalClock.getTime()
            i.draw()
        else:
            for element in i:
                element.tStart = globalClock.getTime()
                element.draw()

        # Present instruction screen to participant
        win.flip()

        # Wait for keypress or trigger.  If escape was pressed, exit the task
        keypress = event.waitKeys(keyList=hand['Quit']+hand['Next'])
        if 'escape' in keypress:
            exitProtocol()

    # Start RecMem Final task
    recPractice = False
    nBackBlock(os.path.join('Sets','RecMem','Version%d.csv' % expInfo['Version']),'RecMemTask')

# Show "all done" screen
endScreen()

# Save and exit from the experiment
exitProtocol()
