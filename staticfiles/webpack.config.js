const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('terser-webpack-plugin');

const baseDir = path.resolve(__dirname, "static_dirs/desktop");
const srcDir = path.resolve(baseDir, "ts");
const dstDir = path.resolve(baseDir, "wp/es5");

module.exports = {
	mode: "development",
	devtool: "source-map",
	entry: { "index": path.resolve(srcDir, "index.ts"), "index.min": path.resolve(srcDir, "index.ts") },
	/*watch: true,*/
	output: {
		filename: "[name].js",
		path: dstDir,
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
		minimizer: [ new UglifyJsPlugin({ include: /\.min\.js$/})
		]
	},
	plugins: [
        new webpack.ProvidePlugin({
           $: "jquery",
           jQuery: "jquery"
        })
    ],
    externals: {
		jquery: 'jQuery'
	},
};
