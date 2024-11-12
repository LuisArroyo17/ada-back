/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html", // Incluye el archivo HTML principal
    "./src/**/*.{js,ts,jsx,tsx,html}", // Incluye archivos en src/
    "./templates/**/*.html", // Incluye plantillas Flask
    "./static/**/*.js" // Opcionalmente, incluye JS en static/
  ],
  theme: {
    extend: {
      colors: {
        richblack: '#0C161D',
        rickblackClaro: '#12212B',
        columbiablue: '#BFDBF7',
        ligthgreen: '#96F08C',
        greenhover: '#7BEC6F',
        firered: '#D61F22',
        redhover: '#B3191C',
        lapislazuli: '#2F6690',
      },
    },
  },
  plugins: [],
}
