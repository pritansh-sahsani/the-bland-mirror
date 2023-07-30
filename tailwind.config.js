/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./main/templates/*.html"],
  theme: {
    screens: {
      960: "960px",
      md: "800px",
      sm: "640px", 
      xsm: "500px",
    },
    borderWidth: {
      0.5: "0.5px",
    },
    extend: {
      colors: {
        customblue: "#007bff",
      },
      inset: {
        "1%": "1%",
        "2%": "2%",
        "5%": "5%",
        "25%": "25%",
      },
      height: {
        "10%": "10%",
        "50%": "50%",
        "70%": "70%",
        "75%": "75%",
        "80%": "80%",
        "90%": "90%",
      },
      width: {
        "3%": "3%",
        "10%": "10%",
        "12%": "12%",
        "20%": "20%",
        "22%": "22%",
        "25%": "25%",
        "30%": "30%",
        "47.5%": "47.5%",
        "57%": "57%",
        "50%": "50%",
        "70%": "70%",
        "75%": "75%",
        "80%": "80%",
        "90%": "90%",
        "95%": "95%",
        "98%": "98%",
        "100%": "100%",
      },
      margin:{
        '1%': '1%',
        '2%':'2%',
        '3%': '3%',
        "4%": "4%",
        "4.5%": "4.5%",
        "5%":"5%", 
        "7.5%": "7.5%",
        "10%": "10%",
        "15%": "15%",
        "35%": "35%",
        "40%": "40%",
      },
      padding:{
        "1%": "1%",
      },
    },
  },
  plugins: [],
}
