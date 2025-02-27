import { useState, useEffect } from 'react';
import { Grid, Card, CardMedia, Typography, Box, IconButton, Snackbar, Alert } from '@mui/material';
import UploadIcon from '@mui/icons-material/Upload';
import axios from 'axios';
import DirectoryPicker from './DirectoryPicker';

const api = axios.create({
  baseURL: '',  // Empty baseURL to use relative paths with proxy
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

const ImageGallery = () => {
  const [localImages, setLocalImages] = useState([]);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [hoveredIndex, setHoveredIndex] = useState(null);

  const fetchLocalImages = async () => {
    const imageFolder = localStorage.getItem('imageFolder');
    if (!imageFolder) {
      // Don't fetch images if no folder is selected
      setLocalImages([]);
      return;
    }

    try {
      const response = await api.get('/api/list-local-images');
      if (response.data.success) {
        setLocalImages(response.data.images.map(image => `${api.defaults.baseURL}/images/${image}`));
      } else {
        throw new Error(response.data.error || 'Failed to fetch local images');
      }
    } catch (error) {
      console.error('Error fetching local images:', error);
      setError(error.message);
    }
  };

  useEffect(() => {
    fetchLocalImages();
  }, []);

  const handleDirectorySelect = async (directoryPath) => {
    // Refresh images after directory selection
    await fetchLocalImages();
  };

  const handleUploadToTV = async (imageUrl) => {
    const tvIp = localStorage.getItem('tvIp');
    if (!tvIp) {
      setError('TV IP address is required. Please set it in Settings.');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      const response = await api.post('/api/push-to-tv', {
        imageUrl,
        tvIp
      });

      if (response.data.success || response.data.error?.includes('Failed to select image on TV')) {
        setUploadSuccess(true);
        setError(null);
      } else {
        throw new Error(response.data.error || 'Failed to push to TV');
      }
    } catch (error) {
      console.error('Error uploading to TV:', error);
      setError(error.response?.data?.error || error.message || 'An unknown error occurred');
      setUploadSuccess(false);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <DirectoryPicker onDirectorySelect={handleDirectorySelect} />
      {error ? (
        <Typography color="error">Error: {error}</Typography>
      ) : (
        <Grid container spacing={3}>
          {localImages.map((image, index) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
              <Card
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
                sx={{ position: 'relative' }}
              >
                <CardMedia
                  component="img"
                  height="200"
                  image={image}
                  alt={`Generated image ${index + 1}`}
                />
                {hoveredIndex === index && (
                  <IconButton
                    onClick={() => handleUploadToTV(image)}
                    disabled={uploading}
                    sx={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      transform: 'translate(-50%, -50%)',
                      backgroundColor: 'rgba(255, 255, 255, 0.8)',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)'
                      }
                    }}
                  >
                    <UploadIcon />
                  </IconButton>
                )}
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      <Snackbar
        open={uploadSuccess}
        autoHideDuration={6000}
        onClose={() => setUploadSuccess(false)}
      >
        <Alert severity="success" sx={{ width: '100%' }}>
          Image successfully pushed to TV!
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ImageGallery;