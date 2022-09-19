from state import BaseState
from context import Context
from geometry_msgs.msg import Twist

class TagSeekState(BaseState):
    def __init__(self, context: Context):
        super().__init__(
            context,
            add_outcomes=["success", "failure", "working"],
        )

    def evaluate(self, ud):
        #TODO: get the tag's location and properties
        fid = self.context.env.get_fid_data()
        
        #TODO: if we don't have a tag: go to the Done State (with outcome 'failure')
        if fid is None:
            self.context.rover.send_drive_stop()
            return 'failure'

        #TODO: if we are within angular and distance tolerances: go to Done State (with outcome 'success')
        angular_approx = fid.x
        distance_approx = fid.dist
        print(angular_approx, distance_approx)
        if angular_approx < 20 and distance_approx > 0.008:
            return 'success'
        #TODO: figure out the twist command to be applied to move rover to tag
        command = Twist()
        #TODO: send Twist command to rover
        print(f"distance approx: {distance_approx}, angular: {angular_approx}")
        if angular_approx < 20:
            command.linear.x = 1 - distance_approx
        command.angular.z = -0.005 * angular_approx
        print(f"command lin: {command.linear.x}, command angular: {command.angular.z}")
        self.context.rover.send_drive_command(command)
        #TODO: stay in the TagSeekState (with outcome 'working')
        return 'working'