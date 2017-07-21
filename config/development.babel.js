const path = require("path")
const Webpack = require("webpack")

const BASE = path.join(__dirname, "..")
const ROOT = path.join(BASE, "react-apps")
const STATIC = path.join(BASE, "static")

modules.exports = {
  devtool: "cheap-module-eval-source-map",

  entry: {
    index: [
      "whatwg-fetch",
      path.join(ROOT, "list", "index.js")
    ]
  },

  output: {
    path: STATIC,
    publicPath: "/static/",
    filename: "[name].js"
  },

  resolve: {
    extensions: [".js"],
    modules: [
      ROOT,
      path.resolve(ROOT, "list"),
      path.resolve(BASE, "node_modules")
    ]
  },

  module: {
    loaders: [
      {
        test: /\.js$/,
        include: ROOT,
        loader: "babel-loader"
      }
    ]
  },

  stats: {
    colors: true,
    reasons: true,
    chunks: false
  },

  plugins: [
    new Webpack.HotModuleReplacementPlugin(),
    new Webpack.NoEmitOnErrorsPlugin()
  ],

  devServer: {
    contentBase: STATIC,
    inline: true,
    publicPath: "/static/",
    hot: true
  }
}
