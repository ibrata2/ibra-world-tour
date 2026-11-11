const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('path');
let win;
app.whenReady().then(() => {
  win = new BrowserWindow({
    width: 1280, height: 720, minWidth: 960, minHeight: 540, backgroundColor: '#000000', autoHideMenuBar: true,
    title: 'IBRA World Tour', icon: path.join(__dirname, 'build', 'icon.ico'), fullscreen: true,
    webPreferences: { preload: path.join(__dirname, 'preload.js'), backgroundThrottling: false }
  });
  win.setMenu(null);
  win.loadFile(path.join(__dirname, 'app', 'index.html'));
});
ipcMain.on('fullscreen', () => win && win.setFullScreen(!win.isFullScreen()));
ipcMain.on('assets', () => shell.openPath(path.join(__dirname, 'app', 'assets')));
app.on('window-all-closed', () => app.quit());
