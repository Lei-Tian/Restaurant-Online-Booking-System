import CssBaseline from '@material-ui/core/CssBaseline';
import { makeStyles } from '@material-ui/core/styles';
import React from 'react';
import { Redirect, Route, Router, Switch } from 'react-router-dom';
import { PrivateRoute } from '../../_components';
import { history } from '../../_helpers';
import { HomePage } from '../HomePage';
import { LoginPage } from '../LoginPage';
import { Nav } from '../Nav';
import { RegisterPage } from '../RegisterPage';

const useStyle = makeStyles((theme) => ({
    root: {
        display: 'flex',
    },
    content: {
        flexGrow: 1,
        height: '100vh',
        overflow: 'auto',
    },
    appBarSpacer: theme.mixins.toolbar,
}));

function App() {
    const classes = useStyle();
    return (
        <div className={classes.root}>
            <Router history={history}>
                <CssBaseline />
                <Nav />
                <main className={classes.content}>
                    <div className={classes.appBarSpacer} />
                    <Switch>
                        <Route path="/login" component={LoginPage} />
                        <Route path="/register" component={RegisterPage} />
                        <PrivateRoute exact path="/" component={HomePage} />
                        <Redirect from="*" to="/" />
                    </Switch>
                </main>
            </Router>
        </div>
    );
}

export { App };
