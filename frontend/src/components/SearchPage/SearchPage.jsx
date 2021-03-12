import DateFnsUtils from '@date-io/date-fns';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import {
    KeyboardDatePicker,
    KeyboardTimePicker,
    MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import 'date-fns';
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { LocationWordCloud } from '../charts';
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
}));

function SearchPage() {
    const classes = useStyles();
    const [searchLocation] = useSearchLocation();
    const [selectedDate, setSelectedDate] = useState(Date.now());
    const user = useSelector((state) => state.authentication.user);
    const dispatch = useDispatch();

    const handleDateChange = (date) => {
        console.log(date);
        setSelectedDate(date);
    };

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
                            onChange={handleDateChange}
                            KeyboardButtonProps={{
                                'aria-label': 'change date',
                            }}
                        />
                    </Grid>
                    <Grid item>
                        <KeyboardTimePicker
                            margin="normal"
                            id="search-time"
                            label="Time"
                            value={selectedDate}
                            onChange={handleDateChange}
                            KeyboardButtonProps={{
                                'aria-label': 'change time',
                            }}
                        />
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
