import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pandas as pd

fig = plt.figure()
chart = fig.add_subplot(1,1,1)
DB = pd.read_csv('005930.csv')

def animate(i):
    frame = 240 + i
    index = DB.index[:frame]
    Value = DB['Adj Close'][:frame]
    #MA30  =  DB['MA30'][:frame]
    MA240 =  DB['MA240'][:frame]
    chart.clear()
    chart.plot(index, Value, 'g')
    #chart.plot(index, MA30, 'r')
    chart.plot(index, MA240, 'b')
    
ani = animation.FuncAnimation(fig, animate, interval = 10)
plt.show()