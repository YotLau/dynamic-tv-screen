import { useState } from 'react'
import { Box, Container, Typography, Button, TextField, Stack, Alert, CircularProgress, IconButton, Paper } from '@mui/material'
import CheckIcon from '@mui/icons-material/Check'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import DirectoryPicker from './components/DirectoryPicker'

const api = axios.create({
  baseURL: '',  // relative paths with proxy
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

const getTheme = (mode) => createTheme({
  palette: {
    mode,
    primary: {
      main: '#3b82f6',
    },
    background: {
      default: mode === 'dark' ? '#1a1a1a' : '#f5f5f5',
      paper: mode === 'dark' ? '#2d2d2d' : '#ffffff',
    },
  },
})

export default function Settings() {
  const [tvIp, setTvIp] = useState(localStorage.getItem('tvIp') || '')
  const [imageFolder, setImageFolder] = useState(localStorage.getItem('imageFolder') || '')
  const [checkingTv, setCheckingTv] = useState(false)
  const [tvCheckResult, setTvCheckResult] = useState(null)
  const [status, setStatus] = useState('Ready')
  const [mode, setMode] = useState(localStorage.getItem('themeMode') || 'dark')
  const navigate = useNavigate()
  
  const theme = getTheme(mode)

  const handleCheckTvIp = async () => {
    if (!tvIp) {
      setStatus('Please enter TV IP address first')
      return
    }
    setCheckingTv(true)
    setTvCheckResult(null)
    try {
      const response = await api.post('/api/check-tv-ip', { tvIp })
      setTvCheckResult(response.data.success)
      setStatus(response.data.success ? 'TV connection successful!' : 'TV connection failed')
    } catch (error) {
      setTvCheckResult(false)
      setStatus('TV connection failed')
    } finally {
      setCheckingTv(false)
    }
  }

  const handleSave = async () => {
    localStorage.setItem('tvIp', tvIp)
    localStorage.setItem('imageFolder', imageFolder)
    try {
      await api.post('/api/save-settings', { tvIp, imageFolder })
    } catch (error) {
      console.error('Save settings error:', error)
    }
    navigate('/')  // go back home
  }

  const handleDirectorySelect = (path) => {
    setImageFolder(path)
    localStorage.setItem('imageFolder', path)
  }

  const handleBack = () => {
    navigate('/')
  }

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', color: 'text.primary' }}>
        <Container maxWidth="sm" sx={{ pt: 4, pb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <IconButton onClick={handleBack} sx={{ mr: 2 }}>
              <ArrowBackIcon />
            </IconButton>
            <Typography variant="h4" component="h1">Settings</Typography>
          </Box>
          
          <Paper sx={{ p: 3 }}>
            <Stack spacing={3}>
        <TextField
          label="TV IP Address"
          type="text"
          fullWidth
          value={tvIp}
          onChange={(e) => setTvIp(e.target.value)}
          helperText="Enter your Samsung TV's local IP address"
          error={tvCheckResult === false}
        />
        <Button
          onClick={handleCheckTvIp}
          variant="outlined"
          disabled={checkingTv || !tvIp}
          startIcon={checkingTv ? <CircularProgress size={20} /> : <CheckIcon />}
          fullWidth
        >
          Check IP
        </Button>
        {tvCheckResult !== null && (
          <Alert severity={tvCheckResult ? "success" : "error"}>
            {tvCheckResult ? "TV connection successful!" : "TV connection failed"}
          </Alert>
        )}
        <TextField
          label="Image Folder"
          type="text"
          fullWidth
          value={imageFolder}
          onChange={(e) => setImageFolder(e.target.value)}
          helperText="Path to store images"
        />
        <Button onClick={handleSave} variant="contained" disabled={tvCheckResult === false}>
          Save Settings
        </Button>
        <Typography variant="body2" color="text.secondary">
          Status: {status}
        </Typography>
            </Stack>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  )
}
