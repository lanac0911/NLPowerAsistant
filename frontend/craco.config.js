const path = require('path');

module.exports = {
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@styles': path.resolve(__dirname, 'src/styles'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@screen': path.resolve(__dirname, 'src/screen'),
      '@utils': path.resolve(__dirname, 'src/utils'),

    },
  },
};
