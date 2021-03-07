module.exports = function override(config, env) {
    config.externals = {
        // global app config object
        Config: JSON.stringify({
            apiUrl:
                env === 'production'
                    ? 'http://localhost:9000/api'
                    : 'http://localhost:9000/api',
            apiV1Url:
                env === 'production'
                    ? 'http://localhost:9000/api/v1'
                    : 'http://localhost:9000/api/v1',
        }),
    };
    return config;
};
