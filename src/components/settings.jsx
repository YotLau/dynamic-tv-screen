import { useState } from 'react';
import { Button, TextField, Box, Alert, IconButton } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import DirectoryPicker from './directorypicker';

const Settings = ({ onDirectorySelect }) => {
  const [tvIp, setTvIp] = useState(localStorage.getItem('tvIp') || '');
  const [testStatus, setTestStatus] = useState(null); // null, 'success', 'error'
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const handleTvIpChange = (event) => {
    const newIp = event.target.value;
    setTvIp(newIp);
    localStorage.setItem('tvIp', newIp);
    setTestStatus(null); // Reset test status when IP changes
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      setError('');
      localStorage.setItem('tvIp', tvIp);
      setTestStatus(null); // Reset test status when saving
      
      // Test the connection before saving
      const response = await fetch('/api/test-tv-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tvIp }),
      });

      const data = await response.json();
      if (data.success) {
        setTestStatus('success');
        setError('');
      } else {
        throw new Error(data.error || 'Failed to connect to TV');
      }
    } catch (error) {
      setTestStatus('error');
      setError('Failed to save settings: ' + error.message);
    } finally {
      setIsSaving(false);
    }
  };

  const testTvConnection = async () => {
    try {
      setError('');
      setTestStatus('testing');
      
      // Validate IP address format
      const ipRegex = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
      if (!ipRegex.test(tvIp)) {
        setTestStatus('error');
        setError('Invalid IP address format. Please enter a valid IP address (e.g., 192.168.1.100)');
        return;
      }

      const response = await fetch('/api/test-tv-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tvIp }),
      });

      const data = await response.json();
      if (data.success) {
        setTestStatus('success');
        setError('');
      } else {
        setTestStatus('error');
        const errorMessage = data.error || 'Failed to connect to TV';
        setError(`Connection failed: ${errorMessage}. Please ensure:\n- The TV is powered on\n- The TV is connected to the same network\n- The IP address is correct`);
      }
    } catch (error) {
      setTestStatus('error');
      setError('Network error: Unable to reach the TV. Please check your network connection and try again.');
    }
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 600, mx: 'auto', p: 3 }}>
      <DirectoryPicker onDirectorySelect={onDirectorySelect} />
      
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
        <TextField
          label="TV IP Address"
          value={tvIp}
          onChange={handleTvIpChange}
          fullWidth
          variant="outlined"
          placeholder="e.g. 192.168.1.100"
          error={testStatus === 'error'}
        />
        <Button
          variant="contained"
          onClick={handleSave}
          sx={{ minWidth: 100 }}
        >
          Save
        </Button>
        <Button
          variant="outlined"
          onClick={testTvConnection}
          sx={{ minWidth: 100, display: 'flex', gap: 1, alignItems: 'center' }}
          startIcon={<CheckCircleIcon />}
        >
          Ping TV
        </Button>
        {testStatus === 'success' && (
          <IconButton color="success" sx={{ p: 0 }}>
            <CheckCircleIcon />
          </IconButton>
        )}
        {testStatus === 'error' && (
          <IconButton color="error" sx={{ p: 0 }}>
            <ErrorIcon />
          </IconButton>
        )}
      </Box>
      
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default Settings;