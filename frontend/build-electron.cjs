const builder = require('electron-builder')
const path = require('path')
const os = require('os')
const fs = require('fs')

const tempOutputDir = path.join(os.tmpdir(), 'chronos-electron-build')
const finalReleaseDir = path.join(__dirname, 'release')

async function run() {
  console.log('Packaging Chronos AI Desktop App in safe build area:', tempOutputDir)
  
  if (fs.existsSync(tempOutputDir)) {
    try {
      fs.rmSync(tempOutputDir, { recursive: true, force: true })
    } catch (e) {
      console.warn('Note on temp cleaning:', e.message)
    }
  }
  fs.mkdirSync(tempOutputDir, { recursive: true })

  await builder.build({
    targets: builder.Platform.WINDOWS.createTarget(['nsis', 'portable']),
    config: {
      appId: 'com.chronos.ai.twin',
      productName: 'Chronos AI Predictive Maintenance',
      directories: {
        output: tempOutputDir,
        app: __dirname
      },
      files: [
        'dist/**/*',
        'electron/**/*',
        'resources/**/*'
      ],
      extraResources: [
        {
          from: path.join(__dirname, '../dist-backend/chronos-backend'),
          to: 'backend',
          filter: ['**/*']
        }
      ],
      win: {
        target: ['nsis', 'portable'],
        icon: path.join(__dirname, 'resources/icon.ico')
      },
      nsis: {
        oneClick: false,
        allowToChangeInstallationDirectory: true,
        createDesktopShortcut: true,
        createStartMenuShortcut: true,
        shortcutName: 'Chronos AI',
        artifactName: 'Chronos-AI-Setup.exe'
      },
      portable: {
        artifactName: '${productName} (Portable).${ext}'
      }
    }
  })

  console.log('Build completed. Transferring artifacts to:', finalReleaseDir)
  fs.mkdirSync(finalReleaseDir, { recursive: true })

  const entries = fs.readdirSync(tempOutputDir)
  for (const entry of entries) {
    const src = path.join(tempOutputDir, entry)
    const stat = fs.statSync(src)
    if (stat.isFile() && (entry.endsWith('.exe') || entry.endsWith('.blockmap') || entry.endsWith('.yml'))) {
      const dest = path.join(finalReleaseDir, entry)
      console.log('Copying artifact: ' + entry)
      fs.copyFileSync(src, dest)
    }
  }

  console.log('====================================================')
  console.log('CHRONOS AI DESKTOP APP BUILT SUCCESSFULLY!')
  console.log('Artifacts location:', finalReleaseDir)
  console.log('====================================================')
}

run().catch((err) => {
  console.error('Packaging failed:', err)
  process.exit(1)
})
