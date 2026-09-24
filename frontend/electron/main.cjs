const { app, BrowserWindow, shell } = require('electron')
const path = require('path')
const { spawn, execSync } = require('child_process')
const fs = require('fs')

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged

let mainWindow = null
let backendProcess = null

// Start bundled Python/FastAPI backend
function startBackend() {
  let backendExePath = ''

  if (app.isPackaged) {
    backendExePath = path.join(process.resourcesPath, 'backend', 'chronos-backend.exe')
  } else {
    backendExePath = path.join(__dirname, '../../dist-backend/chronos-backend/chronos-backend.exe')
  }

  console.log('[Electron Main] Checking backend executable at:', backendExePath)

  if (fs.existsSync(backendExePath)) {
    try {
      backendProcess = spawn(backendExePath, [], {
        windowsHide: true,
        stdio: 'ignore'
      })

      console.log('[Electron Main] chronos-backend started with PID:', backendProcess.pid)

      backendProcess.on('error', (err) => {
        console.error('[Electron Main] Failed to spawn backend:', err)
      })

      backendProcess.on('exit', (code, signal) => {
        console.log(`[Electron Main] Backend exited with code ${code}, signal ${signal}`)
        backendProcess = null
      })
    } catch (e) {
      console.error('[Electron Main] Error launching backend:', e)
    }
  } else {
    console.warn('[Electron Main] Backend executable not found at:', backendExePath)
  }
}

// Stop backend process cleanly
function stopBackend() {
  if (backendProcess && backendProcess.pid) {
    console.log('[Electron Main] Terminating backend PID:', backendProcess.pid)
    try {
      if (process.platform === 'win32') {
        execSync(`taskkill /pid ${backendProcess.pid} /T /F`, { stdio: 'ignore' })
      } else {
        backendProcess.kill('SIGKILL')
      }
    } catch (e) {
      try {
        backendProcess.kill()
      } catch (err) {}
    }
    backendProcess = null
  }
}

function createWindow() {
  const iconPath = path.join(__dirname, '../resources/icon.ico')

  mainWindow = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1024,
    minHeight: 700,
    backgroundColor: '#090a10',
    show: false,
    autoHideMenuBar: true,
    title: 'Chronos AI - 3D Predictive Maintenance Twin',
    icon: iconPath,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true
    }
  })

  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('https:') || url.startsWith('http:')) {
      shell.openExternal(url)
    }
    return { action: 'deny' }
  })

  if (isDev && process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL)
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

// App lifecycle
app.whenReady().then(() => {
  startBackend()
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('will-quit', () => {
  stopBackend()
})

app.on('before-quit', () => {
  stopBackend()
})

process.on('exit', () => {
  stopBackend()
})

