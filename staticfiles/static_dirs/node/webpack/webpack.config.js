const path = require('path');
const UglifyJsPlugin = require('terser-webpack-plugin');

module.exports = {
  mode: "development",
  devtool: "source-map",
  entry: { "index": "../desktop/ts/AppMain.ts", "index.min": "../desktop/ts/AppMain.ts" },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, '../desktop/wp/es5/'),
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
  },
  optimization: {
    minimize: true,
    minimizer: [new UglifyJsPlugin({
      include: /\.min\.js$/
    })]
  }
};
