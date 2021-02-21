import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import React from 'react';
import { useSelector } from 'react-redux';

const useStyles = makeStyles((theme) => ({
    paper: {
        padding: theme.spacing(4, 4, 3),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        backgroundColor: 'white',
    },
}));

function Profile() {
    const classes = useStyles();
    const user = useSelector((state) => state.authentication.user);

    return (
        <Container maxWidth="xs">
            <div className={classes.paper}>
                <h1>username: {user.username}</h1>
            </div>
        </Container>
    );
}

export { Profile };
