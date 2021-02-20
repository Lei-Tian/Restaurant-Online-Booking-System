module.exports = function override(config, env) {
    config.externals = {
        // global app config object
        Config: JSON.stringify(
            env === 'production'
                ? { apiUrl: 'http://myservice:8000' }
                : { apiUrl: 'http://localhost:3000' },
        ),
    };
    return config;
};
