/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          600: '#667eea',
          700: '#5568d3',
        },
        secondary: {
          50: '#f4f7ff',
          100: '#e9efff',
          200: '#d9e0ff',
        },
      },
    },
  },
  plugins: [],
}
