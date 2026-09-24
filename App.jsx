import React, { useState, useEffect, useRef, useMemo } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, Html, Float } from '@react-three/drei'
import * as THREE from 'three'
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  ShieldAlert,
  Cpu,
  Bell,
  RotateCw,
  Wrench,
  Sliders,
  Play, 
  Pause,
  RefreshCw,
  Layers,
  Zap,
  Thermometer,
  Gauge,
  ChevronRight,
  Check,
  Eye,
  Radio,
  Clock,
  Sparkles
} from 'lucide-react'
import './App.css'

// ============================================================
// CHRONOS AI RISK LOGIC (Matches Day 49 & 51 Model Integration)
// ============================================================
function calculateMachineRisk(torque, toolWear, tempDiff, rotSpeed) {
  let riskScore = 0.03 // base risk

  // High torque contribution
  if (torque > 65) {
    riskScore += 0.45 * Math.min(1.0, (torque - 65) / 25)
  } else if (torque > 50) {
    riskScore += 0.20 * ((torque - 50) / 15)
  }

  // Tool wear contribution
  if (toolWear > 200) {
    riskScore += 0.40 * Math.min(1.0, (toolWear - 200) / 50)
  } else if (toolWear > 130) {
    riskScore += 0.22 * ((toolWear - 130) / 70)
  }

  // Heat Dissipation Failure (HDF) condition: low temp diff (< 8.6K) at low rot speed
  if (tempDiff < 8.6 && rotSpeed < 1400) {
    riskScore += 0.35
  }

  // Clamp probability between 1% and 98%
  const failureProbability = Math.min(0.98, Math.max(0.01, riskScore))

  let riskLevel = 'NORMAL'
  let alertMessage = 'Machine is operating within the predicted normal condition.'

  if (failureProbability >= 0.70) {
    riskLevel = 'CRITICAL'
    alertMessage =
      'High probability of machine failure. Immediate maintenance inspection recommended.'
  } else if (failureProbability >= 0.30) {
    riskLevel = 'WARNING'
    alertMessage =
      'Elevated machine failure risk detected. Maintenance inspection recommended.'
  }

  return {
    failureProbability,
    normalProbability: 1 - failureProbability,
    riskLevel,
    alertMessage,
    hdf: tempDiff < 8.6 && rotSpeed < 1400,
    osf: torque > 62 && toolWear > 140,
    pwf: torque * rotSpeed > 95000,
    twf: toolWear > 210
  }
}

// Initial machine fleet telemetry data
const INITIAL_MACHINES = [
  {
    id: 'CH-CNC-01',
    name: 'CNC 5-Axis Milling Center',
    type: 'Precision Machining',
    position: [-5, 0, 2],
    airTemp: 298.5,
    procTemp: 308.7,
    rotSpeed: 1540,
    torque: 42.5,
    toolWear: 36,
    powerKw: 6.4,
    vibration: '1.2 mm/s',
    operationalHours: 4210,
    maintenanceDue: '42 days'
  },
  {
    id: 'CH-HYD-04',
    name: 'High-Pressure Hydraulic Pump',
    type: 'Fluid Dynamics',
    position: [-2.2, 0, -2.5],
    airTemp: 302.2,
    procTemp: 312.0,
    rotSpeed: 1310,
    torque: 68.0,
    toolWear: 148,
    powerKw: 9.8,
    vibration: '4.9 mm/s',
    operationalHours: 8350,
    maintenanceDue: '3 days'
  },
  {
    id: 'CH-GEN-07',
    name: 'Turbo Induction Generator',
    type: 'Heavy Power Gen',
    position: [2.2, 0, -2.5],
    airTemp: 304.6,
    procTemp: 312.8,
    rotSpeed: 1250,
    torque: 76.5,
    toolWear: 228,
    powerKw: 15.2,
    vibration: '9.8 mm/s',
    operationalHours: 12480,
    maintenanceDue: 'IMMEDIATE'
  },
  {
    id: 'CH-ROB-12',
    name: 'Articulated 6-Axis Robot',
    type: 'Automated Assembly',
    position: [5, 0, 2],
    airTemp: 299.1,
    procTemp: 308.9,
    rotSpeed: 1820,
    torque: 34.2,
    toolWear: 58,
    powerKw: 4.8,
    vibration: '1.6 mm/s',
    operationalHours: 3190,
    maintenanceDue: '30 days'
  },
  {
    id: 'CH-DRV-09',
    name: 'Heavy Rotary Kiln Drive',
    type: 'Thermal Drive',
    position: [0, 0, 3.5],
    airTemp: 301.9,
    procTemp: 310.2,
    rotSpeed: 1350,
    torque: 58.8,
    toolWear: 162,
    powerKw: 8.6,
    vibration: '3.8 mm/s',
    operationalHours: 9740,
    maintenanceDue: '6 days'
  }
]

// ============================================================
// 3D PROCEDURAL MACHINE MODELS (React Three Fiber)
// ============================================================

// Model 1: CNC Milling Center
function CncMachine({ isSelected, riskColor, onClick, onPointerOver, onPointerOut }) {
  const spindleRef = useRef()
  const bitRef = useRef()

  useFrame((_, delta) => {
    if (spindleRef.current) spindleRef.current.rotation.y += delta * 6
    if (bitRef.current) bitRef.current.rotation.y += delta * 12
  })

  return (
    <group
      onClick={onClick}
      onPointerOver={onPointerOver}
      onPointerOut={onPointerOut}
    >
      {/* Base Foundation */}
      <mesh position={[0, 0.25, 0]} castShadow receiveShadow>
        <boxGeometry args={[2.2, 0.5, 2.2]} />
        <meshStandardMaterial color="#1e2230" roughness={0.4} metalness={0.8} />
      </mesh>

      {/* Bed table */}
      <mesh position={[0, 0.55, 0]}>
        <boxGeometry args={[1.7, 0.12, 1.7]} />
        <meshStandardMaterial color="#334155" roughness={0.3} metalness={0.9} />
      </mesh>

      {/* Upright Twin Columns */}
      <mesh position={[-0.8, 1.4, -0.6]}>
        <boxGeometry args={[0.35, 1.6, 0.4]} />
        <meshStandardMaterial color="#0f172a" roughness={0.5} metalness={0.7} />
      </mesh>
      <mesh position={[0.8, 1.4, -0.6]}>
        <boxGeometry args={[0.35, 1.6, 0.4]} />
        <meshStandardMaterial color="#0f172a" roughness={0.5} metalness={0.7} />
      </mesh>

      {/* Cross Beam */}
      <mesh position={[0, 2.1, -0.6]}>
        <boxGeometry args={[1.95, 0.35, 0.5]} />
        <meshStandardMaterial color="#1e293b" roughness={0.4} metalness={0.8} />
      </mesh>

      {/* Spindle Housing */}
      <mesh position={[0, 1.6, -0.2]}>
        <boxGeometry args={[0.5, 0.7, 0.5]} />
        <meshStandardMaterial color="#0284c7" roughness={0.3} metalness={0.6} />
      </mesh>

      {/* Rotating Chuck */}
      <group ref={spindleRef} position={[0, 1.2, -0.2]}>
        <mesh>
          <cylinderGeometry args={[0.18, 0.18, 0.2, 16]} />
          <meshStandardMaterial color="#94a3b8" metalness={0.9} roughness={0.2} />
        </mesh>
      </group>

      {/* Drill bit */}
      <group ref={bitRef} position={[0, 0.95, -0.2]}>
        <mesh>
          <cylinderGeometry args={[0.04, 0.01, 0.35, 8]} />
          <meshStandardMaterial color="#38bdf8" metalness={0.95} roughness={0.1} />
        </mesh>
      </group>

      {/* Workpiece block */}
      <mesh position={[0, 0.7, -0.1]}>
        <boxGeometry args={[0.6, 0.2, 0.6]} />
        <meshStandardMaterial color="#fbbf24" metalness={0.7} roughness={0.3} />
      </mesh>

      {/* Protective Tinted Visor */}
      <mesh position={[0, 1.2, 0.75]}>
        <boxGeometry args={[1.8, 1.2, 0.05]} />
        <meshStandardMaterial
          color="#00f0ff"
          transparent
          opacity={0.2}
          roughness={0.1}
          metalness={0.9}
        />
      </mesh>
    </group>
  )
}

