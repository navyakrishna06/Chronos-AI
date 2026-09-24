const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1600,
    height: 1000,
    minWidth: 1200,
    minHeight: 700,

    backgroundColor: '#05070d',

    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // React production build location
  const indexPath = path.join(
    process.resourcesPath,
    'frontend',
    'dist',
    'index.html'
  );

  console.log('Chronos index path:');
  console.log(indexPath);

  win.loadFile(indexPath);

  win.webContents.on(
    'did-fail-load',
    (event, errorCode, errorDescription) => {
      console.error('Chronos dashboard failed to load');
      console.error('Error code:', errorCode);
      console.error('Error:', errorDescription);
      console.error('Path:', indexPath);
    }
  );

  win.webContents.on('did-finish-load', () => {
    console.log('Chronos dashboard loaded successfully.');
  });

  win.webContents.on(
    'console-message',
    (event, level, message, line, sourceId) => {
      console.log(
        `[Renderer] ${message}`
      );
    }
  );
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});