import { useState, useEffect } from 'react';
import { Button, Typography, Box, Alert } from '@mui/material';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';

const DirectoryPicker = ({ onDirectorySelect }) => {
  const [selectedDirectory, setSelectedDirectory] = useState(
    localStorage.getItem('imageFolder') || ''
  );
  const [error, setError] = useState('');
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    // Check if the File System Access API is supported
    if (!('showDirectoryPicker' in window)) {
      setIsSupported(false);
      setError('Your browser does not support directory selection. Please use a modern browser like Chrome or Edge.');
    }
  }, []);

  const handleDirectorySelect = async () => {
    try {
      setError('');
      const directoryHandle = await window.showDirectoryPicker();
      const directoryPath = directoryHandle.name;
      
      localStorage.setItem('imageFolder', directoryPath);
      setSelectedDirectory(directoryPath);
      
      if (onDirectorySelect) {
        onDirectorySelect(directoryPath);
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        // User cancelled the selection
        return;
      }
      console.error('Error selecting directory:', error);
      setError('Failed to select directory. Please try again.');
    }
  };

  return (
    <Box sx={{ mb: 3 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      <Button
        variant="contained"
        startIcon={<FolderOpenIcon />}
        onClick={handleDirectorySelect}
        sx={{ mb: 1 }}
        disabled={!isSupported}
      >
        Select Images Directory
      </Button>
      {selectedDirectory && (
        <Typography variant="body2" color="text.secondary">
          Selected directory: {selectedDirectory}
        </Typography>
      )}
    </Box>
  );
};

export default DirectoryPicker;