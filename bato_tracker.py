# import pandas as pd
# import pyqtgraph as pg
# from PyQt5.QtWidgets import QApplication
# from pyqtgraph import AxisItem



# def read_and_prepare_data(csv_file):
#     df = pd.read_csv(csv_file)
#     df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
#     return df

# class TimeAxisItem(AxisItem):
#     def tickStrings(self, values, scale, spacing):
#         return [pd.to_datetime(value).strftime('%S') for value in values]

# app = QApplication([])
# win = pg.GraphicsLayoutWidget(show=True)
# win.setWindowTitle('Real Time Battery Level Plot')

# # Creating custom axis item for formatting x-axis as seconds
# axis = TimeAxisItem(orientation='bottom')

# plot = win.addPlot(title="Battery Level", axisItems={'bottom': axis})
# plot.getAxis('left').setLabel("Battery Level", units='%')
# plot.getAxis('bottom').setLabel("Time", units='s')
# curve = plot.plot(pen='y')

# # Set y-axis range to be from 0 to 100
# plot.setYRange(0, 100, padding=0)

# # Show grid lines on the plot
# plot.showGrid(x=True, y=True, alpha=0.3)

# def update():
#     df = read_and_prepare_data('data.csv')
#     curve.setData(df['Timestamp'], df['Level'])

# timer = pg.QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(1000)  # Update every 1000 milliseconds (1 second)

# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(pg.QtCore, 'PYQT_VERSION'):
#         QApplication.instance().exec_()

import pandas as pd
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from pyqtgraph import AxisItem

def read_and_prepare_data(csv_file):
    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
    return df

class TimeAxisItem(AxisItem):
    def tickStrings(self, values, scale, spacing):
        # Format the tick labels as day of the month, hour, and minute
        return [pd.to_datetime(value).strftime('%d, %H:%M') for value in values]

app = QApplication([])
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Real Time Battery Level Plot')

# Creating custom axis item for formatting x-axis as day, hour, and minute
axis = TimeAxisItem(orientation='bottom')

plot = win.addPlot(title="Battery Level", axisItems={'bottom': axis})
plot.getAxis('left').setLabel("Battery Level", units='%')
plot.getAxis('bottom').setLabel("Time", units='')

curve = plot.plot(pen='y')

# Set y-axis range to be from 0 to 100
plot.setYRange(0, 100, padding=0)

# Show grid lines on the plot
plot.showGrid(x=True, y=True, alpha=0.3)

def update():
    df = read_and_prepare_data('data.csv')
    curve.setData(df['Timestamp'].astype(int), df['Level'])  # Convert Timestamp to int for plotting

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)  # Update every 1000 milliseconds (1 second)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()
