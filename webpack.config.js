const path = require("path");
const { existsSync } = require("fs");

// Set the entrypoint to main.jsx by default, but main.tsx if using TypeScript.
let entry = "./PastForward/js/main.jsx";
if (existsSync("./PastForward/js/main.tsx")) {
  entry = "./PastForward/js/main.tsx";
}

module.exports = {
  mode: "development",
  entry,
  output: {
    path: path.join(__dirname, "/PastForward/static/js/"),
    filename: "bundle.js",
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        // Exclude external modules from loader tests
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-env", "@babel/preset-react"],
          plugins: ["@babel/transform-runtime"],
        },
      },
      {
        // Support for TypeScript in optional .ts or .tsx files
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx", ".ts", ".tsx"],
  },
};
