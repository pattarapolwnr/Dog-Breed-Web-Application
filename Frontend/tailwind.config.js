/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#612BB4',
        secondary: '#9F005C',
        textPrimary: '#494949',
        textSecondary: '#9D5B9A',
        bgBorderFile: '#BDBDBD',
        bgFile: 'EFEFEF',
      },
      fontWeight: {
        lgt: '300',
        reg: '400',
        med: '500',
        sbld: '600',
        bld: '700',
      },
    },
  },
  plugins: [],
};
