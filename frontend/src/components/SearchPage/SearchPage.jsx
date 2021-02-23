import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { GooglePlaceAutoComplete } from '../../_components';

const useStyles = makeStyles((theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        padding: theme.spacing(4, 4, 3),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
}));

function SearchPage() {
    const classes = useStyles();
    const [location, setLocation] = useState();
    const user = useSelector((state) => state.authentication.user);
    const dispatch = useDispatch();

    return (
        <Container maxWidth="xs">
            <div className={classes.paper}>
                <h1>Welcome to NoMoreWait!</h1>
                <GooglePlaceAutoComplete setLocation={setLocation} />
            </div>
        </Container>
    );
}

export { SearchPage };
