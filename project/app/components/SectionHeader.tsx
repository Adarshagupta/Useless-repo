import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { ChevronRight } from 'lucide-react-native';
import { colors, typography, spacing, borderRadius } from '../theme';

interface SectionHeaderProps {
  title: string;
  icon?: React.ReactNode;
  onSeeAllPress?: () => void;
  showSeeAll?: boolean;
}

const SectionHeader = ({
  title,
  icon,
  onSeeAllPress,
  showSeeAll = true,
}: SectionHeaderProps) => {
  return (
    <View style={styles.container}>
      <View style={styles.titleContainer}>
        <Text style={styles.title}>{title}</Text>
        {icon && <View style={styles.iconContainer}>{icon}</View>}
      </View>
      
      {showSeeAll && onSeeAllPress && (
        <TouchableOpacity style={styles.seeAllButton} onPress={onSeeAllPress}>
          <Text style={styles.seeAllText}>See All</Text>
          <ChevronRight size={16} color={colors.gray} />
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing['4'],
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  title: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.dark,
  },
  iconContainer: {
    marginLeft: spacing['2'],
  },
  seeAllButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.extraLightGray,
    paddingHorizontal: spacing['3'],
    paddingVertical: spacing['1'],
    borderRadius: borderRadius.full,
  },
  seeAllText: {
    fontSize: typography.fontSize.sm,
    color: colors.gray,
    marginRight: spacing['1'],
  },
});

export default SectionHeader;