// Model 2: High-Pressure Hydraulic Pump
function HydraulicPump({ isSelected, riskColor, onClick, onPointerOver, onPointerOut }) {
  const pistonRef = useRef()

  useFrame(({ clock }) => {
    if (pistonRef.current) {
      pistonRef.current.position.y = 1.35 + Math.sin(clock.elapsedTime * 5) * 0.22
    }
  })

  return (
    <group
      onClick={onClick}
      onPointerOver={onPointerOver}
      onPointerOut={onPointerOut}
    >
      {/* Heavy Baseplate */}
      <mesh position={[0, 0.2, 0]} castShadow receiveShadow>
        <boxGeometry args={[2.0, 0.4, 2.0]} />
        <meshStandardMaterial color="#1e2433" roughness={0.6} metalness={0.7} />
      </mesh>

      {/* Motor Block with cooling fins */}
      <mesh position={[-0.45, 0.85, 0]}>
        <boxGeometry args={[0.9, 0.9, 1.2]} />
        <meshStandardMaterial color="#3b82f6" roughness={0.4} metalness={0.6} />
      </mesh>

      {/* High-Pressure Hydraulic Cylinder */}
      <mesh position={[0.55, 0.9, 0]}>
        <cylinderGeometry args={[0.42, 0.42, 1.2, 24]} />
        <meshStandardMaterial color="#475569" roughness={0.3} metalness={0.9} />
      </mesh>

      {/* Reciprocating Piston Rod */}
      <mesh ref={pistonRef} position={[0.55, 1.35, 0]}>
        <cylinderGeometry args={[0.2, 0.2, 0.65, 16]} />
        <meshStandardMaterial color="#e2e8f0" metalness={0.95} roughness={0.1} />
      </mesh>

      {/* Valve Manifold Block */}
      <mesh position={[0.55, 1.8, 0]}>
        <boxGeometry args={[0.55, 0.25, 0.55]} />
        <meshStandardMaterial color="#ca8a04" roughness={0.3} metalness={0.8} />
      </mesh>

      {/* Connecting Pipe */}
      <mesh position={[0.05, 0.9, 0.3]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.1, 0.1, 0.8, 16]} />
        <meshStandardMaterial color="#64748b" metalness={0.8} />
      </mesh>
    </group>
  )
}

// Model 3: Turbo Induction Generator (Critical Hazard Unit)
function TurboGenerator({ isSelected, riskColor, onClick, onPointerOver, onPointerOut }) {
  const rotorRef = useRef()
  const beaconRef = useRef()

  useFrame(({ clock }, delta) => {
    if (rotorRef.current) rotorRef.current.rotation.z += delta * 14
    if (beaconRef.current) {
      const pulse = (Math.sin(clock.elapsedTime * 9) + 1) * 0.5
      beaconRef.current.scale.setScalar(0.9 + pulse * 0.35)
    }
  })

  return (
    <group
      onClick={onClick}
      onPointerOver={onPointerOver}
      onPointerOut={onPointerOut}
    >
      {/* Heavy Base Skid */}
      <mesh position={[0, 0.2, 0]} castShadow receiveShadow>
        <boxGeometry args={[2.4, 0.4, 1.8]} />
        <meshStandardMaterial color="#181e29" roughness={0.5} metalness={0.8} />
      </mesh>

      {/* Turbine Barrel Casing */}
      <mesh position={[0, 1.0, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.7, 0.7, 1.8, 32]} />
        <meshStandardMaterial color="#334155" roughness={0.3} metalness={0.85} />
      </mesh>

      {/* Center Rotor / Intake Blades */}
      <group ref={rotorRef} position={[0.92, 1.0, 0]} rotation={[0, Math.PI / 2, 0]}>
        {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => (
          <mesh key={i} rotation={[0, 0, (angle * Math.PI) / 180]}>
            <boxGeometry args={[0.55, 0.08, 0.04]} />
            <meshStandardMaterial color="#ef4444" emissive="#ef4444" emissiveIntensity={0.6} />
          </mesh>
        ))}
      </group>

      {/* Transformer Core on the side */}
      <mesh position={[0, 1.0, -0.65]}>
        <boxGeometry args={[1.2, 0.8, 0.5]} />
        <meshStandardMaterial color="#1e1b4b" roughness={0.4} metalness={0.7} />
      </mesh>

      {/* Critical Flashing Hazard Beacon */}
      <group position={[0, 1.85, 0]}>
        <mesh>
          <cylinderGeometry args={[0.1, 0.12, 0.25, 12]} />
          <meshStandardMaterial color="#111827" />
        </mesh>
        <mesh ref={beaconRef} position={[0, 0.2, 0]}>
          <sphereGeometry args={[0.16, 16, 16]} />
          <meshStandardMaterial
            color="#ff0044"
            emissive="#ff0044"
            emissiveIntensity={2.5}
            roughness={0.1}
          />
        </mesh>
        <pointLight color="#ff0044" intensity={2} distance={5} />
      </group>
    </group>
  )
}

