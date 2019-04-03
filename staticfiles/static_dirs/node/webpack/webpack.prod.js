const path = require('path');

module.exports = {
  mode: "production",
  devtool: "source-map",
  entry: "../desktop/ts/AppMain.ts",
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, '../desktop/wp/js/'),
  },
  resolve: {
    // Add `.ts` and `.tsx` as a resolvable extension.
    extensions: [".ts", ".tsx", ".js"]
  },
  module: {
    rules: [
      // all files with a `.ts` or `.tsx` extension will be handled by `ts-loader`
      { test: /\.ts$/, loader: "ts-loader" }
    ]
  }
};
