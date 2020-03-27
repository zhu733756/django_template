module.exports = {
	outputDir: '../server/dist',
	assetsDir: 'static',
	devServer: {
		host: '0.0.0.0',
		hot: true,
		proxy: {
			'/api/*': {
				target: 'http://localhost:9000',
				// target: 'http://192.168.83.161:9000',
				changeOrigin: false,
				secure: false
			},
		}
	},
	css: {
		sourceMap: true
	}
}