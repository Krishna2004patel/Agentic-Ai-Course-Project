/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0b1329',
          800: '#0f172a',
          700: '#1e293b',
          600: '#334155'
        },
        kle: {
          red: '#dc2626',
          darkred: '#991b1b',
          lightred: '#fee2e2'
        }
      }
    },
  },
  plugins: [],
}
