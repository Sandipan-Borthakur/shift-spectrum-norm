from matplotlib.widgets import RectangleSelector, Button, TextBox
import numpy as np
import matplotlib.pyplot as plt
import sys


class ShiftSpec:

    def __init__(self, path):
        self.dely = 1.005
        data = np.loadtxt(path)
        self.datashape = data.shape[1]
        self.wave, self.flux = data[:, 0], data[:, 1]
        if self.datashape == 3:
            self.fluxerr = data[:, 2]

        fig, self.ax = plt.subplots()
        self.mainPlot, = self.ax.plot(self.wave, self.flux, 'k')
        self.ax.set_xlim(min(self.wave) - 100, max(self.wave) + 100)
        self.ax.axhline(1, color='g', ls='--')

        self.RS = RectangleSelector(self.ax, self.line_select_callback, useblit=True, button=[1], interactive=True)
        beg = 0.83
        delpos = 0.08
        axclose = fig.add_axes([beg, 0.9, 0.07, 0.065])
        bclose = Button(axclose, 'Accept')
        bclose.on_clicked(self.accept)

        axaccept = fig.add_axes([beg - delpos, 0.9, 0.07, 0.065])
        baccept = Button(axaccept, 'Select')
        baccept.on_clicked(self.select)

        axdown = fig.add_axes([beg - 2 * delpos, 0.9, 0.07, 0.065])
        bdown = Button(axdown, 'Down')
        bdown.on_clicked(self.movedown)

        axup = fig.add_axes([beg - 3 * delpos, 0.9, 0.07, 0.065])
        bup = Button(axup, 'Up')
        bup.on_clicked(self.moveup)

        axdelybox = fig.add_axes([beg - 4 * delpos, 0.9, 0.07, 0.065])
        initial_delytext = '1.005'
        delytext_box = TextBox(axdelybox, 'delY ', initial=initial_delytext)
        delytext_box.on_submit(self.submitdely)

        axsave = fig.add_axes([beg - 5.25 * delpos, 0.9, 0.07, 0.065])
        bsave = Button(axsave, 'Save')
        bsave.on_clicked(self.savefile)

        axbox = fig.add_axes([beg - 7.4 * delpos, 0.9, 0.16, 0.065])
        initial_text = ''
        text_box = TextBox(axbox, 'SaveFile', initial=initial_text)
        text_box.on_submit(self.submit)

        plt.connect('key_press_event', self.movearrows)
        plt.connect('key_press_event', self.selectpress)
        plt.connect('key_press_event', self.acceptpress)
        figmanager = plt.get_current_fig_manager()
        figmanager.window.showMaximized()
        plt.show()

    def select(self, event):
        self.RS.clear()
        self.ind = np.where((self.wave >= x1) & (self.wave <= x2))[0]
        self.waveCrop = self.wave[self.ind]
        self.fluxCrop = self.flux[self.ind]
        if self.datashape == 3:
            self.fluxerrCrop = self.fluxerr[self.ind]
        self.axOrig, = self.ax.plot(self.waveCrop, self.fluxCrop, 'r')
        if event.inaxes is not None:
            event.inaxes.figure.canvas.draw_idle()

    def selectpress(self, event):
        if event.key in ['W', 'w']:
            self.RS.clear()
            self.ind = np.where((self.wave >= x1) & (self.wave <= x2))[0]
            self.waveCrop = self.wave[self.ind]
            self.fluxCrop = self.flux[self.ind]
            if self.datashape == 3:
                self.fluxerrCrop = self.fluxerr[self.ind]
            self.axOrig, = self.ax.plot(self.waveCrop, self.fluxCrop, 'r')
            if event.inaxes is not None:
                event.inaxes.figure.canvas.draw_idle()

    def accept(self, event):
        self.axOrig.remove()
        if event.inaxes is not None:
            event.inaxes.figure.canvas.draw_idle()
        self.flux[self.ind] = self.fluxCrop
        if self.datashape == 3:
            self.fluxerr[self.ind] = self.fluxerrCrop
        self.mainPlot.set_xdata(self.wave)
        self.mainPlot.set_ydata(self.flux)

    def acceptpress(self, event):
        if event.key in ['A', 'a']:
            self.axOrig.remove()
            if event.inaxes is not None:
                event.inaxes.figure.canvas.draw_idle()
            self.flux[self.ind] = self.fluxCrop
            if self.datashape == 3:
                self.fluxerr[self.ind] = self.fluxerrCrop
            self.mainPlot.set_xdata(self.wave)
            self.mainPlot.set_ydata(self.flux)

    def moveup(self, event):
        self.fluxCrop = self.fluxCrop * self.dely
        if self.datashape == 3:
            self.fluxerrCrop = self.fluxerrCrop * self.dely
        self.axOrig.remove()
        self.axOrig, = self.ax.plot(self.waveCrop, self.fluxCrop, 'r')
        if event.inaxes is not None:
            event.inaxes.figure.canvas.draw_idle()

    def movedown(self, event):
        self.fluxCrop = self.fluxCrop / self.dely
        if self.datashape == 3:
            self.fluxerrCrop = self.fluxerrCrop * self.dely
        self.axOrig.remove()
        self.axOrig, = self.ax.plot(self.waveCrop, self.fluxCrop, 'r')
        if event.inaxes is not None:
            event.inaxes.figure.canvas.draw_idle()

    def movearrows(self, event):
        if event.key in ['up']:
            self.fluxCrop = self.fluxCrop * self.dely
            if self.datashape == 3:
                self.fluxerrCrop = self.fluxerrCrop * self.dely
            self.axOrig.remove()
            self.axOrig, = self.ax.plot(self.waveCrop, self.fluxCrop, 'r')
            if event.inaxes is not None:
                event.inaxes.figure.canvas.draw_idle()
        if event.key in ['down']:
            self.fluxCrop = self.fluxCrop / self.dely
            if self.datashape == 3:
                self.fluxerrCrop = self.fluxerrCrop * self.dely
            self.axOrig.remove()
            self.axOrig, = self.ax.plot(self.waveCrop, self.fluxCrop, 'r')
            if event.inaxes is not None:
                event.inaxes.figure.canvas.draw_idle()

    def submitdely(self, dely):
        self.dely = float(dely)

    def submit(self, text):
        self.saveText = text

    def savefile(self, event):
        print(self.saveText)
        if self.datashape == 3:
            np.savetxt(self.saveText, np.c_[self.wave, self.flux, self.fluxerr], delimiter=" ",
                       fmt=['%.2f', '%.5f', '%.5f'])
        else:
            np.savetxt(self.saveText, np.c_[self.wave, self.flux], delimiter=" ")

    def line_select_callback(self, eclick, erelease):
        global x1, y1, x2, y2
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

if __name__ == "__main__":
    try:
        path = sys.argv[1]
        ShiftSpec(path)
    except Exception as e:
        print(e)
