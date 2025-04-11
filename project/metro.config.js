const { getDefaultConfig } = require('@expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

// Fix for @babel/runtime exports issue
config.resolver.extraNodeModules = {
  '@babel/runtime': path.resolve(__dirname, 'node_modules/@babel/runtime')
};

module.exports = config; 