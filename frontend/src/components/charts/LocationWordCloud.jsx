import React, { useEffect, useState } from 'react';
import ReactWordcloud from 'react-wordcloud';
import { axios_instance } from '../../_helpers';

const LocationWordCloud = React.memo(() => {
    const [locations, setLocations] = useState([]);
    const callbacks = {
        getWordTooltip: (word) => `${word.text}`,
    };

    useEffect(() => {
        axios_instance
            .get('/consumer/location-restaurants-count')
            .then((res) => {
                const ret = res.data.map((item) => ({
                    text: item.city,
                    value: Math.floor(item.restaurant_count / 100) + 10,
                }));
                setLocations(ret);
            });
    }, []);

    return <ReactWordcloud words={locations} callbacks={callbacks} />;
});

export { LocationWordCloud };
