import DateFnsUtils from '@date-io/date-fns';
import Container from '@material-ui/core/Container';
import FormControl from '@material-ui/core/FormControl';
import Grid from '@material-ui/core/Grid';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import { makeStyles } from '@material-ui/core/styles';
import {
    KeyboardDatePicker,
    MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import 'date-fns';
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { LocationWordCloud } from '../charts';
import { TIME_CHOICES } from './constantValues';
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
    timeFormControl: {
        marginTop: theme.spacing(1),
    },
    timeSelectBox: {
        minWidth: 150,
    },
}));

function SearchPage() {
    const classes = useStyles();
    const [searchLocation] = useSearchLocation();
    const [selectedDate, setSelectedDate] = useState(Date.now());
    const [selectedTime, setSelectedTime] = useState('ASAP');
    const dispatch = useDispatch();

    return (
        <Container maxWidth="md" className={classes.root}>
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
                            className={classes.timeFormControl}
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
                </Grid>
            </MuiPickersUtilsProvider>
        </Container>
    );
}

export { SearchPage };
