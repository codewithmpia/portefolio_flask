/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../contents/**/*.html",
    "../contents/**/*.py",
    "../*.py",
  ],
  theme: {
    fontFamily: {
      jetbrains: ["JetBrains Mono", "serif"],
    }
  }
};
