const forms = require('@tailwindcss/forms');

module.exports = {
  content: [
    './**/*.html',
    './**/*.js'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#002468',
        'background-light': '#f5f6f8',
        'background-dark': '#0f1623'
      },
      fontFamily: { display: ['Sora'] },
      borderRadius: { DEFAULT: '0.125rem', lg: '0.25rem', xl: '0.5rem', full: '0.75rem' }
    }
  },
  plugins: [forms]
};
