var config = require("./make-webpack-config")({
  devServer: true,
  hotComponents: true,
  devtool: "#cheap-module-eval-source-map",
  separateStylesheet: true,
  // redux_dev_tools: true,
  debug: true,
  watchOptions: {
    poll: true
  },
});
console.log(JSON.stringify(config, null, 2));
module.exports = config;
