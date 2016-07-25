var config = require('./make-webpack-config')({
  devServer: true,
  hotComponents: true,
  devtool: '#inline-source-map',
  separateStylesheet: true,
  debug: true,
  redux_dev_tools: true,
  watchOptions: {
    poll: true
  }
})
console.log(JSON.stringify(config, null, 2))
module.exports = config