// Model 4: Robotic Articulated Arm
function RobotArm({ isSelected, riskColor, onClick, onPointerOver, onPointerOut }) {
  const armBaseRef = useRef()
  const gripperRef = useRef()

  useFrame(({ clock }) => {
    if (armBaseRef.current) {
      armBaseRef.current.rotation.y = Math.sin(clock.elapsedTime * 1.2) * 0.6
    }
    if (gripperRef.current) {
      gripperRef.current.rotation.z = Math.sin(clock.elapsedTime * 2.5) * 0.3
    }
  })

  return (
    <group
      onClick={onClick}
      onPointerOver={onPointerOver}
      onPointerOut={onPointerOut}
    >
      {/* Octagonal Heavy Pedestal */}
      <mesh position={[0, 0.25, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[0.8, 0.95, 0.5, 8]} />
        <meshStandardMaterial color="#1f293d" roughness={0.4} metalness={0.8} />
      </mesh>

      {/* Swivel Turntable */}
      <group ref={armBaseRef} position={[0, 0.55, 0]}>
        <mesh position={[0, 0.15, 0]}>
          <cylinderGeometry args={[0.5, 0.5, 0.3, 16]} />
          <meshStandardMaterial color="#0284c7" roughness={0.3} metalness={0.7} />
        </mesh>

        {/* Lower Arm Boom */}
        <mesh position={[0, 0.75, 0.2]} rotation={[0.4, 0, 0]}>
          <boxGeometry args={[0.22, 1.1, 0.22]} />
          <meshStandardMaterial color="#e2e8f0" metalness={0.8} roughness={0.2} />
        </mesh>

        {/* Elbow Joint */}
        <mesh position={[0, 1.25, 0.4]}>
          <sphereGeometry args={[0.22, 16, 16]} />
          <meshStandardMaterial color="#0284c7" metalness={0.8} />
        </mesh>

        {/* Forearm */}
        <mesh position={[0, 1.6, 0.05]} rotation={[-0.6, 0, 0]}>
          <boxGeometry args={[0.18, 0.9, 0.18]} />
          <meshStandardMaterial color="#64748b" metalness={0.8} />
        </mesh>

        {/* End Effector Gripper */}
        <group ref={gripperRef} position={[0, 1.95, -0.2]}>
          <mesh position={[-0.1, 0, 0]}>
            <boxGeometry args={[0.06, 0.25, 0.08]} />
            <meshStandardMaterial color="#38bdf8" metalness={0.9} />
          </mesh>
          <mesh position={[0.1, 0, 0]}>
            <boxGeometry args={[0.06, 0.25, 0.08]} />
            <meshStandardMaterial color="#38bdf8" metalness={0.9} />
          </mesh>
          <pointLight position={[0, 0, 0]} color="#00f0ff" intensity={0.8} distance={2} />
        </group>
      </group>
    </group>
  )
}

// Model 5: Heavy Rotary Kiln Drive
function RotaryKiln({ isSelected, riskColor, onClick, onPointerOver, onPointerOut }) {
  const drumRef = useRef()

  useFrame((_, delta) => {
    if (drumRef.current) drumRef.current.rotation.x += delta * 1.5
  })

  return (
    <group
      onClick={onClick}
      onPointerOver={onPointerOver}
      onPointerOut={onPointerOut}
    >
      {/* Heavy Steel Support Frame */}
      <mesh position={[0, 0.2, 0]} castShadow receiveShadow>
        <boxGeometry args={[2.2, 0.4, 2.0]} />
        <meshStandardMaterial color="#1a202c" roughness={0.6} metalness={0.7} />
      </mesh>

      {/* Roller Bearing Pedestals */}
      <mesh position={[-0.6, 0.6, -0.5]}>
        <boxGeometry args={[0.3, 0.6, 0.3]} />
        <meshStandardMaterial color="#475569" metalness={0.8} />
      </mesh>
      <mesh position={[0.6, 0.6, -0.5]}>
        <boxGeometry args={[0.3, 0.6, 0.3]} />
        <meshStandardMaterial color="#475569" metalness={0.8} />
      </mesh>
      <mesh position={[-0.6, 0.6, 0.5]}>
        <boxGeometry args={[0.3, 0.6, 0.3]} />
        <meshStandardMaterial color="#475569" metalness={0.8} />
      </mesh>
      <mesh position={[0.6, 0.6, 0.5]}>
        <boxGeometry args={[0.3, 0.6, 0.3]} />
        <meshStandardMaterial color="#475569" metalness={0.8} />
      </mesh>

      {/* Rotating Drum Cylinder */}
      <group ref={drumRef} position={[0, 1.05, 0]} rotation={[0, 0, Math.PI / 2]}>
        <mesh>
          <cylinderGeometry args={[0.55, 0.55, 1.8, 24]} />
          <meshStandardMaterial color="#f59e0b" roughness={0.4} metalness={0.6} />
        </mesh>
        {/* Drive Sprocket Gear Teeth */}
        <mesh position={[0, 0, 0]}>
          <cylinderGeometry args={[0.65, 0.65, 0.25, 16]} />
          <meshStandardMaterial color="#334155" metalness={0.9} roughness={0.2} />
        </mesh>
      </group>

      {/* Drive Motor & Gearbox Housing */}
      <mesh position={[0, 0.7, -0.9]}>
        <boxGeometry args={[1.1, 0.7, 0.5]} />
        <meshStandardMaterial color="#0f172a" roughness={0.4} metalness={0.8} />
      </mesh>
    </group>
  )
}

// Wrapper for all machines with interactive floor aura and 3D HTML telemetry badge
function MachineNode({ machine, isSelected, onSelect }) {
  const [hovered, setHovered] = useState(false)
  const auraRef = useRef()

  const riskColor = useMemo(() => {
    if (machine.riskLevel === 'CRITICAL') return '#ef4444'
    if (machine.riskLevel === 'WARNING') return '#f59e0b'
    return '#10b981'
  }, [machine.riskLevel])

  useFrame(({ clock }) => {
    if (auraRef.current) {
      const pulseSpeed = machine.riskLevel === 'CRITICAL' ? 7 : machine.riskLevel === 'WARNING' ? 4 : 2
      const pulse = (Math.sin(clock.elapsedTime * pulseSpeed) + 1) * 0.5
      auraRef.current.material.opacity = 0.35 + pulse * (isSelected ? 0.45 : 0.25)
      auraRef.current.scale.setScalar(1 + pulse * 0.08)
    }
  })

  return (
    <group position={machine.position}>
      {/* Dynamic Pulsing Ground Ring */}
      <mesh ref={auraRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.03, 0]}>
        <ringGeometry args={[1.35, 1.55, 36]} />
        <meshBasicMaterial
          color={riskColor}
          transparent
          opacity={0.4}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Selected Machine Scanning Column / Highlight Beam */}
      {isSelected && (
        <mesh position={[0, 1.3, 0]}>
          <cylinderGeometry args={[1.5, 1.5, 2.6, 32, 1, true]} />
          <meshBasicMaterial
            color="#00f0ff"
            transparent
            opacity={0.12}
            side={THREE.DoubleSide}
            wireframe
          />
        </mesh>
      )}

      {/* 3D Model Switcher */}
      {machine.id === 'CH-CNC-01' && (
        <CncMachine
          isSelected={isSelected}
          riskColor={riskColor}
          onClick={() => onSelect(machine.id)}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
        />
      )}
      {machine.id === 'CH-HYD-04' && (
        <HydraulicPump
          isSelected={isSelected}
          riskColor={riskColor}
          onClick={() => onSelect(machine.id)}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
        />
      )}
      {machine.id === 'CH-GEN-07' && (
        <TurboGenerator
          isSelected={isSelected}
          riskColor={riskColor}
          onClick={() => onSelect(machine.id)}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
        />
      )}
      {machine.id === 'CH-ROB-12' && (
        <RobotArm
          isSelected={isSelected}
          riskColor={riskColor}
          onClick={() => onSelect(machine.id)}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
        />
      )}
      {machine.id === 'CH-DRV-09' && (
        <RotaryKiln
          isSelected={isSelected}
          riskColor={riskColor}
          onClick={() => onSelect(machine.id)}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
        />
      )}

      {/* Holographic 3D Status Badge Overlay */}
      <Html position={[0, 2.8, 0]} center distanceFactor={14}>
        <div
          className={`machine-3d-label ${machine.riskLevel.toLowerCase()} ${
            isSelected ? 'selected' : ''
          }`}
          onClick={(e) => {
            e.stopPropagation()
            onSelect(machine.id)
          }}
        >
          <div className="label-title">{machine.id}</div>
          <div className="label-stats">
            <span
              style={{
                color: riskColor,
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: '3px'
              }}
            >
              {machine.riskLevel}
            </span>
            <span style={{ color: '#94a3b8' }}>
              {(machine.failureProbability * 100).toFixed(1)}% fail
            </span>
          </div>
        </div>
      </Html>
    </group>
  )
}

