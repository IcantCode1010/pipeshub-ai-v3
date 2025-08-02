# PipesHub AI Design Profile

## Overview

PipesHub AI uses Material-UI (MUI) v5 as its primary component library with a custom theme configuration. The application supports both light and dark modes with a modern, clean interface following Material Design principles.

## Color System

### Primary Colors

```json
{
  "primary": {
    "lighter": "#C8FAD6",
    "light": "#5BE49B",
    "main": "#00A76F",    // Main green
    "dark": "#007867",
    "darker": "#004B50",
    "contrastText": "#FFFFFF"
  }
}
```

### Secondary Colors

```json
{
  "secondary": {
    "lighter": "#EFD6FF",
    "light": "#C684FF",
    "main": "#8E33FF",    // Purple
    "dark": "#5119B7",
    "darker": "#27097A",
    "contrastText": "#FFFFFF"
  }
}
```

### Status Colors

```json
{
  "info": {
    "lighter": "#CAFDF5",
    "light": "#61F3F3",
    "main": "#00B8D9",    // Cyan
    "dark": "#006C9C",
    "darker": "#003768",
    "contrastText": "#FFFFFF"
  },
  "success": {
    "lighter": "#D3FCD2",
    "light": "#77ED8B",
    "main": "#22C55E",    // Green
    "dark": "#118D57",
    "darker": "#065E49",
    "contrastText": "#FFFFFF"
  },
  "warning": {
    "lighter": "#FFF5CC",
    "light": "#FFD666",
    "main": "#FFAB00",    // Orange
    "dark": "#B76E00",
    "darker": "#7A4100",
    "contrastText": "#1C252E"
  },
  "error": {
    "lighter": "#FFE9D5",
    "light": "#FFAC82",
    "main": "#FF5630",    // Red
    "dark": "#B71D18",
    "darker": "#7A0916",
    "contrastText": "#FFFFFF"
  }
}
```

### Grey Scale

```json
{
  "grey": {
    "50": "#FCFDFD",
    "100": "#F9FAFB",
    "200": "#F4F6F8",
    "300": "#DFE3E8",
    "400": "#C4CDD5",
    "500": "#919EAB",    // Mid grey
    "600": "#637381",
    "700": "#454F5B",
    "800": "#1C252E",
    "900": "#141A21"
  }
}
```

### Theme-Specific Colors

#### Light Mode

