module.exports = require("./make-webpack-config")({
	devServer: true,
	hotComponents: true,
	devtool: "source-map",
  separateStylesheet: true,
	debug: true
});
