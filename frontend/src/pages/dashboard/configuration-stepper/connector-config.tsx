import { z } from 'zod';
import axios from 'src/utils/axios';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import React, { useMemo, useState, useEffect, useCallback } from 'react';

import {
  Box,
  Fade,
  Grid,
  alpha,
  Button,
  useTheme,
  TextField,
  Typography,
  FormHelperText,
  CircularProgress,
  Paper,
  Divider,
  Chip,
  Card,
  CardContent,
  Stack,
  InputAdornment,
  Tooltip,
  Alert,
} from '@mui/material';
import scrollableContainerStyle from 'src/sections/qna/chatbot/utils/styles/scrollbar';

import { Iconify } from 'src/components/iconify';
import { useAuthContext } from 'src/auth/hooks';
import type { ConnectorFormValues } from './types';

const getCurrentRedirectUri = () => {
  const currentUrl = new URL(window.location.href);
  currentUrl.hash = '';
  currentUrl.search = '';
  const currentUri = currentUrl.toString();
  const currentRedirectUri = currentUri.endsWith('/')
    ? `${currentUri}account/individual/settings/connector/googleWorkspace`
    : `${currentUri}/account/individual/settings/connector/googleWorkspace`;

  return currentRedirectUri;
};
const getRedirectUris = async () => {
  // Get the current window URL without hash and search parameters

  const currentWindowLocation = getCurrentRedirectUri();

  // Get the frontend URL from the backend
  try {
    const response = await axios.get(`/api/v1/configurationManager/frontendPublicUrl`);
    const frontendBaseUrl = response.data.url;
    // Ensure the URL ends with a slash if needed
    const frontendUrl = frontendBaseUrl.endsWith('/')
      ? `${frontendBaseUrl}account/individual/settings/connector/googleWorkspace`
      : `${frontendBaseUrl}/account/individual/settings/connector/googleWorkspace`;

    return {
      currentWindowLocation,
      recommendedRedirectUri: frontendUrl,
      urisMismatch: currentWindowLocation !== frontendUrl,
    };
  } catch (error) {
    console.error('Error fetching frontend URL:', error);
    return {
      currentWindowLocation,
      recommendedRedirectUri: currentWindowLocation,
      urisMismatch: false,
    };
  }
};

// Updated schema for business accounts to include admin email field
const businessConnectorSchema = z.object({
  googleWorkspace: z.object({
    serviceCredentials: z.string().min(1, 'Service credentials are required'),
    clientId: z.string().optional(),
    clientEmail: z.string().optional(),
    privateKey: z.string().optional(),
    projectId: z.string().optional(),
    adminEmail: z.string().email('Invalid email address').min(1, 'Admin email is required'),
  }),
});

const individualConnectorSchema = z.object({
  googleWorkspace: z.object({
    clientId: z.string().min(1, 'Client ID is required'),
    clientSecret: z.string().min(1, 'Client Secret is required'),
  }),
});

// Constants remain unchanged
const FILE_SIZE_LIMIT = 5 * 1024 * 1024;
const ALLOWED_FILE_TYPES = ['application/json'];
const ALLOWED_FILE_EXTENSIONS = ['.json'];

interface ConnectorConfigStepProps {
  onSubmit: (data: ConnectorFormValues, file: File | null) => void;
  onSkip: () => void;
  initialValues: ConnectorFormValues | null;
  initialFile: File | null;
  setMessage: (message: string) => void;
}