- **Background**: `#FFFFFF` (paper and default)
- **Background Neutral**: `grey[200]` (#F4F6F8)
- **Text Primary**: `grey[800]` (#1C252E)
- **Text Secondary**: `grey[600]` (#637381)
- **Text Disabled**: `grey[500]` (#919EAB)
- **Divider**: `rgba(grey[500], 0.2)`

#### Dark Mode

- **Background Paper**: `grey[800]` (#1C252E)
- **Background Default**: `grey[900]` (#141A21)
- **Background Neutral**: `#28323D`
- **Text Primary**: `#FFFFFF`
- **Text Secondary**: `grey[500]` (#919EAB)
- **Text Disabled**: `grey[600]` (#637381)
- **Divider**: `rgba(grey[500], 0.2)`

## Typography

### Font Families

- **Primary Font**: "Public Sans Variable" (for body text)
- **Secondary Font**: "Barlow" (for headings H1-H3)
- **Font Stack**: `"FontName", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`

### Font Weights

- Light: 300
- Regular: 400
- Medium: 500
- SemiBold: 600
- Bold: 700

### Typography Scale

| Variant             | Font Size        | Line Height | Font Weight | Font Family | Responsive Sizes             |
| ------------------- | ---------------- | ----------- | ----------- | ----------- | ---------------------------- |
| **h1**        | 40px (2.5rem)    | 1.25        | 800         | Barlow      | sm: 52px, md: 58px, lg: 64px |
| **h2**        | 32px (2rem)      | 1.33        | 800         | Barlow      | sm: 40px, md: 44px, lg: 48px |
| **h3**        | 24px (1.5rem)    | 1.5         | 700         | Barlow      | sm: 26px, md: 30px, lg: 32px |
| **h4**        | 20px (1.25rem)   | 1.5         | 700         | Primary     | sm: 20px, md: 24px, lg: 24px |
| **h5**        | 18px (1.125rem)  | 1.5         | 700         | Primary     | sm: 19px, md: 20px, lg: 20px |
| **h6**        | 17px (1.0625rem) | 1.56        | 600         | Primary     | sm: 18px, md: 18px, lg: 18px |
| **subtitle1** | 16px (1rem)      | 1.5         | 600         | Primary     | -                            |
| **subtitle2** | 14px (0.875rem)  | 1.57        | 600         | Primary     | -                            |
| **body1**     | 16px (1rem)      | 1.5         | 400         | Primary     | -                            |
| **body2**     | 14px (0.875rem)  | 1.57        | 400         | Primary     | -                            |
| **caption**   | 12px (0.75rem)   | 1.5         | 400         | Primary     | -                            |
| **overline**  | 12px (0.75rem)   | 1.5         | 700         | Primary     | UPPERCASE                    |
| **button**    | 14px (0.875rem)  | 1.71        | 700         | Primary     | Normal case                  |

## Spacing System

PipesHub AI uses an 8px base grid system. Common spacing values:

- **4px** (0.25rem): Minimal spacing
- **8px** (0.5rem): Small spacing
- **12px** (0.75rem): Compact spacing
- **16px** (1rem): Default spacing
- **24px** (1.5rem): Medium spacing
- **32px** (2rem): Large spacing
- **48px** (3rem): Extra large spacing

## Component Styling

### Buttons

#### Button Sizes

- **Small**: Height 30px, padding 4px (text) or 8px (contained/outlined)
- **Medium**: Default height, padding 8px (text) or 12px (contained/outlined)
- **Large**: Height 48px, padding 10px (text) or 16px (contained/outlined)

#### Button Variants

1. **Contained** (default): Solid background, elevation disabled by default
2. **Outlined**: Transparent with border
3. **Text**: No background or border
4. **Soft** (custom): Light background with alpha channel

#### Button States

- **Hover**: Box shadow for contained, border highlight for outlined
- **Disabled**: Reduced opacity (0.48)
- **Loading**: Spinner with position indicators

### Shadows

The app uses a 25-level shadow system (0-24) with dynamic opacity based on theme:

- Light mode: Based on grey[500]
- Dark mode: Based on black

Common shadow levels:

- **z0**: None
- **z1**: Subtle elevation
- **z8**: Card elevation
- **z16**: Modal/Dialog elevation
- **z24**: Maximum elevation

### Border Radius

- **Small**: 4px
- **Default**: 8px
- **Medium**: 12px
- **Large**: 16px

## Layout & Responsive Design

### Breakpoints

- **xs**: 0px (mobile)
- **sm**: 600px (tablet portrait)
- **md**: 900px (tablet landscape)
- **lg**: 1200px (desktop)
- **xl**: 1536px (large desktop)

### Container Widths

- Max width: 1200px (centered with padding)
- Padding: 16px (mobile), 24px (tablet+)

### Navigation

- **Horizontal Nav** (default): Top navigation bar
- **Vertical Nav**: Side navigation drawer
- **Compact Layout**: Reduced spacing option

## Utility Classes & Helpers

### Color Utilities

```javascript
// Alpha channel colors
varAlpha(colorChannel, opacity) // e.g., varAlpha(grey['500Channel'], 0.2)
```

### Responsive Font Sizes

```javascript
responsiveFontSizes({ sm: 16, md: 18, lg: 20 })
```

### Media Query Helpers

```javascript
useResponsive('up', 'md')    // Desktop and up
useResponsive('down', 'sm')  // Mobile only
useResponsive('between', 'sm', 'md') // Tablet only
```

## CSS-in-JS Patterns

### Theme Access

```javascript
theme.palette.primary.main
theme.typography.h1
theme.spacing(2) // 16px
theme.breakpoints.up('md')
```

### Conditional Styling

```javascript
// Light/Dark mode specific
[stylesMode.dark]: { 
  backgroundColor: theme.palette.grey[800] 
}

// Responsive styling
[theme.breakpoints.up('md')]: {
  padding: theme.spacing(3)
}
```

## Icons

The application uses Iconify icons with the following primary sets:

- **@iconify/solar**: Main icon set
- **@iconify/mdi**: Material Design icons
- **@iconify/eva**: Eva icons

## Form Elements

### Text Fields

- Full width by default
- Helper text below field
- Error states with red accent
- Floating labels

### Select/Autocomplete

- Consistent with text field styling
- Dropdown with shadow
- Multi-select with chips

### Checkboxes/Radio

- Primary color accent
- Custom sizing options
- Disabled state with reduced opacity

## Best Practices for New Pages

1. **Use Theme Variables**: Always reference theme colors, spacing, and typography
2. **Responsive First**: Design mobile-first, enhance for larger screens
3. **Consistent Spacing**: Use the 8px grid system
4. **Typography Hierarchy**: Use appropriate heading levels and text variants
5. **Color Usage**: Primary for main actions, grey for secondary, status colors for feedback
6. **Dark Mode Support**: Test all components in both light and dark themes
7. **Accessibility**: Maintain proper contrast ratios and focus states
8. **Component Reuse**: Leverage existing MUI components before creating custom ones

## Example Component Structure

```jsx
import { Box, Typography, Button, Card } from '@mui/material';
import { useTheme } from '@mui/material/styles';

function ExamplePage() {
  const theme = useTheme();
  
  return (
    <Box sx={{ 
      p: 3,  // 24px padding
      maxWidth: 'lg',
      mx: 'auto'
    }}>
      <Typography variant="h3" sx={{ mb: 3 }}>
        Page Title
      </Typography>
    
      <Card sx={{ 
        p: 3,
        backgroundColor: theme.palette.background.paper,
        boxShadow: theme.customShadows[8]
      }}>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
          Content goes here
        </Typography>
      
        <Button 
          variant="contained" 
          color="primary"
          size="large"
        >
          Action Button
        </Button>
      </Card>
    </Box>
  );
}
```

This design profile ensures consistency across all pages and components in the PipesHub AI application.
