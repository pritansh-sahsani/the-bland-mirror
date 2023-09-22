/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./main/templates/*.html"],
  theme: {
    screens: {
      1180:"1180px",
      960: "960px",
      880: "880px",
      md: "800px",
      725: "725px",
      sm: "640px", 
      xsm: "500px",
    },
    extend: {
      borderWidth: {
        0.5: "0.5px",
      },  
      space: {
        '5%': '5%',
      },
      colors: {
        customblue: "#007bff",
      },
      inset: {
        "1%": "1%",
        "2%": "2%",
        "5%": "5%",
        "7%": "7%",
        "12%": "12%",
        "25%": "25%",
        "50%": "50%",
      },
      height: {
        "15":"4rem",
        
        "10%": "10%",
        "50%": "50%",
        "70%": "70%",
        "75%": "75%",
        "80%": "80%",
        "90%": "90%",
      },
      width: {
        "15":"4rem",
        "4.25rem":"4.25rem",
        "17rem":"17rem",
        "22rem":"22rem",
        "26rem":"26rem",
        "34rem":"34rem",

        "3%": "3%",
        "10%": "10%",
        "12%": "12%",
        "20%": "20%",
        "22%": "22%",
        "25%": "25%",
        "30%": "30%",
        "33%": "33%",
        "40%": "40%",
        "47.5%": "47.5%",
        "57%": "57%",
        "50%": "50%",
        "70%": "70%",
        "75%": "75%",
        "80%": "80%",
        "85%": "85%",
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
        "30%": "30%",
        "35%": "35%",
        "40%": "40%",
        "50%": "50%",

        '0.65rem': '0.65rem',
        '0.7rem': '0.7rem',
        "1.09rem": "1.09rem",
        "1.87rem": "1.87rem",
        "2.25rem": "2.25rem",
        "2.6rem": "2.6rem",
        "3.75rem": "3.75rem",
      },
      padding:{
        "1%": "1%",
      },
      fontSize: {
        "12rem": "12rem",
      },
      colors:{
        "gradient":"#003764",
        "main": "white",
        "antimain": "#1a1a1d",
      },maxHeight: {
        '50%': '50%',
      } 
    },
  },
  plugins: [],
}
