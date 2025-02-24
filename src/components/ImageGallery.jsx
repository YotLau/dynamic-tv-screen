import { useState, useEffect } from 'react';
import { Grid, Card, CardMedia, Typography, Box, IconButton, Snackbar, Alert } from '@mui/material';
import UploadIcon from '@mui/icons-material/Upload';
import axios from 'axios';

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

  useEffect(() => {
    const fetchLocalImages = async () => {
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

    fetchLocalImages();
  }, []);

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

      // Always consider it a success if we get a response, even with TV selection message
      if (response.data.success || response.data.error?.includes('Failed to select image on TV')) {
        setUploadSuccess(true);
        setError(null); // Clear any previous errors on success
      } else {
        throw new Error(response.data.error || 'Failed to push to TV');
      }
    } catch (error) {
      console.error('Error uploading to TV:', error);
      setError(error.response?.data?.error || error.message || 'An unknown error occurred');
      setUploadSuccess(false); // Ensure upload success is false on error
    } finally {
      setUploading(false);
    }
  };

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">Error: {error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
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
                sx={{ objectFit: 'cover' }}
              />
              {hoveredIndex === index && (
                <Box
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    bgcolor: 'rgba(0, 0, 0, 0.5)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  <IconButton
                    onClick={() => handleUploadToTV(image)}
                    disabled={uploading}
                    sx={{
                      color: 'white',
                      '&:hover': {
                        bgcolor: 'rgba(255, 255, 255, 0.2)'
                      }
                    }}
                  >
                    <UploadIcon />
                  </IconButton>
                </Box>
              )}
            </Card>
          </Grid>
        ))}
      </Grid>
      {localImages.length === 0 && (
        <Typography variant="body1" sx={{ mt: 2 }}>
          No images found in the gallery.
        </Typography>
      )}
      {error && (
        <Box sx={{ p: 3 }}>
          <Typography color="error">Error: {error}</Typography>
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
    </Box>
  );
};

export default ImageGallery;