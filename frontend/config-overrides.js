module.exports = function override(config, env) {
    config.externals = {
        // global app config object
        Config: JSON.stringify({
            apiUrl:
                env === 'production'
                    ? 'http://myservice:8000'
                    : 'http://localhost:3000',
        }),
    };
    return config;
};
