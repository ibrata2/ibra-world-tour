const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('ibra', {
  toggleFullscreen: () => ipcRenderer.send('fullscreen'),
  openAssets: () => ipcRenderer.send('assets')
});
