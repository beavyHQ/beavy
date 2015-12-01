module.exports = require("./make-webpack-config")({
		// commonsChunk: true,
		longTermCaching: true,
		separateStylesheet: true,
		minimize: true,
		devtool: null,
		// devtool: 'eval-source-map'
		devtool: "#source-map"
	});
	// require("./make-webpack-config")({
	// 	prerender: true,
	// 	optimize: true,
	// 	minimize: true
	// })
;