const ConnectorConfigStep: React.FC<ConnectorConfigStepProps> = ({
  onSubmit,
  onSkip,
  initialValues,
  initialFile,
  setMessage,
}) => {
  const theme = useTheme();
  const [redirectUris, setRedirectUris] = useState<{
    currentWindowLocation: string;
    recommendedRedirectUri: string;
    urisMismatch: boolean;
  } | null>(null);
  const { user } = useAuthContext();
  const accountType = user?.accountType || 'individual';

  const [serviceCredentialsFile, setServiceCredentialsFile] = useState<File | null>(null);
  const [parsedJsonData, setParsedJsonData] = useState<any>(null);
  const [credentialsError, setCredentialsError] = useState<string>('');
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [formPartiallyFilled, setFormPartiallyFilled] = useState<boolean>(false);

  // Form for business accounts (file upload with extracted fields)
  const businessForm = useForm<any>({
    resolver: zodResolver(businessConnectorSchema),
    mode: 'onChange',
    defaultValues: {
      googleWorkspace: {
        serviceCredentials: '',
        clientId: '',
        clientEmail: '',
        privateKey: '',
        projectId: '',
        adminEmail: '',
      },
    },
  });

  // Form for individual accounts (always visible)
  const individualForm = useForm<any>({
    resolver: zodResolver(individualConnectorSchema),
    mode: 'onChange',
    defaultValues: {
      googleWorkspace: {
        clientId: '',
        clientSecret: '',
        redirectUri: redirectUris?.recommendedRedirectUri || getCurrentRedirectUri(),
      },
    },
  });

  // First useEffect to fetch redirect URIs and update form
  useEffect(() => {
    const initializeForm = async () => {
      // Get redirect URIs info
      const uris = await getRedirectUris();
      setRedirectUris(uris);

      // Update the existing individualForm with the new redirectUri
      individualForm.setValue(
        'googleWorkspace.redirectUri',
        uris?.recommendedRedirectUri || getCurrentRedirectUri()
      );
    };

    initializeForm();
  }, [individualForm]);

  // Determine which form to use based on account type
  const { handleSubmit, formState, control, watch } =
    accountType === 'business' ? businessForm : individualForm;

  const { isValid, errors } = formState;

  // Watch form fields to determine if partially filled
  const formValues = watch();

  // Check if the form is partially filled but not completely valid
  useEffect(() => {
    if (accountType === 'business') {
      const values = formValues.googleWorkspace;
      // Check if any field has a value but the form isn't valid
      const hasAnyValue =
        (values.adminEmail && values.adminEmail.trim() !== '') || serviceCredentialsFile !== null;

      setFormPartiallyFilled(hasAnyValue && !isValid);
    } else {
      const values = formValues.googleWorkspace;
      // Check if any field has a value but the form isn't valid
      const hasAnyValue =
        (values.clientId && values.clientId.trim() !== '') ||
        (values.clientSecret && values.clientSecret.trim() !== '') ||
        (values.redirectUri &&
          values.redirectUri !== 'http://localhost:3001/account/individual/settings/connector');

      setFormPartiallyFilled(hasAnyValue && !isValid);
    }
  }, [formValues, isValid, accountType, serviceCredentialsFile]);

  // Second useEffect to initialize form with initial values and file
  useEffect(() => {
    if (initialValues) {
      if (accountType === 'business') {
        businessForm.reset(initialValues);
      } else {
        individualForm.reset(initialValues);
      }
    }
    if (initialFile) {
      setServiceCredentialsFile(initialFile);
    }
  }, [initialValues, initialFile, accountType, businessForm, individualForm]);

  // Extract data from uploaded JSON for individual users
  const extractIndividualDataFromJson = useCallback(
    (jsonData: any) => {
      try {
        console.log('Parsing individual JSON data:', jsonData);

        // Web application credentials format
        if (jsonData.web) {
          const clientId = jsonData.web.client_id;
          const clientSecret = jsonData.web.client_secret;

          if (clientId && clientSecret) {
            individualForm.setValue('googleWorkspace.clientId', clientId, { shouldValidate: true });
            individualForm.setValue('googleWorkspace.clientSecret', clientSecret, {
              shouldValidate: true,
            });

            return true;
          }
        }

        // Try installed application format
        if (jsonData.installed) {
          const clientId = jsonData.installed.client_id;
          const clientSecret = jsonData.installed.client_secret;

          if (clientId && clientSecret) {
            individualForm.setValue('googleWorkspace.clientId', clientId, { shouldValidate: true });
            individualForm.setValue('googleWorkspace.clientSecret', clientSecret, {
              shouldValidate: true,
            });

            return true;
          }
        }

        // Try direct properties (less common but possible)
        const clientId = jsonData.clientId || jsonData.client_id;
        const clientSecret = jsonData.clientSecret || jsonData.client_secret;

        if (clientId && clientSecret) {
          individualForm.setValue('googleWorkspace.clientId', clientId, { shouldValidate: true });
          individualForm.setValue('googleWorkspace.clientSecret', clientSecret, {
            shouldValidate: true,
          });

          return true;
        }

        setMessage('Could not find client ID and client secret in the JSON file');
        return false;
      } catch (error) {
        console.error('Error parsing JSON file:', error);
        setMessage('Failed to extract data from JSON file');
        return false;
      }
    },
    [individualForm, setMessage]
  );

  // Extract data from uploaded JSON for business users
  const extractBusinessDataFromJson = useCallback(
    (jsonData: any) => {
      try {
        // Store the full parsed JSON for later use
        setParsedJsonData(jsonData);

        // Extract required fields
        businessForm.setValue('googleWorkspace.clientId', jsonData.client_id || '', {
          shouldValidate: true,
        });
        businessForm.setValue('googleWorkspace.clientEmail', jsonData.client_email || '', {
          shouldValidate: true,
        });
        businessForm.setValue('googleWorkspace.privateKey', jsonData.private_key || '', {
          shouldValidate: true,
        });
        businessForm.setValue('googleWorkspace.projectId', jsonData.project_id || '', {
          shouldValidate: true,
        });

        return true;
      } catch (error) {
        setMessage('Failed to extract JSON data');
        return false;
      }
    },
    // eslint-disable-next-line
    [businessForm]
  );

  // Expose submit method to parent component
  useEffect(() => {
    (window as any).submitConnectorForm = () => {
      if (formPartiallyFilled) {
        // Don't allow submission if the form is partially filled but not valid
        setMessage('Please complete all required fields or skip this step');
        return false;
      }

      if (accountType === 'business') {
        // Business accounts require file upload and admin email
        if (isValid && serviceCredentialsFile && parsedJsonData) {
          handleSubmit((data) => {
            onSubmit(data, serviceCredentialsFile);
          })();
          return true;
        }
        return false;
      }

      // Individual accounts can now submit only if fully valid
      if (isValid) {
        handleSubmit((data) => {
          onSubmit(data, serviceCredentialsFile);
        })();
        return true;
      }
      return false;
    };

    return () => {
      delete (window as any).submitConnectorForm;
    };
  }, [
    accountType,
    isValid,
    serviceCredentialsFile,
    handleSubmit,
    onSubmit,
    parsedJsonData,
    formPartiallyFilled,
    setMessage,
  ]);

  // Validate file type using both extension and MIME type
  const validateFileType = useCallback((file: File): boolean => {
    // Check file extension
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    const isValidExtension = ALLOWED_FILE_EXTENSIONS.includes(fileExtension);

    // Check MIME type (more reliable than extension)
    const isValidMimeType = ALLOWED_FILE_TYPES.includes(file.type);

    // For JSON files, we need to be more forgiving with MIME types as they can vary
    // Some systems might report "text/plain" or other MIME types for JSON
    const isJsonFile = fileExtension === '.json';

    return isValidExtension && (isValidMimeType || isJsonFile);
  }, []);

  // Process the selected file
  const processFile = useCallback(
    (file: File): void => {
      setIsProcessing(true);
      setCredentialsError('');

      // Check file size
      if (file.size > FILE_SIZE_LIMIT) {
        setCredentialsError(
          `File is too large. Maximum size is ${FILE_SIZE_LIMIT / (1024 * 1024)} MB.`
        );
        setIsProcessing(false);
        return;
      }

      // Check file type
      if (!validateFileType(file)) {
        setCredentialsError('Only JSON files are supported. Please select a valid JSON file.');
        setIsProcessing(false);
        return;
      }

      setServiceCredentialsFile(file);
      const reader = new FileReader();

      reader.onload = (e: ProgressEvent<FileReader>) => {
        if (e.target && typeof e.target.result === 'string') {
          try {
            // Validate JSON structure
            const jsonData = JSON.parse(e.target.result);

            if (accountType === 'business') {
              // Business account validation
              if (!jsonData.client_id || !jsonData.client_email || !jsonData.private_key) {
                throw new Error('Missing required fields in service account credentials file');
              }

              // Store the raw JSON content
              businessForm.setValue('googleWorkspace.serviceCredentials', e.target.result, {
                shouldValidate: true,
              });

              // Extract fields for business
              extractBusinessDataFromJson(jsonData);
            } else if (!extractIndividualDataFromJson(jsonData)) {
              // Individual account handling - using else if
              throw new Error('Missing required fields in the JSON file (clientId, clientSecret)');
            }

            setIsProcessing(false);
          } catch (error: any) {
            setCredentialsError(
              `Invalid JSON format: ${error.message || 'The file does not contain valid JSON data.'}`
            );
            setServiceCredentialsFile(null);
            setParsedJsonData(null);
            setIsProcessing(false);
          }
        }
      };

      reader.onerror = () => {
        setCredentialsError('Error reading file. Please try again.');
        setServiceCredentialsFile(null);
        setParsedJsonData(null);
        setIsProcessing(false);
      };

      reader.readAsText(file);
    },
    [
      validateFileType,
      accountType,
      extractIndividualDataFromJson,
      businessForm,
      extractBusinessDataFromJson,
    ]
  );

  // Handle file selection from input
  const handleFileChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      setCredentialsError('');
      const { files } = event.target;

      if (files && files[0]) {
        processFile(files[0]);
      }
      // Reset the file input to ensure onChange fires even if the same file is selected again
      event.target.value = '';
    },
    [processFile]
  );

  const handleFormSubmit = useCallback(
    (data: any) => {
      if (formPartiallyFilled) {
        setMessage('Please complete all required fields or skip this step');
        return;
      }

      if (accountType === 'business') {
        if (serviceCredentialsFile && parsedJsonData) {
          onSubmit(data, serviceCredentialsFile);
        }
      } else {
        // Individual account - can submit with or without file
        onSubmit(data, serviceCredentialsFile);
      }
    },
    [accountType, onSubmit, serviceCredentialsFile, parsedJsonData, formPartiallyFilled, setMessage]
  );

  // Drag and drop handlers
  const handleDragEnter = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer) {
      e.dataTransfer.dropEffect = 'copy';
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const { files } = e.dataTransfer;
      if (files.length > 1) {
        setCredentialsError('Please drop only one file.');
        return;
      }

      if (files && files[0]) {
        processFile(files[0]);
      }
    },
    [processFile]
  );

  // Remove file handler
  const handleRemoveFile = useCallback(
    (e: React.MouseEvent) => {
      e.stopPropagation();
      setServiceCredentialsFile(null);
      setParsedJsonData(null);

      if (accountType === 'business') {
        businessForm.setValue('googleWorkspace.serviceCredentials', '', { shouldValidate: true });
        businessForm.setValue('googleWorkspace.clientId', '');
        businessForm.setValue('googleWorkspace.clientEmail', '');
        businessForm.setValue('googleWorkspace.privateKey', '');
        businessForm.setValue('googleWorkspace.projectId', '');
      }
      // For individual accounts, we keep the form values to allow manual editing
    },
    [accountType, businessForm]
  );

  // Memoized upload area styles - enhanced modern design
  const uploadAreaStyles = useMemo(
    () => ({
      border: `2px dashed ${
        isDragging
          ? theme.palette.primary.main
          : serviceCredentialsFile
            ? theme.palette.success.main
            : alpha(theme.palette.text.primary, 0.15)
      }`,
      borderRadius: '12px',
      height: accountType === 'business' ? 220 : 200,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      textAlign: 'center',
      bgcolor: isDragging
        ? alpha(theme.palette.primary.main, 0.04)
        : serviceCredentialsFile
          ? alpha(theme.palette.success.main, 0.04)
          : alpha(theme.palette.background.default, 0.6),
      cursor: isProcessing ? 'wait' : 'pointer',
      transition: theme.transitions.create(
        ['border-color', 'background-color', 'box-shadow', 'transform'],
        { duration: theme.transitions.duration.shorter }
      ),
      '&:hover': {
        borderColor: !isProcessing ? theme.palette.primary.main : undefined,
        bgcolor: !isProcessing ? alpha(theme.palette.primary.main, 0.04) : undefined,
        boxShadow: !isProcessing
          ? `0 4px 12px ${alpha(theme.palette.primary.main, 0.08)}`
          : undefined,
        transform: !isProcessing ? 'translateY(-2px)' : undefined,
      },
      position: 'relative',
      px: 2,
      py: 3,
    }),
    [theme, isDragging, serviceCredentialsFile, isProcessing, accountType]
  );

  // Direct form submission handler
  const onFormSubmit = (data: ConnectorFormValues) => {
    handleFormSubmit(data);
  };

  return (
    <Paper
      component="form"
      id="connector-config-form"
      onSubmit={handleSubmit(onFormSubmit)}
      noValidate
      elevation={0}
      sx={{
        height: '100%',
        maxHeight: '500px',
        display: 'flex',
        flexDirection: 'column',
        backdropFilter: 'blur(8px)',
        borderRadius: 3,
        overflow: 'hidden',
        ...scrollableContainerStyle,
        ...scrollableContainerStyle,
      }}
    >
      <Box
        sx={{
          p: { xs: 2.5, sm: 3.5 },
          pb: { xs: 2.5, sm: 3.5 },
          height: '100%',
          overflow: 'auto',
          ...scrollableContainerStyle,
        }}
      >
        {/* Header with logo */}
        <Stack direction="row" spacing={2.5} alignItems="center" sx={{ mb: 3.5 }}>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 46,
              height: 46,
              borderRadius: '10px',
              overflow: 'hidden',
              boxShadow: `0 3px 10px ${alpha('#4285F4', 0.25)}`,
              flexShrink: 0,
            }}
          >
            <Iconify
              icon="simple-icons:google"
              width={28}
              height={28}
              color={theme.palette.primary.main}
            />
          </Box>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 600, letterSpacing: '-0.01em' }}>
              Google Workspace
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5, opacity: 0.85 }}>
              {accountType === 'business'
                ? 'Upload your service account credentials and set admin email'
                : 'Configure your OAuth credentials'}
            </Typography>
          </Box>
        </Stack>

        {/* Business account admin email field */}
        {accountType === 'business' && (
          <Stack spacing={2.5} sx={{ mb: 3 }}>
            <Controller
              name="googleWorkspace.adminEmail"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  {...field}
                  label="Admin Email Address"
                  placeholder="e.g., admin@yourdomain.com"
                  fullWidth
                  size="small"
                  error={!!fieldState.error}
                  helperText={fieldState.error?.message}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Iconify
                          icon="ri:mail-line"
                          width={20}
                          height={20}
                          sx={{ color: theme.palette.primary.main, opacity: 0.8 }}
                        />
                      </InputAdornment>
                    ),
                  }}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 2,
                      bgcolor: alpha(theme.palette.background.paper, 0.6),
                      transition: theme.transitions.create(['box-shadow', 'background-color']),
                      '&:hover': {
                        bgcolor: theme.palette.background.paper,
                      },
                      '&.Mui-focused': {
                        boxShadow: `0 0 0 2px ${alpha(theme.palette.primary.main, 0.2)}`,
                      },
                    },
                  }}
                />
              )}
            />
          </Stack>
        )}

        {/* Individual account form fields */}
        {redirectUris?.urisMismatch && (
          <Alert
            severity="warning"
            sx={{
              mb: 3,
              borderRadius: 1,
            }}
          >
            <Typography variant="body2" sx={{ mb: 1 }}>
              Redirect URI mismatch detected! Using the recommended URI from backend configuration.
            </Typography>
            <Typography variant="caption" component="div">
              Current window location: {redirectUris.currentWindowLocation}
            </Typography>
            <Typography variant="caption" component="div">
              Recommended redirect URI: {redirectUris.recommendedRedirectUri}
            </Typography>
          </Alert>
        )}
        {accountType === 'individual' && (
          <>
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
                icon="eva:info-outline"
                width={20}
                height={20}
                color={theme.palette.info.main}
                style={{ marginTop: 2 }}
              />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  <Typography
                    component="span"
                    variant="body2"
                    color="primary.main"
                    sx={{ fontWeight: 500 }}
                  >
                    Redirect URI:
                  </Typography>{' '}
                  {redirectUris?.recommendedRedirectUri}
                </Typography>
              </Box>
            </Box>

            <Stack spacing={2.5} sx={{ mb: 4 }}>
              <Controller
                name="googleWorkspace.clientId"
                control={control}
                render={({ field, fieldState }) => (
                  <TextField
                    {...field}
                    label="Client ID"
                    placeholder="e.g., 969340771549-75fn6kuu6p4oapk45ibrc5acpps.com"
                    fullWidth
                    size="small"
                    error={!!fieldState.error}
                    helperText={fieldState.error?.message}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Iconify
                            icon="ri:user-settings-line"
                            width={20}
                            height={20}
                            sx={{ color: theme.palette.primary.main, opacity: 0.8 }}
                          />
                        </InputAdornment>
                      ),
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        borderRadius: 2,
                        bgcolor: alpha(theme.palette.background.paper, 0.6),
                        transition: theme.transitions.create(['box-shadow', 'background-color']),
                        '&:hover': {
                          bgcolor: theme.palette.background.paper,
                        },
                        '&.Mui-focused': {
                          boxShadow: `0 0 0 2px ${alpha(theme.palette.primary.main, 0.2)}`,
                        },
                      },
                    }}
                  />
                )}
              />

              <Controller
                name="googleWorkspace.clientSecret"
                control={control}
                render={({ field, fieldState }) => (
                  <TextField
                    {...field}
                    label="Client Secret"
                    placeholder="e.g., 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"
                    fullWidth
                    size="small"
                    type="password"
                    error={!!fieldState.error}
                    helperText={fieldState.error?.message}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Iconify
                            icon="ri:key-2-line"
                            width={20}
                            height={20}
                            sx={{ color: theme.palette.primary.main, opacity: 0.8 }}
                          />
                        </InputAdornment>
                      ),
                    }}
                    sx={{
                      '& .MuiOutlinedInput-root': {
                        borderRadius: 2,
                        bgcolor: alpha(theme.palette.background.paper, 0.6),
                        transition: theme.transitions.create(['box-shadow', 'background-color']),
                        '&:hover': {
                          bgcolor: theme.palette.background.paper,
                        },
                        '&.Mui-focused': {
                          boxShadow: `0 0 0 2px ${alpha(theme.palette.primary.main, 0.2)}`,
                        },
                      },
                    }}
                  />
                )}
              />

              {/* <Controller
              name="googleWorkspace.redirectUri"
              control={control}
              render={({ field, fieldState }) => (
                <TextField
                  {...field}
                  label="Redirect URI"
                  fullWidth
                  size="small"
                  error={!!fieldState.error}
                  helperText={fieldState.error?.message}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Iconify
                          icon="ri:links-line"
                          width={20}
                          height={20}
                          sx={{ color: theme.palette.primary.main, opacity: 0.8 }}
                        />
                      </InputAdornment>
                    ),
                  }}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 2,
                      bgcolor: alpha(theme.palette.background.paper, 0.6),
                      transition: theme.transitions.create(['box-shadow', 'background-color']),
                      '&:hover': {
                        bgcolor: theme.palette.background.paper,
                      },
                      '&.Mui-focused': {
                        boxShadow: `0 0 0 2px ${alpha(theme.palette.primary.main, 0.2)}`,
                      },
                    },
                  }}
                />
              )}
            /> */}
            </Stack>
          </>
        )}

        {/* File Upload UI */}
        <Box sx={{ mt: 0, mb: 2, flexGrow: 1 }}>
          {accountType === 'individual' && (
            <Stack direction="row" alignItems="center" spacing={1.5} sx={{ mb: 3.5 }}>
              <Divider sx={{ flexGrow: 1 }} />
              <Chip
                label="OR UPLOAD CREDENTIALS"
                size="small"
                variant="outlined"
                sx={{
                  px: 1.5,
                  py: 0.5,
                  borderRadius: '8px',
                  fontSize: '0.675rem',
                  fontWeight: 600,
                  letterSpacing: '0.05em',
                  border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,
                  color: theme.palette.primary.main,
                }}
              />
              <Divider sx={{ flexGrow: 1 }} />
            </Stack>
          )}

          <Tooltip
            title={
              isProcessing
                ? 'Processing file...'
                : 'Drag and drop your credentials file or click to browse'
            }
            placement="top"
            arrow
          >
            <Box
              component="div"
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              role="button"
              tabIndex={0}
              onClick={() => !isProcessing && document.getElementById('file-upload-input')?.click()}
              onKeyDown={(e) => {
                if (!isProcessing && (e.key === 'Enter' || e.key === ' ')) {
                  document.getElementById('file-upload-input')?.click();
                }
              }}
              aria-disabled={isProcessing}
              sx={{
                ...uploadAreaStyles,
                mx: { xs: 0, sm: 1 },
                mt: 1,
                mb: { xs: 2.5, sm: 3 },
              }}
            >
              {isProcessing ? (
                <Stack spacing={1.5} alignItems="center">
                  <CircularProgress
                    size={32}
                    thickness={4}
                    sx={{
                      color: theme.palette.primary.main,
                    }}
                  />
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>
                    Processing file...
                  </Typography>
                </Stack>
              ) : !serviceCredentialsFile ? (
                <>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 60,
                      height: 60,
                      borderRadius: '50%',
                      background: `linear-gradient(135deg, ${alpha(theme.palette.primary.light, 0.12)}, ${alpha(theme.palette.primary.main, 0.15)})`,
                      mb: 2.5,
                      transition: theme.transitions.create(['transform', 'background-color'], {
                        duration: theme.transitions.duration.shorter,
                      }),
                      ...(isDragging && {
                        transform: 'scale(1.1)',
                        bgcolor: alpha(theme.palette.primary.main, 0.12),
                      }),
                    }}
                  >
                    <Iconify
                      icon={isDragging ? 'ri:file-upload-fill' : 'ri:upload-cloud-2-line'}
                      width={32}
                      height={32}
                      sx={{
                        color: theme.palette.primary.main,
                        transition: theme.transitions.create('transform', {
                          duration: theme.transitions.duration.shortest,
                        }),
                        ...(isDragging && {
                          transform: 'scale(1.1)',
                        }),
                      }}
                    />
                  </Box>
                  <Typography
                    variant="body1"
                    sx={{
                      fontWeight: 600,
                      color: isDragging ? theme.palette.primary.main : 'text.primary',
                    }}
                  >
                    {isDragging
                      ? 'Drop file here'
                      : accountType === 'business'
                        ? 'Upload service credentials'
                        : 'Upload JSON credentials'}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                    or click to browse files
                  </Typography>
                  <Box
                    sx={{
                      mt: 1,
                      px: 1.5,
                      py: 0.5,
                      borderRadius: '6px',
                      bgcolor: alpha(theme.palette.info.main, 0.08),
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    <Iconify
                      icon="mdi:information-outline"
                      width={14}
                      height={14}
                      sx={{ color: theme.palette.info.main, mr: 0.5 }}
                    />
                    <Typography
                      variant="caption"
                      sx={{ fontWeight: 500, color: theme.palette.info.main, fontSize: '0.65rem' }}
                    >
                      Only .json files supported (max 5MB)
                    </Typography>
                  </Box>
                </>
              ) : (
                <Fade in={!!serviceCredentialsFile}>
                  <Stack spacing={1.5} alignItems="center" width="100%">
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 52,
                        height: 52,
                        borderRadius: '50%',
                        background: `linear-gradient(135deg, ${alpha(theme.palette.success.light, 0.2)}, ${alpha(
                          theme.palette.success.main,
                          0.2
                        )})`,
                        boxShadow: `0 4px 12px ${alpha(theme.palette.success.main, 0.15)}`,
                        mb: 1,
                      }}
                    >
                      <Iconify
                        icon="mdi:check-circle-outline"
                        width={28}
                        height={28}
                        sx={{ color: theme.palette.success.main }}
                      />
                    </Box>

                    <Box
                      sx={{
                        px: 2,
                        py: 0.75,
                        borderRadius: '8px',
                        bgcolor: alpha(theme.palette.background.paper, 0.5),
                        border: `1px solid ${alpha(theme.palette.divider, 0.08)}`,
                        boxShadow: `0 2px 8px ${alpha(theme.palette.common.black, 0.04)}`,
                        display: 'flex',
                        alignItems: 'center',
                        width: 'auto',
                        maxWidth: '100%',
                      }}
                    >
                      <Iconify
                        icon="ri:file-text-line"
                        width={20}
                        height={20}
                        sx={{ color: theme.palette.primary.main, flexShrink: 0, mr: 1 }}
                      />
                      <Typography
                        variant="body2"
                        fontWeight={500}
                        sx={{
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {serviceCredentialsFile.name}
                      </Typography>
                    </Box>

                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ fontSize: '0.7rem' }}
                    >
                      {(serviceCredentialsFile.size / 1024).toFixed(1)} KB
                    </Typography>

                    <Button
                      size="small"
                      color="error"
                      variant="outlined"
                      startIcon={<Iconify icon="ri:delete-bin-line" width={18} height={18} />}
                      sx={{
                        borderRadius: '10px',
                        textTransform: 'none',
                        px: 2,
                        py: 0.75,
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        boxShadow: `0 2px 8px ${alpha(theme.palette.error.main, 0.15)}`,
                        background: `linear-gradient(135deg, ${alpha(theme.palette.error.light, 0.2)}, ${alpha(
                          theme.palette.error.main,
                          0.2
                        )})`,
                        '&:hover': {
                          background: `linear-gradient(135deg, ${alpha(theme.palette.error.light, 0.3)}, ${alpha(
                            theme.palette.error.main,
                            0.3
                          )})`,
                        },
                      }}
                      onClick={handleRemoveFile}
                    >
                      Remove
                    </Button>
                  </Stack>
                </Fade>
              )}
            </Box>
          </Tooltip>
        </Box>

        {/* Warning for partially filled forms */}
        {formPartiallyFilled && (
          <Box
            sx={{
              mb: 2,
              p: 2,
              borderRadius: '10px',
              background: `linear-gradient(135deg, ${alpha(theme.palette.warning.light, 0.08)}, ${alpha(
                theme.palette.warning.main,
                0.08
              )})`,
              borderLeft: `4px solid ${theme.palette.warning.main}`,
              display: 'flex',
              alignItems: 'flex-start',
              boxShadow: `0 2px 8px ${alpha(theme.palette.warning.main, 0.1)}`,
            }}
          >
            <Iconify
              icon="ri:alert-line"
              width={22}
              height={22}
              sx={{ color: theme.palette.warning.main, mt: 0.25, mr: 1.5, flexShrink: 0 }}
            />
            <Typography variant="body2" color="warning.main" sx={{ fontWeight: 500 }}>
              Please complete all required fields or use the Skip button. Partial configuration is
              not allowed.
            </Typography>
          </Box>
        )}

        {credentialsError && (
          <Box
            sx={{
              mb: 2,
              p: 2,
              borderRadius: '10px',
              background: `linear-gradient(135deg, ${alpha(theme.palette.error.light, 0.08)}, ${alpha(
                theme.palette.error.main,
                0.08
              )})`,
              borderLeft: `4px solid ${theme.palette.error.main}`,
              display: 'flex',
              alignItems: 'flex-start',
              boxShadow: `0 2px 8px ${alpha(theme.palette.error.main, 0.1)}`,
            }}
          >
            <Iconify
              icon="ri:error-warning-fill"
              width={22}
              height={22}
              sx={{ color: theme.palette.error.main, mt: 0.25, mr: 1.5, flexShrink: 0 }}
            />
            <Typography variant="body2" color="error.main" sx={{ fontWeight: 500 }}>
              {credentialsError}
            </Typography>
          </Box>
        )}

        {/* Hidden file input */}
        <input
          id="file-upload-input"
          type="file"
          accept=".json,application/json"
          hidden
          onChange={handleFileChange}
          disabled={isProcessing}
        />

        {/* Hidden submit button for programmatic submission */}
        <Button type="submit" style={{ display: 'none' }} id="connector-form-submit-button">
          Submit
        </Button>
      </Box>
    </Paper>
  );
};
export default ConnectorConfigStep;
