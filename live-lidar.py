import matplotlib
from matplotlib import animation
from rplidar import RPLidar as Lidar
from math import cos, sin, radians
import threading
import  matplotlib.pyplot as plt, matplotlib.animation as animation
lidar = Lidar("COM13")

length = 360*2

scan_data = {'x': [0] * length, 'y': [0] * length}

try:
    def fetch_data():
        global scan_data
        global lidar

        for scan in lidar.iter_scans(max_buf_meas=32000):
            for quality, angle, distance in scan:
                radians_angle = radians(angle)
                distance /= 10
                ox = sin(radians_angle) * distance
                oy = cos(radians_angle) * distance

                scan_data['x'].append(ox)
                scan_data['y'].append(oy)

                scan_data['x'], scan_data['y'] = scan_data['x'][-length:], scan_data['y'][-length:]
    t1 = threading.Thread(target=fetch_data)
    t1.start()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['bottom'].set_position('zero')
    def animate(i):
        global scan_data

        ax.clear()
        ax.plot(scan_data['x'], scan_data['y'], 'b.')
    
    anim = animation.FuncAnimation(fig, animate, fargs=(), interval=.1)
    plt.show()
finally:
    lidar.stop()
    lidar.disconnect()
    t1.join()