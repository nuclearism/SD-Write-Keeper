#!/usr/bin/python3

import time
import wx
import os, string
import threading
from ctypes import windll

DRIVE_REMOVABLE = 2

class SDKeeper(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(280, 90), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.keep_started = 0;
        self.initui()
        self.Show()

    def initui(self):
        panel = wx.Panel(self, -1)
        drive_list = get_available_drive()
        grid = wx.GridSizer(2, 2, 0, 20)
        self.btn_msg = "KEEP CALM"
        self.button = wx.Button(panel, 1, self.btn_msg)
        self.combo = wx.ComboBox(panel, 2, "Drive", (15, 10), (100, 20), drive_list, wx.CB_DROPDOWN|wx.ALIGN_CENTER_VERTICAL)
        self.label = wx.StaticText(panel, 3, label = "SD write Keeper")
        grid.Add(self.combo, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL | wx.TOP , 10)
        grid.Add(self.button, 1, wx.ALIGN_CENTER_VERTICAL | wx.TOP, 10)
        grid.Add(self.label, 2, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT | wx.LEFT, 5)
        self.Bind(wx.EVT_BUTTON, self.OnClick, id=1)
        panel.SetSizer(grid)

    def settimer(self):
        self.threadtimer = threading.Timer(3, self.keep_write)
        self.threadtimer.start()

    def keep_write(self):
        f = open(self.path+'keep_write.txt', mode='wt', encoding='utf-8')
        f.write(time.ctime())
        f.close()
        self.settimer()

    def OnClick(self, event):
        if self.keep_started == 0:
            self.path = self.combo.GetValue()
            if self.path == "Drive":
                self.label.SetLabel('Select the Drive!')
                return -1
            else:
                self.label.SetLabel("Keep write every 1hr")
                self.button.SetLabel("WRITE ON")
                self.keep_write()
                self.keep_started = 1

        else:
            self.threadtimer.cancel()
            self.combo.Set(get_available_drive())
            self.combo.SetLabel("Drive")
            self.label.SetLabel("Stopping write keeper...")
            self.button.SetLabel(self.btn_msg)
            self.keep_started = 0


def get_available_drive():
    drives = ['%s:/' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    drive_type = [windll.kernel32.GetDriveTypeW(i) for i in drives]
    return [ v for i, v in enumerate(drives) if drive_type[i] == DRIVE_REMOVABLE]

def main():
    app = wx.App()
    SDKeeper(None, title='sd_write_keeper')
    app.MainLoop()



if __name__ == '__main__':
    main()