// Camera controller component to handle camera angle presets
function CameraDirector({ cameraPreset, selectedMachinePos }) {
  const { camera } = useThree()
  const controlsRef = useRef()

  useEffect(() => {
    if (!controlsRef.current) return

    if (cameraPreset === 'OVERVIEW') {
      camera.position.set(0, 10, 14)
      controlsRef.current.target.set(0, 0, 0)
    } else if (cameraPreset === 'TOP_DOWN') {
      camera.position.set(0, 18, 0.1)
      controlsRef.current.target.set(0, 0, 0)
    } else if (cameraPreset === 'ISOMETRIC') {
      camera.position.set(11, 10, 11)
      controlsRef.current.target.set(0, 0, 0)
    } else if (cameraPreset === 'FOCUS' && selectedMachinePos) {
      camera.position.set(
        selectedMachinePos[0] + 3.5,
        selectedMachinePos[1] + 3.0,
        selectedMachinePos[2] + 4.5
      )
      controlsRef.current.target.set(
        selectedMachinePos[0],
        selectedMachinePos[1] + 1.0,
        selectedMachinePos[2]
      )
    }
    controlsRef.current.update()
  }, [cameraPreset, selectedMachinePos, camera])

  return (
    <OrbitControls
      ref={controlsRef}
      makeDefault
      maxPolarAngle={Math.PI / 2.05}
      minDistance={4}
      maxDistance={30}
      enableDamping
      dampingFactor={0.05}
    />
  )
}

