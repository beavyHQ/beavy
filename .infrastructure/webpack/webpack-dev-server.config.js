module.exports = require("./make-webpack-config")({
	devServer: true,
	devtool: "#eval",
  separateStylesheet: true,
	debug: true
});
