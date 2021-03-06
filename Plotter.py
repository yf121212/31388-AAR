import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import time

from Robot import Robot

class Plotter():
    ''' Plot the results of a simulation in real time'''
    
    # define a 2x2 grid to hold plots
    fig, ax = plt.subplots(2,2)
    plt.ion()

    # axes for position, speed and angle of robot
    pos_ax = plt.subplot(122)

    speed_ax = plt.subplot(221)
    speed_ax.grid()
    speed_ax.set_xlim([0,50])
    speed_ax.set_ylim([-10,10])
    speed_ax.set_ylabel("Angular Speed (rad/sec)")

    ang_ax = plt.subplot(223)
    ang_ax.set_ylim([0,2*np.pi])
    ang_ax.set_xlabel("Time (s)")
    ang_ax.set_ylabel("Angle (rad)")
    ang_ax.grid()



    def __init__(self):
        self.data = {}

    def add_robot(self, robot):
        '''Add a robot to the plot, creating a Rob_dat instance'''
        self.data[robot.name] = Robot_Data(
            robot.name, robot.color, robot.xi[0],
            robot.xi[1], robot.xi[2], 0)
        

    def update_data(self, name, x, y, theta, time, r_speed, l_speed):
        '''Record the data from the sim in the Robot_data class'''
        # find the correct robot and plot its data
        self.data[name].update( x, y, theta, time, r_speed, l_speed)
        robot_data = self.data[name]

        # reset pos axis to remove the arrows from the previous frames
        robot_data.robot_pos, = self.pos_ax.plot(
            [], [], color = robot_data.color, lw=2)
        # robot_data.robot_star, = self.pos_ax.plot(
        #     [], [], color = robot_data.color + "*")
        Plotter.pos_ax.set_xlim([-1,1])
        Plotter.pos_ax.set_ylim([-1,1])
        Plotter.pos_ax.grid()

        # draw an arrow on the canvas and set the angle to the pose angle
        bbox_props = dict(boxstyle="rarrow,pad=0.3", fc=robot_data.color,
                          ec=robot_data.color, lw=2)

        t = self.pos_ax.text(x, y, name, ha="center", va="center", 
                            rotation=(theta*(180/np.pi)),
                            size=5,
                            bbox=bbox_props)

        # plot the last 100 position points
        robot_data.robot_pos.set_data(
            robot_data.x_pos, 
            robot_data.y_pos)
        robot_data.robot_star.set_data(x, y)

        # pose angle vs time
        if time:
            Plotter.ang_ax.set_xlim([0,time])
            Plotter.speed_ax.set_xlim([0, time])
        
        robot_data.robot_angle.set_data(
            robot_data.sim_time, robot_data.theta_pos)

        # wheel speeds
        robot_data.robot_r_speed.set_data(robot_data.sim_time, 
                                        robot_data.speed_data_r)
        robot_data.robot_l_speed.set_data(robot_data.sim_time, 
                                        robot_data.speed_data_l)

    def update_canvas(self):
        '''Redraw the canvas with updated data'''
        self.fig.canvas.draw()
        plt.show()
        plt.pause(0.05)

class Robot_Data():
    '''Stores data for a specific robot'''

    def __init__(
            self, name, color, x_init, y_init, 
            ang_init, r_speed_init = 0, 
            l_speed_init = 0):

        self.name = name
        self.color = color
        self.speed_data_r = [r_speed_init]
        self.speed_data_l = [l_speed_init]
        self.theta_pos = [ang_init]
        self.x_pos = [x_init]
        self.y_pos = [y_init]

        # create lines for the storage of data to be plotted on the 
        # global axes
        self.robot_pos, = Plotter.pos_ax.plot([], [], color=color, 
                                                    linestyle = "solid", lw=2)
        self.robot_star, = Plotter.pos_ax.plot([], [], 'g*')
        self.robot_angle, = Plotter.ang_ax.plot([], [], color=color, 
                                                    linestyle = "-")
        self.robot_l_speed, = Plotter.speed_ax.plot([], [], color=color, 
                                                        linestyle = "--")
        self.robot_r_speed, = Plotter.speed_ax.plot([], [], color=color, 
                                                        linestyle = "-.")
        self.sim_time = [0]

    def update(self, x , y, theta, time, r_speed, l_speed):
        '''Append new values to the data lists'''
        self.speed_data_r.append(r_speed)
        self.speed_data_l.append(l_speed)
        self.theta_pos.append(theta)
        self.x_pos.append(x)
        self.y_pos.append(y)
        self.sim_time.append(time)

if __name__ == "__main__":
    print("Running Plotter.py")

