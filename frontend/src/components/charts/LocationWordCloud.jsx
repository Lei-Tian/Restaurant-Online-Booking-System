import React, { useEffect, useState } from 'react';
import ReactWordcloud from 'react-wordcloud';
import { axios_instance } from '../../_helpers';

function LocationWordCloud() {
    const [locations, setLocations] = useState([]);

    useEffect(() => {
        axios_instance
            .get('/consumer/location-restaurants-count')
            .then((res) => {
                setLocations(res.data);
            });
    }, []);

    return <ReactWordcloud words={locations} />;
}

export { LocationWordCloud };
