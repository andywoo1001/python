import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

# This example uses subclassing, but there is no reason that the proper function
# couldn't be set up and then use FuncAnimation. The code is long, but not
# really complex. The length is due solely to the fact that there are a total
# of 9 lines that need to be changed for the animation as well as 3 subplots
# that need initial set up.
class SubplotAnimation(animation.TimedAnimation):
    def __init__(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 4)

        self.t = np.linspace(0, 80, 400)
        self.x = np.cos(2 * np.pi * self.t / 10.)
        self.y = np.sin(2 * np.pi * self.t / 10.)
        self.z = 10 * self.t

        self.line1 = Line2D([], [], color='black')
        ax1.add_line(self.line1)
        ax1.set_xlim(-1, 1)
        ax1.set_ylim(-2, 2)

        self.line2 = Line2D([], [], color='black')
        ax2.add_line(self.line2)
        ax2.set_xlim(-1, 1)
        ax2.set_ylim(0, 800)

        self.line3 = Line2D([], [], color='black')
        ax3.add_line(self.line3)
        ax3.set_xlim(-1, 1)
        ax3.set_ylim(0, 800)

        animation.TimedAnimation.__init__(self, fig, interval=50, blit=True)

    def _draw_frame(self, framedata):
        i = framedata
        head = i - 1
        head_len = 10
        head_slice = (self.t > self.t[i] - 1.0) & (self.t < self.t[i])

        self.line1.set_data(self.x[:i], self.y[:i])

        self.line2.set_data(self.y[:i], self.z[:i])

        self.line3.set_data(self.x[:i], self.z[:i])

        self._drawn_artists = [self.line1, 
            self.line2, 
            self.line3, ]

    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        lines =  [self.line1, 
            self.line2, 
            self.line3, ]
        for l in lines:
            l.set_data([], [])

ani = SubplotAnimation()
#ani.save('test_sub.mp4')
plt.show()
