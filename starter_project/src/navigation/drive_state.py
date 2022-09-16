from multiprocessing import context
from state import BaseState
import numpy as np
from context import Context
from drive import get_drive_command

class DriveState(BaseState):
    def __init__(self, context: Context):
        super().__init__(
            context,
            #TODO:
            add_outcomes=["reached_point", "driving_to_point"],
        )

    def evaluate(self, ud):
        print("in drive")
        target = np.array([4.5, 2.5, 0.0])
        #TODO: get the rovers pose, if it doesn't exist stay in DriveState with outcome "driving_to_point"
        rover_pose = self.context.rover.get_pose()
        
        if rover_pose == None:
            return "driving_to_point"
        print(rover_pose.position)
        #TODO: get the drive command (and completion status) based on target and pose (HINT: use get_drive_command())
        drive_command, complete = get_drive_command(target, rover_pose, 1.0, 0.95)
        print(drive_command)
        #TODO: if we are finished getting to the target, return with outcome "reached_point"
        if complete:
            return "reached_point"

        #TODO: send the drive command to the rover
        self.context.rover.send_drive_command(drive_command)

        #TODO: tell smach to stay in the DriveState by returning with outcome "driving_to_point"
        return "driving_to_point"