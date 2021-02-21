import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import CircularProgress from '@material-ui/core/CircularProgress';
import Container from '@material-ui/core/Container';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useLocation } from 'react-router-dom';
import { alertActions, userActions } from '../../_actions';

const useStyles = makeStyles((theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        padding: theme.spacing(4, 4, 3),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        backgroundColor: 'white',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(0, 0, 2),
    },
    circularProgress: {
        marginLeft: theme.spacing(2),
    },
    register: {
        margin: theme.spacing(0, 0, 1),
    },
    loginAlert: {
        padding: theme.spacing(1),
        backgroundColor: '#ffcdd2',
        color: '#b71c1c',
    },
}));

function LoginPage() {
    const classes = useStyles();
    const [inputs, setInputs] = useState({
        username: '',
        password: '',
    });
    const { username, password } = inputs;
    const loggingIn = useSelector((state) => state.authentication.loggingIn);
    const alert = useSelector((state) => state.alert);
    const dispatch = useDispatch();
    const location = useLocation();

    // reset login status
    useEffect(() => {
        dispatch(userActions.logout());
        return () => {
            // clear alert on location change
            dispatch(alertActions.clear());
        };
    }, []);

    function handleChange(e) {
        const { name, value } = e.target;
        setInputs((inputs) => ({ ...inputs, [name]: value }));
    }

    function handleSubmit(e) {
        e.preventDefault();

        if (username && password) {
            // get return url from location state or default to home page
            const { from } = location.state || { from: { pathname: '/' } };
            dispatch(userActions.login(username, password, from));
        }
    }

    return (
        <Container maxWidth="xs">
            <div className={classes.paper}>
                <Avatar className={classes.avatar}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign in
                </Typography>
                <form
                    className={classes.form}
                    noValidate
                    onSubmit={handleSubmit}
                >
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoFocus
                        onChange={handleChange}
                    />
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        autoComplete="current-password"
                        onChange={handleChange}
                    />
                    <FormControlLabel
                        control={<Checkbox value="remember" color="primary" />}
                        label="Remember me"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                    >
                        Sign In
                    </Button>
                    <Grid container className={classes.register}>
                        <Grid item>
                            <Link to="/register">
                                {"Don't have an account? Sign Up"}
                            </Link>
                        </Grid>
                        <Grid item className={classes.circularProgress}>
                            {loggingIn && (
                                <CircularProgress size={25} color="secondary" />
                            )}
                        </Grid>
                    </Grid>
                    {alert.message && (
                        <div className={classes.loginAlert}>
                            {alert.message}
                        </div>
                    )}
                </form>
            </div>
        </Container>
    );
}

export { LoginPage };
