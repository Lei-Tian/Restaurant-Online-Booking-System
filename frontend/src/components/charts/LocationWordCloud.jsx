import { makeStyles } from '@material-ui/core/styles';
import React, { useEffect, useState } from 'react';
import ReactWordcloud from 'react-wordcloud';
import { axios_instance } from '../../_helpers';

const size = [1200, 285];

const useStyles = makeStyles((theme) => ({
    root: {
        maxHeight: size[1],
    },
}));

const LocationWordCloud = React.memo(() => {
    const classes = useStyles();
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

    return (
        <div className={classes.root}>
            <ReactWordcloud
                size={size}
                words={locations}
                callbacks={callbacks}
            />
        </div>
    );
});

export { LocationWordCloud };
