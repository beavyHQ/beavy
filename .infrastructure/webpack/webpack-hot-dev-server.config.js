var config = require('./make-webpack-config')({
  devServer: true,
  hotComponents: true,
  devtool: '#inline-source-map',
  separateStylesheet: true,
  debug: true
})
console.log(JSON.stringify(config, null, 2))
module.exports = config
