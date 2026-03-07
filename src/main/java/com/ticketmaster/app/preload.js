const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  startWatch: (config) => ipcRenderer.send('start-watch', config),
  stopWatch: () => ipcRenderer.send('stop-watch'),
  onMessage: (cb) => ipcRenderer.on('python-message', (_, msg) => cb(msg)),
  removeListeners: () => ipcRenderer.removeAllListeners('python-message'),
  minimize: () => ipcRenderer.send('window-minimize'),
  hide:     () => ipcRenderer.send('window-hide'),
  close:    () => ipcRenderer.send('window-hide'),   // keep compat
  quit:     () => ipcRenderer.send('window-quit'),
});