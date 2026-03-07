const { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let tray;
let pythonProcess = null;

// Determine python backend path (works both in dev and packaged exe)
function getPythonPath() {
  if (app.isPackaged) {
    // Matches extraResources "to" path in package.json
    return path.join(process.resourcesPath, 'backend', 'task.exe');
  }
  // Dev: watcher.py sits one level up in backend/ folder
  return path.join(__dirname, '..', 'backend', 'watcher.py');
}

function getPythonExecutable() {
  if (app.isPackaged) {
    return getPythonPath(); // bundled exe, self-contained
  }
  return 'python'; // dev mode
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 680,
    minWidth: 780,
    minHeight: 580,
    frame: false,
    titleBarStyle: 'hidden',
    backgroundColor: '#0a0a0f',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
  });

  mainWindow.loadFile(path.join(__dirname, 'src', 'index.html'));

  // Hide to tray on close
  mainWindow.on('close', (e) => {
    if (!app.isQuiting) {
      e.preventDefault();
      mainWindow.hide();
    }
  });
}

function createTray() {
  const iconPath = path.join(__dirname, 'assets', 'tray-icon.png');
  const icon = fs.existsSync(iconPath)
    ? nativeImage.createFromPath(iconPath)
    : nativeImage.createEmpty();

  tray = new Tray(icon);
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Open TicketWatch', click: () => mainWindow.show() },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        app.isQuiting = true;
        stopPython();
        app.quit();
      },
    },
  ]);
  tray.setToolTip('TicketWatch — monitoring tickets');
  tray.setContextMenu(contextMenu);
  tray.on('double-click', () => mainWindow.show());
}

// ── Python process management ──────────────────────────────────────────────

function startPython(taskConfig) {
  stopPython();

  const exe = getPythonExecutable();
  const script = app.isPackaged ? [] : [getPythonPath()];
  const args = [...script, JSON.stringify(taskConfig)];

  pythonProcess = spawn(exe, args, { stdio: ['pipe', 'pipe', 'pipe'] });

  pythonProcess.stdout.on('data', (data) => {
    const lines = data.toString().split('\n').filter(Boolean);
    lines.forEach((line) => {
      try {
        const msg = JSON.parse(line);
        mainWindow?.webContents.send('python-message', msg);
      } catch {
        mainWindow?.webContents.send('python-message', { type: 'log', text: line });
      }
    });
  });

  pythonProcess.stderr.on('data', (data) => {
    mainWindow?.webContents.send('python-message', {
      type: 'error',
      text: data.toString(),
    });
  });

  pythonProcess.on('close', (code) => {
    mainWindow?.webContents.send('python-message', {
      type: 'stopped',
      code,
    });
    pythonProcess = null;
  });
}

function stopPython() {
  if (pythonProcess) {
    const pid = pythonProcess.pid;
    try {
      // Kill entire process tree (task.exe + Chrome child processes)
      if (process.platform === 'win32') {
        require('child_process').execSync(`taskkill /PID ${pid} /T /F`, { stdio: 'ignore' });
      } else {
        process.kill(-pid, 'SIGKILL');
      }
    } catch (e) {
      // Process may already be dead
    }
    pythonProcess = null;
  }
}

// ── IPC handlers ───────────────────────────────────────────────────────────

ipcMain.on('start-watch', (_, config) => startPython(config));
ipcMain.on('stop-watch', () => {
  stopPython();
  mainWindow?.webContents.send('python-message', { type: 'stopped', code: 0 });
});
ipcMain.on('window-minimize', () => mainWindow.minimize());
ipcMain.on('window-hide',     () => mainWindow.hide());
ipcMain.on('window-close',    () => mainWindow.hide());   // legacy compat
ipcMain.on('window-quit',     () => {
  app.isQuiting = true;
  stopPython();
  app.quit();
});

// ── App lifecycle ──────────────────────────────────────────────────────────

app.whenReady().then(() => {
  createWindow();
  createTray();
});

app.on('window-all-closed', (e) => e.preventDefault());
app.on('before-quit', () => stopPython());