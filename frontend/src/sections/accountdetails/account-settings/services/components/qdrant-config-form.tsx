import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';

import { alpha, useTheme } from '@mui/material/styles';
import {
  Box,
  Grid,
  Alert,
  Button,
  TextField,
  Typography,
  InputAdornment,
  CircularProgress,
} from '@mui/material';

import { Iconify } from 'src/components/iconify';

import { getQdrantConfig, updateQdrantConfig } from '../utils/services-configuration-service';

interface QdrantConfigFormProps {
  onValidationChange: (isValid: boolean) => void;
  onSaveSuccess?: () => void;
}

export interface QdrantConfigFormRef {
  handleSave: () => Promise<void>;
}

const QdrantConfigForm = forwardRef<QdrantConfigFormRef, QdrantConfigFormProps>(
  ({ onValidationChange, onSaveSuccess }, ref) => {
    const theme = useTheme();
    const [formData, setFormData] = useState({
      host: '',
      grpcPort: '',
      apiKey: '',
    });

    const [errors, setErrors] = useState({
      host: '',
      grpcPort: '',
      apiKey: '',
    });

    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [saveError, setSaveError] = useState<string | null>(null);
    const [isEditing, setIsEditing] = useState(false);
    const [originalData, setOriginalData] = useState({
      host: '',
      grpcPort: '',
      apiKey: '',
    });

    // Expose the handleSave method to the parent component
    useImperativeHandle(ref, () => ({
      handleSave: async () => {
        await handleSave();
      },
    }));

    // Load existing config on mount
    useEffect(() => {
      const fetchConfig = async () => {
        setIsLoading(true);
        try {
          const config = await getQdrantConfig();

          const data = {
            host: config?.host || '',
            grpcPort: config?.grpcPort || '',
            apiKey: config?.apiKey || '',
          };

          setFormData(data);
          setOriginalData(data);
        } catch (error) {
          console.error('Failed to load Qdrant config:', error);
        } finally {
          setIsLoading(false);
        }
      };

      fetchConfig();
    }, []);

    // Validate form and notify parent
    useEffect(() => {
      const isValid =
        formData.host.trim() !== '' &&
        formData.grpcPort.trim() !== '' &&
        !errors.host &&
        !errors.grpcPort &&
        !errors.apiKey;

      // Only notify about validation if in edit mode and form has changes
      const hasChanges =
        formData.host !== originalData.host ||
        formData.grpcPort !== originalData.grpcPort ||
        formData.apiKey !== originalData.apiKey;

      onValidationChange(isValid && isEditing && hasChanges);
    }, [formData, errors, onValidationChange, isEditing, originalData]);

    // Handle input change
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const { name, value } = e.target;

      setFormData({
        ...formData,
        [name]: value,
      });

      // Validate
      validateField(name, value);
    };

    // Handle edit mode toggle
    const handleToggleEdit = () => {
      if (isEditing) {
        // Cancel edit - revert to original data
        setFormData(originalData);
        setErrors({
          host: '',
          grpcPort: '',
          apiKey: '',
        });
      }
      setIsEditing(!isEditing);
    };

    // Field validation
    const validateField = (name: string, value: string) => {
      let error = '';

      if ((name === 'host' || name === 'grpcPort') && value.trim() === '') {
        error = 'This field is required';
      } else if (name === 'grpcPort' && !/^\d+$/.test(value)) {
        error = 'Port must be a number';
      } else if (name === 'grpcPort' && (parseInt(value, 10) <= 0 || parseInt(value, 10) > 65535)) {
        error = 'Port must be between 1 and 65535';
      } else if (name === 'apiKey' && value.trim() !== '' && value.length < 16) {
        error = 'API key should be at least 16 characters';
      }

      setErrors({
        ...errors,
        [name]: error,
      });
    };

    // Handle save
    const handleSave = async () => {
      setIsSaving(true);
      setSaveError(null);

      try {
        await updateQdrantConfig({
          host: formData.host,
          grpcPort: formData.grpcPort,
          apiKey: formData.apiKey,
        });

        // Update original data after successful save
        setOriginalData({
          host: formData.host,
          grpcPort: formData.grpcPort,
          apiKey: formData.apiKey,
        });

        // Exit edit mode
        setIsEditing(false);

        if (onSaveSuccess) {
          onSaveSuccess();
        }

        return true;
      } catch (error) {
        setSaveError('Failed to save Qdrant configuration');
        console.error('Error saving Qdrant config:', error);
        return false;
      } finally {
        setIsSaving(false);
      }
    };

    if (isLoading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress size={24} />
        </Box>
      );
    }

    return (
      <>
        {saveError && (
          <Alert
            severity="error"
            sx={{
              mb: 3,
              borderRadius: 1,
            }}
          >
            {saveError}
          </Alert>
        )}

        <Box
          sx={{
            mb: 3,
            p: 2,
            borderRadius: 1,
            bgcolor: alpha(theme.palette.info.main, 0.04),
            border: `1px solid ${alpha(theme.palette.info.main, 0.15)}`,
            display: 'flex',
            alignItems: 'flex-start',
            gap: 1,
          }}
        >
          <Iconify
            icon="mdi:information-outline"
            width={20}
            height={20}
            color={theme.palette.info.main}
            style={{ marginTop: 2 }}
          />
          <Box>
            <Typography variant="body2" color="text.secondary">
              Qdrant connection details. Enter the host, gRPC port, and optional API key for
              connecting to the Qdrant service.
            </Typography>
          </Box>
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
          <Button
            onClick={handleToggleEdit}
            startIcon={<Iconify icon={isEditing ? 'mdi:close' : 'mdi:pencil'} />}
            color={isEditing ? 'error' : 'primary'}
            size="small"
          >
            {isEditing ? 'Cancel' : 'Edit'}
          </Button>
        </Box>

        <Grid container spacing={2.5}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Host"
              name="host"
              value={formData.host}
              onChange={handleChange}
              placeholder="qdrant-service.example.com"
              error={Boolean(errors.host)}
              helperText={errors.host || 'Hostname or IP address of the Qdrant service'}
              required
              size="small"
              disabled={!isEditing}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Iconify icon="mdi:server" width={18} height={18} />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: alpha(theme.palette.text.primary, 0.15),
                  },
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="gRPC Port"
              name="grpcPort"
              value={formData.grpcPort}
              onChange={handleChange}
              placeholder="50051"
              error={Boolean(errors.grpcPort)}
              helperText={errors.grpcPort || 'Port for gRPC communication'}
              required
              size="small"
              type="number"
              disabled={!isEditing}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Iconify icon="mdi:pound" width={18} height={18} />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: alpha(theme.palette.text.primary, 0.15),
                  },
                },
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="API Key (optional)"
              name="apiKey"
              value={formData.apiKey}
              onChange={handleChange}
              type="password"
              error={Boolean(errors.apiKey)}
              helperText={
                errors.apiKey || 'Authentication key for the Qdrant service (if required)'
              }
              size="small"
              disabled={!isEditing}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Iconify icon="mdi:key" width={18} height={18} />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: alpha(theme.palette.text.primary, 0.15),
                  },
                },
              }}
            />
          </Grid>
        </Grid>

        {isSaving && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <CircularProgress size={24} />
          </Box>
        )}
      </>
    );
  }
);

export default QdrantConfigForm;
