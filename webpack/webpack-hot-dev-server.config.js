module.exports = require("./make-webpack-config")({
	devServer: true,
	hotComponents: true,
	devtool: "source-map",
  separateStylesheet: true,
  redux_dev_tools: true,
	debug: true
});
