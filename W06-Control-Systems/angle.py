import math
import lib601.sm as sm
from soar.io import io
import lib601.gfx as gfx
import lib601.util as util
import lib601.sonarDist as sonarDist

######################################################################
#
#            Brain SM
#
######################################################################

desiredRight = 0.4
forwardVelocity = 0.1

# No additional delay.
# Output is a sequence of (distance, angle) pairs
class Sensor(sm.SM):
   def getNextValues(self, state, inp):
       v = sonarDist.getDistanceRightAndAngle(inp.sonars)
       print('Dist from robot center to wall on right', v[0])
       if not v[1]:
           print('******  Angle reading not valid  ******')
       return (state, v)


class WallFollower(sm.SM):
    """
    Implements a state machine whose input is a pair of the perpendic­ular
    distance to the wall on the right and the angle to the wall and whose output
    is an instance of the class io.Action
    """
    startState = None
    def getNextValues(self, state, inp):
        # inp is a tuple (distanceRight, angle)
        error = desiredRight - inp[0]
        if inp[1] == None: 
            output = io.Action(forwardVelocity, rvel = 0)
        output = io.Action(forwardVelocity, rvel = k3 * error - k4 * inp[1])
        return state, output


sensorMachine = Sensor()
sensorMachine.name = 'sensor'
mySM = sm.Cascade(sensorMachine, WallFollower())

######################################################################
#
#            Running the robot
#
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)
    robot.gfx.addStaticPlotSMProbe(y=('rightDistance', 'sensor',
                                      'output', lambda x:x[0]))
    robot.behavior = mySM
    robot.behavior.start(traceTasks = robot.gfx.tasks())

def step():
    robot.behavior.step(io.SensorInput()).execute()