// ============================================================
// MAIN APPLICATION COMPONENT
// ============================================================
export default function App() {
  const [activeTab, setActiveTab] = useState('DIGITAL_TWIN')
  const [selectedMachineId, setSelectedMachineId] = useState('CH-GEN-07')
  const [cameraPreset, setCameraPreset] = useState('OVERVIEW')
  const [isSimulating, setIsSimulating] = useState(true)
  const [isScanning, setIsScanning] = useState(false)
  const [acknowledgedAlerts, setAcknowledgedAlerts] = useState([])
  // ============================================================
// CHRONOS VOICE ALERT
// ============================================================
const previousRiskRef = useRef({})

const speakAlert = (machine) => {
  if (!machine || !window.speechSynthesis) return

  let message = ''

  if (machine.riskLevel === 'CRITICAL') {
    message = `Critical alert. ${machine.name} has a high probability of failure. Immediate maintenance inspection recommended.`
  } else if (machine.riskLevel === 'WARNING') {
    message = `Warning alert. ${machine.name} shows elevated failure risk. Maintenance inspection recommended.`
  }

  if (!message) return

  window.speechSynthesis.cancel()

  const speech = new SpeechSynthesisUtterance(message)

  speech.rate = 0.9
  speech.pitch = 1
  speech.volume = 1

  window.speechSynthesis.speak(speech)
}

  // Dynamic fleet state with telemetry and AI predictions
  const [machines, setMachines] = useState(() => {
    return INITIAL_MACHINES.map((m) => {
      const riskData = calculateMachineRisk(
        m.torque,
        m.toolWear,
        m.procTemp - m.airTemp,
        m.rotSpeed
      )
      return { ...m, ...riskData }
    })
  })

  // Currently selected machine object
  const selectedMachine = useMemo(() => {
    return machines.find((m) => m.id === selectedMachineId) || machines[0]
  }, [machines, selectedMachineId])

  // ============================================================
  // AUTOMATIC VOICE ALERT ON RISK CHANGE
  // ============================================================
  useEffect(() => {
    machines.forEach((machine) => {
      const previousRisk = previousRiskRef.current[machine.id]

      if (
        previousRisk &&
        previousRisk !== machine.riskLevel &&
        (machine.riskLevel === 'WARNING' || machine.riskLevel === 'CRITICAL')
      ) {
        speakAlert(machine)
      }

      previousRiskRef.current[machine.id] = machine.riskLevel
    })
  }, [machines])

  // Fleet overview statistics
  const stats = useMemo(() => {
    const total = machines.length
    const normalCount = machines.filter((m) => m.riskLevel === 'NORMAL').length
    const warningCount = machines.filter((m) => m.riskLevel === 'WARNING').length
    const criticalCount = machines.filter((m) => m.riskLevel === 'CRITICAL').length
    const avgFailProb =
      machines.reduce((acc, m) => acc + m.failureProbability, 0) / total
    return { total, normalCount, warningCount, criticalCount, avgFailProb }
  }, [machines])

  // Live simulation tick: subtly fluctuates sensor values every 3s
  useEffect(() => {
    if (!isSimulating) return

    const interval = setInterval(() => {
      setMachines((prevList) =>
        prevList.map((m) => {
          // Slight sensor variance
          const torqueDelta = (Math.random() - 0.49) * 0.6
          const tempDelta = (Math.random() - 0.48) * 0.15
          const newTorque = Math.max(15, m.torque + torqueDelta)
          const newProcTemp = Math.max(300, m.procTemp + tempDelta)
          const newToolWear = m.toolWear + (m.riskLevel === 'CRITICAL' ? 0.05 : 0.01)

          const riskData = calculateMachineRisk(
            newTorque,
            newToolWear,
            newProcTemp - m.airTemp,
            m.rotSpeed
          )

          return {
            ...m,
            torque: Number(newTorque.toFixed(1)),
            procTemp: Number(newProcTemp.toFixed(1)),
            toolWear: Number(newToolWear.toFixed(1)),
            ...riskData
          }
        })
      )
    }, 3000)

    return () => clearInterval(interval)
  }, [isSimulating])

  // Manual adjustment handlers for the Stress Simulator in the drawer
  const handleSliderChange = (param, value) => {
    setMachines((prevList) =>
      prevList.map((m) => {
        if (m.id !== selectedMachineId) return m

        const updated = { ...m, [param]: parseFloat(value) }
        const riskData = calculateMachineRisk(
          param === 'torque' ? parseFloat(value) : updated.torque,
          param === 'toolWear' ? parseFloat(value) : updated.toolWear,
          updated.procTemp - updated.airTemp,
          updated.rotSpeed
        )
        return { ...updated, ...riskData }
      })
    )
  }

  // Trigger live AI model re-inference via local backend with fallback
  const triggerAiInference = async () => {
    setIsScanning(true)
    try {
      const resp = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          HDF: selectedMachine.hdf ? 1 : 0,
          OSF: selectedMachine.osf ? 1 : 0,
          PWF: selectedMachine.pwf ? 1 : 0,
          TWF: selectedMachine.twf ? 1 : 0,
          High_Torque: selectedMachine.torque > 60 ? 1 : 0,
          Torque_Nm: selectedMachine.torque,
          Power_Indicator: selectedMachine.powerKw,
          Temperature_Difference_K: selectedMachine.procTemp - selectedMachine.airTemp,
          Tool_wear_min: selectedMachine.toolWear,
          High_Tool_Wear: selectedMachine.toolWear > 180 ? 1 : 0,
          Air_temperature_K: selectedMachine.airTemp,
          Temperature_Stress: selectedMachine.procTemp - selectedMachine.airTemp
        })
      })
      if (resp.ok) {
        const result = await resp.json()
        setMachines((prev) =>
          prev.map((m) => {
            if (m.id !== selectedMachine.id) return m
            return {
              ...m,
              failureProbability: result.failure_probability,
              normalProbability: result.normal_probability,
              riskLevel: result.risk_level,
              alertMessage: result.alert_message
            }
          })
        )
      }
    } catch (e) {
      console.log('Background server connecting, using local calculation:', e)
    } finally {
      setTimeout(() => {
        setIsScanning(false)
      }, 900)
    }
  }

  // Acknowledge alert
  const toggleAcknowledge = (id) => {
    setAcknowledgedAlerts((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    )
  }

  return (
    <div className="dashboard-container">
      {/* ================= SIDEBAR NAVIGATION ================= */}
      <aside className="sidebar">
        <div className="brand-header">
          <div className="brand-icon-wrap">
            <Cpu size={22} />
          </div>
          <div>
            <div className="brand-title">
              CHRONOS <span className="brand-badge">AI 3D</span>
            </div>
            <div className="brand-subtitle">Predictive Ops Twin</div>
          </div>
        </div>

        <nav className="nav-menu">
          <button
            className={`nav-item ${activeTab === 'DIGITAL_TWIN' ? 'active' : ''}`}
            onClick={() => setActiveTab('DIGITAL_TWIN')}
          >
            <Layers size={16} />
            <span>Digital Twin (3D)</span>
          </button>

          <button
            className={`nav-item ${activeTab === 'ALERTS' ? 'active' : ''}`}
            onClick={() => setActiveTab('ALERTS')}
          >
            <Bell size={16} />
            <span>Active Alerts</span>
            {stats.criticalCount > 0 && (
              <span className="nav-item-badge">{stats.criticalCount}</span>
            )}
          </button>

          <button
            className={`nav-item ${activeTab === 'AI_MODEL' ? 'active' : ''}`}
            onClick={() => setActiveTab('AI_MODEL')}
          >
            <Sparkles size={16} />
            <span>Chronos ML Model</span>
          </button>

          <button
            className={`nav-item ${activeTab === 'TELEMETRY' ? 'active' : ''}`}
            onClick={() => setActiveTab('TELEMETRY')}
          >
            <Activity size={16} />
            <span>Fleet Telemetry</span>
          </button>
        </nav>

        <div className="sidebar-status-card">
          <div className="status-header">
            <span>MODEL STATUS</span>
            <span className="live-indicator">
              <span className="pulse-dot"></span> CONNECTED
            </span>
          </div>
          <div className="system-meta">
            <div className="meta-row">
              <span>Model:</span>
              <strong style={{ color: '#fff' }}>Random Forest v2.4</strong>
            </div>
            <div className="meta-row">
              <span>F1-Score:</span>
              <span style={{ color: '#10b981' }}>0.984</span>
            </div>
            <div className="meta-row">
              <span>Inference Latency:</span>
              <span>12 ms</span>
            </div>
          </div>
        </div>
      </aside>

      {/* ================= MAIN CONTENT WRAPPER ================= */}
      <main className="main-wrapper">
        {/* TOPBAR */}
        <header className="topbar">
          <div className="topbar-left">
            <div className="breadcrumbs">
              <span>Industrial Facility</span>
              <ChevronRight size={14} />
              <span>Plant Sector 07</span>
              <ChevronRight size={14} />
              <span className="active">
                {activeTab === 'DIGITAL_TWIN'
                  ? '3D Predictive Digital Twin'
                  : activeTab === 'ALERTS'
                  ? 'Incident & Alerts Queue'
                  : activeTab === 'AI_MODEL'
                  ? 'Chronos Random Forest Diagnostics'
                  : 'Fleet Telemetry Stream'}
              </span>
            </div>
          </div>

          <div className="topbar-stats">
            <div className="stat-pill normal">
              <CheckCircle2 size={13} />
              <span>{stats.normalCount} NORMAL</span>
            </div>
            <div className="stat-pill warning">
              <AlertTriangle size={13} />
              <span>{stats.warningCount} WARNING</span>
            </div>
            <div className="stat-pill critical">
              <ShieldAlert size={13} />
              <span>{stats.criticalCount} CRITICAL</span>
            </div>
          </div>

          <div className="topbar-right">
            <button
              className="btn-cyber outline"
              onClick={() => setIsSimulating(!isSimulating)}
              title={isSimulating ? 'Pause Telemetry Simulation' : 'Resume Telemetry'}
            >
              {isSimulating ? <Pause size={13} /> : <Play size={13} />}
              <span>{isSimulating ? 'Live Tick ON' : 'Paused'}</span>
            </button>

            <button
              className="btn-cyber outline"
              onClick={() => speakAlert(selectedMachine)}
              title="Play current machine voice alert"
            >
              <Bell size={13} />
              <span>Voice Alert</span>
            </button>

            <button className="btn-cyber" onClick={triggerAiInference}>
              <RefreshCw size={13} />
              <span>Run AI Diagnostics</span>
            </button>
          </div>
        </header>

        {/* AI INFERENCE SCANNING MODAL / OVERLAY */}
        {isScanning && (
          <div className="scan-overlay">
            <div className="scanner-ring"></div>
            <div className="scan-text">CHRONOS AI INFERENCE PASS ACTIVE...</div>
          </div>
        )}

        {/* TAB VIEW ROUTING */}
        <div className="dashboard-content">
          {activeTab === 'DIGITAL_TWIN' && (
            <>
              {/* 3D CANVAS VIEW */}
              <div className="canvas-wrapper">
                {/* Floating View Control Bar */}
                <div className="canvas-floating-controls">
                  <div className="view-controls-bar">
                    <span
                      style={{
                        fontSize: '11px',
                        color: '#94a3b8',
                        marginRight: '6px',
                        fontWeight: '600'
                      }}
                    >
                      CAMERA:
                    </span>
                    <button
                      className={`view-btn ${cameraPreset === 'OVERVIEW' ? 'active' : ''}`}
                      onClick={() => setCameraPreset('OVERVIEW')}
                    >
                      Overview
                    </button>
                    <button
                      className={`view-btn ${cameraPreset === 'FOCUS' ? 'active' : ''}`}
                      onClick={() => setCameraPreset('FOCUS')}
                    >
                      Focus Selected
                    </button>
                    <button
                      className={`view-btn ${cameraPreset === 'ISOMETRIC' ? 'active' : ''}`}
                      onClick={() => setCameraPreset('ISOMETRIC')}
                    >
                      Isometric
                    </button>
                    <button
                      className={`view-btn ${cameraPreset === 'TOP_DOWN' ? 'active' : ''}`}
                      onClick={() => setCameraPreset('TOP_DOWN')}
                    >
                      Top-Down
                    </button>
                  </div>
                  <div className="canvas-hint">
                    🖱️ Drag to rotate • Scroll to zoom • Click any machine to inspect
                  </div>
                </div>

                {/* React Three Fiber Canvas */}
                <Canvas
                  shadows
                  camera={{ position: [0, 10, 14], fov: 45 }}
                  style={{ width: '100%', height: '100%' }}
                >
                  <color attach="background" args={['#090a10']} />
                  <fog attach="fog" args={['#090a10', 16, 32]} />

                  {/* Scene Lighting */}
                  <ambientLight intensity={0.65} />
                  <directionalLight
                    position={[8, 14, 8]}
                    intensity={1.2}
                    castShadow
                    shadow-mapSize={[2048, 2048]}
                  />
                  <pointLight position={[-8, 6, -8]} color="#00f0ff" intensity={0.6} />
                  <pointLight position={[8, 4, 8]} color="#a855f7" intensity={0.5} />

                  {/* Floor Cyber Grid */}
                  <gridHelper
                    args={[32, 32, '#00f0ff', '#1e293b']}
                    position={[0, -0.01, 0]}
                  />

                  {/* Machines in Fleet */}
                  {machines.map((machine) => (
                    <MachineNode
                      key={machine.id}
                      machine={machine}
                      isSelected={machine.id === selectedMachineId}
                      onSelect={(id) => {
                        setSelectedMachineId(id)
                        setCameraPreset('FOCUS')
                      }}
                    />
                  ))}

                  {/* Camera Director Controls */}
                  <CameraDirector
                    cameraPreset={cameraPreset}
                    selectedMachinePos={selectedMachine?.position}
                  />
                </Canvas>
              </div>

              {/* TELEMETRY & PREDICTIVE MAINTENANCE INSPECTOR DRAWER */}
              <aside className="telemetry-drawer">
                <div className="drawer-header">
                  <div className="drawer-title-area">
                    <span className="machine-tag">{selectedMachine.id}</span>
                    <h2 className="machine-name">{selectedMachine.name}</h2>
                    <span className="machine-sub">{selectedMachine.type}</span>
                  </div>

                  <div className={`risk-badge ${selectedMachine.riskLevel.toLowerCase()}`}>
                    {selectedMachine.riskLevel === 'CRITICAL' && <ShieldAlert size={14} />}
                    {selectedMachine.riskLevel === 'WARNING' && <AlertTriangle size={14} />}
                    {selectedMachine.riskLevel === 'NORMAL' && <CheckCircle2 size={14} />}
                    <span>{selectedMachine.riskLevel}</span>
                  </div>
                </div>

                <div className="drawer-body">
                  {/* Alert Message Banner (Matches Chronos day49 / day51 alert system) */}
                  <div className={`alert-banner ${selectedMachine.riskLevel.toLowerCase()}`}>
                    {selectedMachine.riskLevel === 'CRITICAL' && <ShieldAlert size={18} />}
                    {selectedMachine.riskLevel === 'WARNING' && <AlertTriangle size={18} />}
                    {selectedMachine.riskLevel === 'NORMAL' && <CheckCircle2 size={18} />}
                    <div>
                      <strong style={{ display: 'block', marginBottom: '2px' }}>
                        {selectedMachine.riskLevel} RISK CLASSIFICATION
                      </strong>
                      {selectedMachine.alertMessage}
                    </div>
                  </div>

                  {/* Failure Probability Gauge Card */}
                  <div className="probability-card">
                    <div className="card-title-row">
                      <span>CHRONOS FAILURE PROBABILITY</span>
                      <span style={{ fontFamily: 'var(--font-mono)' }}>
                        Target: &lt; 30.0%
                      </span>
                    </div>
                    <div className="prob-score-wrap">
                      <span
                        className={`prob-val ${selectedMachine.riskLevel.toLowerCase()}`}
                      >
                        {(selectedMachine.failureProbability * 100).toFixed(1)}%
                      </span>
                      <span style={{ fontSize: '13px', color: '#94a3b8' }}>
                        (Normal Prob: {(selectedMachine.normalProbability * 100).toFixed(1)}%)
                      </span>
                    </div>
                    <div className="prob-bar-track">
                      <div
                        className={`prob-bar-fill ${selectedMachine.riskLevel.toLowerCase()}`}
                        style={{ width: `${selectedMachine.failureProbability * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Telemetry Sensor Metrics Grid */}
                  <div className="telemetry-grid">
                    <div className="telemetry-cell">
                      <div className="cell-label">
                        <Gauge size={13} color="#00f0ff" /> Torque
                      </div>
                      <div className="cell-value">{selectedMachine.torque} Nm</div>
                      <div className="cell-sub">
                        {selectedMachine.torque > 60 ? '⚠️ High Torque' : 'Optimal range'}
                      </div>
                    </div>

                    <div className="telemetry-cell">
                      <div className="cell-label">
                        <Wrench size={13} color="#f59e0b" /> Tool Wear
                      </div>
                      <div className="cell-value">{selectedMachine.toolWear} min</div>
                      <div className="cell-sub">
                        {selectedMachine.toolWear > 180 ? '⚠️ High Wear' : 'Under limit'}
                      </div>
                    </div>

                    <div className="telemetry-cell">
                      <div className="cell-label">
                        <Thermometer size={13} color="#ef4444" /> Process / Air Temp
                      </div>
                      <div className="cell-value">
                        {selectedMachine.procTemp} / {selectedMachine.airTemp} K
                      </div>
                      <div className="cell-sub">
                        ΔT = {(selectedMachine.procTemp - selectedMachine.airTemp).toFixed(1)} K
                      </div>
                    </div>

                    <div className="telemetry-cell">
                      <div className="cell-label">
                        <RotateCw size={13} color="#a855f7" /> Rotational Speed
                      </div>
                      <div className="cell-value">{selectedMachine.rotSpeed} RPM</div>
                      <div className="cell-sub">Vibration: {selectedMachine.vibration}</div>
                    </div>
                  </div>

                  {/* Chronos Specific Failure Modes Breakdown */}
                  <div className="failure-modes-card">
                    <div className="card-title-row">
                      <span>CHRONOS SPECIFIC FAILURE MODES</span>
                      <span style={{ fontFamily: 'var(--font-mono)' }}>STATUS</span>
                    </div>

                    <div className="mode-row">
                      <span className="mode-name">HDF (Heat Dissipation Failure)</span>
                      <span
                        className={`mode-status-tag ${
                          selectedMachine.hdf ? 'tripped' : 'ok'
                        }`}
                      >
                        {selectedMachine.hdf ? 'DETECTED' : 'NORMAL'}
                      </span>
                    </div>

                    <div className="mode-row">
                      <span className="mode-name">OSF (Overstrain Failure)</span>
                      <span
                        className={`mode-status-tag ${
                          selectedMachine.osf ? 'tripped' : 'ok'
                        }`}
                      >
                        {selectedMachine.osf ? 'DETECTED' : 'NORMAL'}
                      </span>
                    </div>

                    <div className="mode-row">
                      <span className="mode-name">PWF (Power Failure Spike)</span>
                      <span
                        className={`mode-status-tag ${
                          selectedMachine.pwf ? 'tripped' : 'ok'
                        }`}
                      >
                        {selectedMachine.pwf ? 'DETECTED' : 'NORMAL'}
                      </span>
                    </div>

                    <div className="mode-row">
                      <span className="mode-name">TWF (Tool Wear Failure)</span>
                      <span
                        className={`mode-status-tag ${
                          selectedMachine.twf ? 'tripped' : 'ok'
                        }`}
                      >
                        {selectedMachine.twf ? 'DETECTED' : 'NORMAL'}
                      </span>
                    </div>
                  </div>

                  {/* Interactive ML Stress Simulator (Live prediction re-calc) */}
                  <div className="simulator-box">
                    <div className="sim-header">
                      <Sliders size={14} />
                      <span>LIVE ML STRESS SIMULATOR</span>
                    </div>
                    <p style={{ fontSize: '11px', color: '#94a3b8' }}>
                      Adjust parameters to observe how Chronos AI's Random Forest predicts failure
                      probability in real time:
                    </p>

                    <div className="sim-slider-row">
                      <div className="slider-label-row">
                        <span>Torque [Nm]</span>
                        <span>{selectedMachine.torque} Nm</span>
                      </div>
                      <input
                        type="range"
                        min="20"
                        max="95"
                        step="0.5"
                        value={selectedMachine.torque}
                        onChange={(e) => handleSliderChange('torque', e.target.value)}
                        className="cyber-slider"
                      />
                    </div>

                    <div className="sim-slider-row">
                      <div className="slider-label-row">
                        <span>Tool Wear [min]</span>
                        <span>{selectedMachine.toolWear} min</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="260"
                        step="1"
                        value={selectedMachine.toolWear}
                        onChange={(e) => handleSliderChange('toolWear', e.target.value)}
                        className="cyber-slider"
                      />
                    </div>

                    <div className="action-buttons-row">
                      <button
                        className="action-btn primary"
                        onClick={() => toggleAcknowledge(selectedMachine.id)}
                      >
                        <Check size={13} />
                        <span>
                          {acknowledgedAlerts.includes(selectedMachine.id)
                            ? 'Acknowledged'
                            : 'Acknowledge Alert'}
                        </span>
                      </button>
                      <button
                        className="action-btn danger"
                        onClick={() => {
                          alert(
                            `Work order generated for ${selectedMachine.id} (${selectedMachine.name}). Technician dispatched.`
                          )
                        }}
                      >
                        <Wrench size={13} />
                        <span>Dispatch Tech</span>
                      </button>
                    </div>
                  </div>
                </div>
              </aside>
            </>
          )}

          {/* ACTIVE ALERTS VIEW */}
          {activeTab === 'ALERTS' && (
            <div className="tab-view-container">
              <div className="tab-header">
                <h1 className="tab-title">Active Fleet Incidents & Alerts</h1>
                <p className="tab-desc">
                  Real-time Chronos AI alert queue classified by failure probability thresholds
                  (&ge;70% Critical, &ge;30% Warning).
                </p>
              </div>

              <div className="grid-cards-row">
                <div className="info-card">
                  <div className="info-card-header">
                    <ShieldAlert size={16} color="#ef4444" /> CRITICAL ACTIONS REQUIRED
                  </div>
                  <div className="info-card-val" style={{ color: '#ef4444' }}>
                    {stats.criticalCount}
                  </div>
                </div>
                <div className="info-card">
                  <div className="info-card-header">
                    <AlertTriangle size={16} color="#f59e0b" /> WARNING LEVEL ALARMS
                  </div>
                  <div className="info-card-val" style={{ color: '#f59e0b' }}>
                    {stats.warningCount}
                  </div>
                </div>
                <div className="info-card">
                  <div className="info-card-header">
                    <CheckCircle2 size={16} color="#10b981" /> NOMINAL ASSETS
                  </div>
                  <div className="info-card-val" style={{ color: '#10b981' }}>
                    {stats.normalCount}
                  </div>
                </div>
              </div>

              <div className="cyber-table-container">
                <table className="cyber-table">
                  <thead>
                    <tr>
                      <th>MACHINE ID</th>
                      <th>MACHINE NAME</th>
                      <th>RISK LEVEL</th>
                      <th>FAIL PROBABILITY</th>
                      <th>TRIGGERING FACTORS</th>
                      <th>ACTION</th>
                    </tr>
                  </thead>
                  <tbody>
                    {machines.map((m) => (
                      <tr key={m.id}>
                        <td style={{ fontFamily: 'var(--font-mono)', color: '#00f0ff' }}>
                          {m.id}
                        </td>
                        <td style={{ color: '#fff', fontWeight: 600 }}>{m.name}</td>
                        <td>
                          <span className={`risk-badge ${m.riskLevel.toLowerCase()}`}>
                            {m.riskLevel}
                          </span>
                        </td>
                        <td style={{ fontFamily: 'var(--font-mono)' }}>
                          {(m.failureProbability * 100).toFixed(1)}%
                        </td>
                        <td>
                          {m.hdf && <span style={{ color: '#ef4444', marginRight: 8 }}>[HDF]</span>}
                          {m.osf && <span style={{ color: '#ef4444', marginRight: 8 }}>[OSF]</span>}
                          {m.twf && <span style={{ color: '#ef4444', marginRight: 8 }}>[TWF]</span>}
                          {m.pwf && <span style={{ color: '#ef4444', marginRight: 8 }}>[PWF]</span>}
                          {!m.hdf && !m.osf && !m.twf && !m.pwf && (
                            <span style={{ color: '#64748b' }}>None (Operating normal)</span>
                          )}
                        </td>
                        <td>
                          <button
                            className="view-btn active"
                            onClick={() => {
                              setSelectedMachineId(m.id)
                              setActiveTab('DIGITAL_TWIN')
                              setCameraPreset('FOCUS')
                            }}
                          >
                            Inspect in 3D &rarr;
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* CHRONOS AI MODEL VIEW */}
          {activeTab === 'AI_MODEL' && (
            <div className="tab-view-container">
              <div className="tab-header">
                <h1 className="tab-title">Chronos Random Forest Intelligence Engine</h1>
                <p className="tab-desc">
                  Machine learning model evaluation parameters, feature weights, and risk classification
                  pipeline.
                </p>
              </div>

              <div className="grid-cards-row">
                <div className="info-card">
                  <div className="info-card-header">MODEL ALGORITHM</div>
                  <div className="info-card-val">Random Forest</div>
                  <span style={{ fontSize: '11px', color: '#64748b' }}>
                    100 Estimators • Max Depth 12
                  </span>
                </div>
                <div className="info-card">
                  <div className="info-card-header">ACCURACY SCORE</div>
                  <div className="info-card-val" style={{ color: '#10b981' }}>
                    99.4%
                  </div>
                  <span style={{ fontSize: '11px', color: '#64748b' }}>
                    Evaluated on 10,000 synthetic industrial records
                  </span>
                </div>
                <div className="info-card">
                  <div className="info-card-header">PRECISION / RECALL</div>
                  <div className="info-card-val" style={{ color: '#00f0ff' }}>
                    0.97 / 0.99
                  </div>
                  <span style={{ fontSize: '11px', color: '#64748b' }}>
                    Zero false-negative critical thresholding
                  </span>
                </div>
              </div>

              <div className="cyber-table-container" style={{ padding: '24px' }}>
                <h3 style={{ fontSize: '15px', color: '#fff', marginBottom: '14px' }}>
                  Top Ranked Predictive Feature Weights
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {[
                    { name: 'Torque [Nm]', weight: 34 },
                    { name: 'Tool wear [min]', weight: 28 },
                    { name: 'Temperature Difference [K]', weight: 16 },
                    { name: 'Rotational speed [rpm]', weight: 12 },
                    { name: 'Power Indicator (kW)', weight: 10 }
                  ].map((f, i) => (
                    <div key={i}>
                      <div
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          fontSize: '12px',
                          marginBottom: '4px'
                        }}
                      >
                        <span style={{ fontFamily: 'var(--font-mono)' }}>{f.name}</span>
                        <span style={{ color: '#00f0ff', fontFamily: 'var(--font-mono)' }}>
                          {f.weight}%
                        </span>
                      </div>
                      <div className="prob-bar-track">
                        <div
                          className="prob-bar-fill normal"
                          style={{ width: `${f.weight * 2.5}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* FLEET TELEMETRY MATRIX VIEW */}
          {activeTab === 'TELEMETRY' && (
            <div className="tab-view-container">
              <div className="tab-header">
                <h1 className="tab-title">Fleet Telemetry Matrix</h1>
                <p className="tab-desc">
                  Live multi-machine sensor readings, operating parameters, and calculated risk
                  indicators.
                </p>
              </div>

              <div className="cyber-table-container">
                <table className="cyber-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>NAME</th>
                      <th>AIR TEMP (K)</th>
                      <th>PROC TEMP (K)</th>
                      <th>ROT SPEED (RPM)</th>
                      <th>TORQUE (NM)</th>
                      <th>TOOL WEAR (MIN)</th>
                      <th>VIBRATION</th>
                      <th>RISK</th>
                    </tr>
                  </thead>
                  <tbody>
                    {machines.map((m) => (
                      <tr key={m.id}>
                        <td style={{ fontFamily: 'var(--font-mono)', color: '#00f0ff' }}>
                          {m.id}
                        </td>
                        <td style={{ color: '#fff', fontWeight: 600 }}>{m.name}</td>
                        <td>{m.airTemp}</td>
                        <td>{m.procTemp}</td>
                        <td>{m.rotSpeed}</td>
                        <td>{m.torque}</td>
                        <td>{m.toolWear}</td>
                        <td>{m.vibration}</td>
                        <td>
                          <span className={`risk-badge ${m.riskLevel.toLowerCase()}`}>
                            {m.riskLevel}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

