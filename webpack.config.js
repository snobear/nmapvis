module.exports = {
    entry: [
        './src/index.js'
    ],
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: [
                  'babel-loader',
                ]
            },
            {
              test: /\.css$/i,
              use: [
                'style-loader',
                'css-loader'
              ],
            }
        ]
    },
    output: {
        path: __dirname + '/static',
        filename: 'bundle.js'
    }
};
