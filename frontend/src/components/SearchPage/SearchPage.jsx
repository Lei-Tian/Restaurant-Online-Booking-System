import DateFnsUtils from '@date-io/date-fns';
import { IconButton } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import Collapse from '@material-ui/core/Collapse';
import Container from '@material-ui/core/Container';
import Divider from '@material-ui/core/Divider';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Grid from '@material-ui/core/Grid';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import ResetIcon from '@material-ui/icons/ClearAll';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Favorite from '@material-ui/icons/Favorite';
import FavoriteBorder from '@material-ui/icons/FavoriteBorder';
import SearchIcon from '@material-ui/icons/Search';
import Rating from '@material-ui/lab/Rating';
import {
    KeyboardDatePicker,
    MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import clsx from 'clsx';
import 'date-fns';
import React, { useState } from 'react';
import { axios_instance } from '../../_helpers';
import { LocationWordCloud } from '../charts';
import {
    CUISINE_CHOICES,
    PARTY_SIZE_CHOICES,
    TIME_CHOICES,
} from './constantValues';
import { useSearchLocation } from './global.state';
import { LocationSearchBox } from './LocationSearchBox';
import { RestaurantResultTable } from './RestaurantResultTable';

const useStyles = makeStyles((theme) => ({
    root: {
        padding: theme.spacing(0, 4, 3),
        backgroundColor: 'white',
    },
    locationSearchBox: {
        marginTop: theme.spacing(1),
    },
    requiredFieldFormControl: {
        marginTop: theme.spacing(1),
    },
    timeSelectBox: {
        minWidth: 150,
    },
    partySizeBox: {
        minWidth: 150,
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    options: {
        marginTop: theme.spacing(2),
    },
    moreButton: {
        textAlign: 'center',
    },
    iconButton: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
    },
    cuisineSelectBox: {
        minWidth: 200,
    },
    divider: {
        marginBottom: theme.spacing(2),
    },
}));

function SearchPage() {
    const classes = useStyles();
    const [expanded, setExpanded] = useState(false);
    const [selectedDate, setSelectedDate] = useState(
        new Date().toISOString().slice(0, 10),
    );
    const [selectedTime, setSelectedTime] = useState('10:00 AM');
    const [partySize, setPartySize] = useState('2 guests');
    const [cuisine, setCuisine] = useState('');
    const [goodForKids, setGoodForKids] = useState();
    const [minStar, setMinStar] = useState();
    const [location, setLocation] = useSearchLocation();
    const [searchResult, setSearchResult] = useState();
    const [searchPayload, setSearchPayload] = useState();

    const handleReset = () => {
        setSelectedDate(new Date().toISOString().slice(0, 10));
        setSelectedTime('10:00 AM');
        setPartySize('2 guests');
        setLocation('');
        setCuisine('');
        setGoodForKids(null);
        setMinStar(null);
        setSearchPayload(null);
    };

    const handleSearch = () => {
        const [city, state, country] = location.split(', ');
        const payload = {
            country,
            state,
            city,
            datetime: `${selectedDate}T${selectedTime.split(' ')[0]}:00.000Z`,
            party_size: parseInt(partySize.split(' ')[0]),
        };
        if (cuisine) payload['cuisine'] = cuisine;
        if (minStar) payload['min_star'] = minStar;
        if (goodForKids) payload['good_for_kids'] = goodForKids;
        setSearchPayload(payload);
        (async () => {
            const ret = await axios_instance.post(
                '/consumer/search?offset=0&limit=10',
                payload,
            );
            setSearchResult(ret.data);
        })();
    };

    return (
        <Container className={classes.root}>
            <h1>Welcome to NoMoreWait</h1>
            <LocationWordCloud />
            <MuiPickersUtilsProvider utils={DateFnsUtils}>
                <Grid container justify="space-around">
                    <Grid item>
                        <KeyboardDatePicker
                            variant="inline"
                            format="MM/dd/yyyy"
                            margin="normal"
                            id="search-date"
                            label="Date"
                            value={selectedDate}
                            onChange={(date) => {
                                setSelectedDate(
                                    date.toISOString().slice(0, 10),
                                );
                            }}
                            KeyboardButtonProps={{
                                'aria-label': 'change date',
                            }}
                        />
                    </Grid>
                    <Grid item>
                        <FormControl
                            variant="outlined"
                            className={classes.requiredFieldFormControl}
                        >
                            <InputLabel>Time</InputLabel>
                            <Select
                                labelId="time"
                                id="location-choice-time"
                                value={selectedTime}
                                onChange={(e) =>
                                    setSelectedTime(e.target.value)
                                }
                                label="Time"
                                className={classes.timeSelectBox}
                            >
                                {TIME_CHOICES.map((item) => (
                                    <MenuItem value={item}>{item}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item>
                        <div className={classes.locationSearchBox}>
                            <LocationSearchBox />
                        </div>
                    </Grid>
                    <Grid item>
                        <FormControl
                            variant="outlined"
                            className={classes.requiredFieldFormControl}
                        >
                            <InputLabel>Party size</InputLabel>
                            <Select
                                labelId="partysize"
                                id="partysize"
                                value={partySize}
                                onChange={(e) => setPartySize(e.target.value)}
                                label="Party size"
                                className={classes.partySizeBox}
                            >
                                {PARTY_SIZE_CHOICES.map((item) => (
                                    <MenuItem value={item}>{item}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                </Grid>
            </MuiPickersUtilsProvider>
            <div className={classes.moreButton}>
                More
                <IconButton
                    className={clsx(classes.expand, {
                        [classes.expandOpen]: expanded,
                    })}
                    onClick={() => setExpanded(!expanded)}
                    aria-expanded={expanded}
                    aria-label="show more"
                >
                    <ExpandMoreIcon />
                </IconButton>
            </div>
            <Collapse in={expanded} timeout="auto" unmountOnExit>
                <Grid
                    container
                    justify="space-around"
                    className={classes.options}
                >
                    <Grid item>
                        <FormControl variant="outlined">
                            <InputLabel>Cuisine</InputLabel>
                            <Select
                                labelId="cuisine"
                                id="cuisine"
                                value={cuisine}
                                onChange={(e) => setCuisine(e.target.value)}
                                label="Cuisine"
                                className={classes.cuisineSelectBox}
                            >
                                {CUISINE_CHOICES.map((item) => (
                                    <MenuItem value={item}>{item}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item>
                        <Box
                            component="fieldset"
                            mb={3}
                            borderColor="transparent"
                        >
                            <Typography component="legend">
                                Min Stars
                            </Typography>
                            <Rating
                                name="star-rating"
                                value={minStar}
                                onChange={(event, newValue) => {
                                    setMinStar(newValue);
                                }}
                            />
                        </Box>
                    </Grid>
                    <Grid item>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    icon={<FavoriteBorder />}
                                    checkedIcon={<Favorite />}
                                    onChange={(event) =>
                                        setGoodForKids(event.target.checked)
                                    }
                                    name="goodForKids"
                                />
                            }
                            label="Good for Kids"
                        />
                    </Grid>
                </Grid>
            </Collapse>
            <Divider className={classes.divider} />
            <Grid container justify="center">
                <Grid item>
                    <div className={classes.iconButton}>
                        <Button
                            color="secondary"
                            variant="contained"
                            startIcon={<SearchIcon />}
                            onClick={handleSearch}
                        >
                            Search
                        </Button>
                    </div>
                </Grid>
                <Grid item>
                    <div className={classes.iconButton}>
                        <Button
                            variant="contained"
                            startIcon={<ResetIcon />}
                            onClick={handleReset}
                        >
                            Reset
                        </Button>
                    </div>
                </Grid>
            </Grid>
            {searchResult && (
                <RestaurantResultTable
                    data={searchResult}
                    payload={searchPayload}
                />
            )}
        </Container>
    );
}

export { SearchPage };
