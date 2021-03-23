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
import { useDispatch } from 'react-redux';
import { LocationWordCloud } from '../charts';
import {
    CUISINE_CHOICES,
    PARTY_SIZE_CHOICES,
    TIME_CHOICES,
} from './constantValues';
import { useSearchLocation } from './global.state';
import { LocationSearchBox } from './LocationSearchBox';

const useStyles = makeStyles((theme) => ({
    root: {
        marginTop: theme.spacing(8),
        padding: theme.spacing(4, 4, 3),
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
    iconButton: {
        textAlign: 'center',
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
    const [selectedDate, setSelectedDate] = useState(Date.now());
    const [selectedTime, setSelectedTime] = useState('ASAP');
    const [partySize, setPartySize] = useState('2 guests');
    const [cuisine, setCuisine] = useState();
    const [goodForKids, setGoodForKids] = useState();
    const [minStar, setMinStar] = useState();
    const [searchLocation] = useSearchLocation();
    const dispatch = useDispatch();

    return (
        <Container className={classes.root}>
            <h1>Welcome to NoMoreWait!</h1>
            <div>
                <LocationWordCloud />
            </div>
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
                            onChange={(e) => setSelectedDate(e.target.value)}
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
                <div className={classes.iconButton}>
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
                <div className={classes.iconButton}>
                    <Button
                        color="secondary"
                        variant="contained"
                        startIcon={<SearchIcon />}
                    >
                        Search
                    </Button>
                </div>
            </MuiPickersUtilsProvider>
        </Container>
    );
}

export { SearchPage };
