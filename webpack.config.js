/*
 * Webpack development server configuration
 *
 * This file is set up for serving the webpack-dev-server, which will watch for changes and recompile as required if
 * the subfolder /webpack-dev-server/ is visited. Visiting the root will not automatically reload.
 */
'use strict';
var webpack = require('webpack');

module.exports = {

  output: {
    filename: '[name].js',
    path: 'assets/',
  },


  cache: true,
  debug: true,
  devtool: false,
  entry: {
      'main':
        ['./jsbeavy/main.jsx'],
    },

  stats: {
    colors: true,
    reasons: true
  },

  resolve: {
    extensions: ['', '.js', '.jsx'],
    alias: {
    }
  },
  module: {
    noParse: /lie\.js$|\/leveldown\//,
    preLoaders: [{
      test: '\\.js$',
      exclude: 'node_modules',
      loader: 'jsxhint'
    }],
    loaders: [{
      test: /\.jsx$/,
      exclude: 'node_modules',
      loader: 'babel-loader?optional=runtime'
    },{
      test: /\.json/,
      loader: 'json'
    },{
      test: /\.less/,
      loader: 'style-loader!css-loader!less-loader'
    },{
      test: /\.sass/,
      loader: 'style-loader!css-loader!sass-loader?outputStyle=expanded'
    },{
      test: /\.css$/,
      loader: 'style-loader!css-loader'
    },{
      test: /\.(png|jpg)$/,
      loader: 'url-loader?limit=8192'
    },{
      test: /\.gif/,
      loader: "url-loader?limit=10000&minetype=image/gif"
    },{
      test: /\.woff([0-9]*)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
      loader: "url-loader?limit=10000&minetype=application/font-woff"
    },{
      test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
      loader: "file-loader"
    }]
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],

  devServer: {
    contentBase: "./assets/",
    publicPath: "/assets/",
    proxy : {"*": "http://127.0.0.1:5000/"},
    hot: true,
    progress: true,
    stats: {colors: true, }
  }

};
