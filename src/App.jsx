import { useState } from 'react'
import { Box, Container, Typography, Button, TextField, Paper, LinearProgress, Stack, IconButton, Snackbar, Alert, CircularProgress } from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import Brightness4Icon from '@mui/icons-material/Brightness4'
import Brightness7Icon from '@mui/icons-material/Brightness7'
import SettingsIcon from '@mui/icons-material/Settings'
import { useNavigate } from 'react-router-dom'
import ImageGallery from './components/ImageGallery'
import axios from 'axios'

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

// Configure axios
const api = axios.create({
  baseURL: '',  // Empty baseURL to use relative paths with proxy
  timeout: 60000,  // Increased timeout to 60 seconds
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

function App() {
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [status, setStatus] = useState('Ready')
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [imageUrl, setImageUrl] = useState(null)
  const [mode, setMode] = useState('dark')
  const [tvIp, setTvIp] = useState(localStorage.getItem('tvIp') || '')
  const [imageFolder, setImageFolder] = useState(localStorage.getItem('imageFolder') || '')
  const navigate = useNavigate()

  const theme = getTheme(mode)

  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'))
  }

  const handleSettingsOpen = () => {
    navigate('/settings')
  }

  const handleFolderSelect = async () => {
    try {
      setLoading(true)
      setStatus('Opening folder selection dialog...')
      const response = await api.post('/api/select-folder', null, {
        timeout: 120000 // Increase timeout to 2 minutes for folder selection
      })
      if (response.data.success) {
        setImageFolder(response.data.folderPath)
        localStorage.setItem('imageFolder', response.data.folderPath)
        setStatus('Folder selected successfully!')
        window.location.reload() // Reload to refresh the image gallery
      } else {
        throw new Error(response.data.error || 'Failed to select folder')
      }
    } catch (error) {
      const errorMessage = error.code === 'ECONNABORTED' 
        ? 'Folder selection timed out. Please try again.'
        : error.response?.data?.error || error.message || 'Failed to select folder'
      setStatus(`Error: ${errorMessage}`)
    } finally {
      setLoading(false)
    }
  }

  const handleError = (error) => {
    console.error('API Error:', error);
    const errorMessage = error.response?.data?.error || error.message || 'An unknown error occurred';
    setStatus(`Error: ${errorMessage}`);
    return errorMessage;
  };

  const generatePrompt = async () => {
    try {
      setLoading(true)
      setStatus('Generating prompt...')
      const response = await api.post('/api/generate-prompt')
      console.log('Prompt response:', response.data)
      if (response.data.success) {
        setPrompt(response.data.prompt)
        setStatus('Prompt generated successfully!')
      } else {
        throw new Error(response.data.error || 'Failed to generate prompt')
      }
    } catch (error) {
      handleError(error);
      setPrompt('')
    } finally {
      setLoading(false)
    }
  }

  const generateImage = async () => {
    try {
      if (!prompt) {
        throw new Error('Please generate a prompt first')
      }
      setLoading(true)
      setStatus('Generating image...')
      const response = await api.post('/api/generate-image', { prompt })
      console.log('Image response:', response.data)
      if (response.data.success) {
        setImageUrl(response.data.imageUrl)
        setStatus('Image generated successfully!')
      } else {
        throw new Error(response.data.error || 'Failed to generate image')
      }
    } catch (error) {
      handleError(error);
      setImageUrl(null)
    } finally {
      setLoading(false)
    }
  }

  const pushToTV = async () => {
    try {
      if (!imageUrl) {
        throw new Error('No image available to push')
      }

      if (!tvIp) {
        throw new Error('TV IP address is required. Please set it in Settings.')
      }
      
      setLoading(true)
      setUploadSuccess(false)
      setStatus('Pushing image to TV...')
      const response = await api.post('/api/push-to-tv', {
        imageUrl: imageUrl,
        tvIp: tvIp
      })
      console.log('TV push response:', response.data)
      if (response.data.success) {
        setStatus('Image successfully pushed to TV!')
        setUploadSuccess(true)
      } else {
        throw new Error(response.data.error || 'Failed to push to TV')
      }
    } catch (error) {
      handleError(error);
    } finally {
      setLoading(false)
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', color: 'text.primary' }}>
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', py: 3 }}>
            <Typography variant="h4" component="h1">Dynamic TV Screen</Typography>
            <Box>
              <IconButton onClick={handleSettingsOpen} color="inherit" sx={{ mr: 1 }}>
                <SettingsIcon />
              </IconButton>
              <IconButton onClick={toggleTheme} color="inherit">
                {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
              </IconButton>
            </Box>
          </Box>



          <Paper sx={{ p: 3, mb: 3 }}>
            <Stack spacing={2}>
              <Box>
                <Button
                  variant="contained"
                  onClick={generatePrompt}
                  disabled={loading}
                  sx={{ mr: 2 }}
                >
                  Generate Prompt
                </Button>
                <Button
                  variant="contained"
                  onClick={generateImage}
                  disabled={loading}
                  sx={{ mr: 2 }}
                >
                  Generate Image
                </Button>
                <Button
                  variant="contained"
                  onClick={pushToTV}
                  disabled={loading || !imageUrl}
                >
                  {loading ? 'Pushing to TV...' : 'Push to TV'}
                </Button>
              </Box>

              {loading && (
                <Box sx={{ width: '100%' }}>
                  <LinearProgress />
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {status}
                  </Typography>
                </Box>
              )}

              <Snackbar
                open={uploadSuccess}
                autoHideDuration={6000}
                onClose={() => setUploadSuccess(false)}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
              >
                <Alert onClose={() => setUploadSuccess(false)} severity="success" sx={{ width: '100%' }}>
                  Image successfully uploaded to TV!
                </Alert>
              </Snackbar>

              <TextField
                label="Generated Prompt"
                multiline
                rows={4}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                fullWidth
                disabled={loading}
              />

              {imageUrl && (
                <Box sx={{ mt: 2 }}>
                  <img
                    src={imageUrl}
                    alt="Generated artwork"
                    style={{ maxWidth: '100%', height: 'auto' }}
                  />
                </Box>
              )}

              <Typography variant="body1">
                Status: {status}
              </Typography>
            </Stack>
          </Paper>
          <ImageGallery />
        </Container>
      </Box>
    </ThemeProvider>
  )
}

export default App