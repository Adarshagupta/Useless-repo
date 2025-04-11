// App theme colors and styles
const colors = {
  primary: '#FF385C',
  primaryDark: '#E61E4D',
  primaryLight: '#FF5A5F',
  secondary: '#00A699',
  secondaryDark: '#008F8C',
  secondaryLight: '#2EC4B6',
  accent: '#6246EA',
  success: '#22C55E',
  warning: '#F59E0B',
  error: '#EF4444',
  dark: '#111827',
  darkGray: '#374151',
  gray: '#6B7280',
  lightGray: '#D1D5DB',
  extraLightGray: '#F3F4F6',
  white: '#FFFFFF',
  background: '#F9FAFB',
  card: '#FFFFFF',
  border: '#E5E7EB',
};

const typography = {
  fontFamily: {
    sans: 'System',
    serif: 'Georgia',
    mono: 'Courier',
  },
  fontSize: {
    xs: 12,
    sm: 14,
    base: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
  lineHeight: {
    none: 1,
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  },
};

const spacing = {
  '0': 0,
  '0.5': 2,
  '1': 4,
  '2': 8,
  '3': 12,
  '4': 16,
  '5': 20,
  '6': 24,
  '8': 32,
  '10': 40,
  '12': 48,
  '16': 64,
};

const borderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

const shadows = {
  none: {
    shadowColor: 'transparent',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0,
    shadowRadius: 0,
    elevation: 0,
  },
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
};

// Common styles
const commonStyles = {
  card: {
    backgroundColor: colors.card,
    borderRadius: borderRadius.lg,
    padding: spacing['4'],
    ...shadows.md,
  },
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  section: {
    marginBottom: spacing['6'],
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.dark,
    marginBottom: spacing['3'],
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  center: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  spaceBetween: {
    justifyContent: 'space-between',
  },
};

// Export all theme elements
const theme = {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  commonStyles,
};

export { colors, typography, spacing, borderRadius, shadows, commonStyles };
export default theme;