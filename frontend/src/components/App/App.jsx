import CssBaseline from '@material-ui/core/CssBaseline';
import { makeStyles } from '@material-ui/core/styles';
import React from 'react';
import { Redirect, Route, Router, Switch } from 'react-router-dom';
import { PrivateRoute } from '../../_components';
import { history } from '../../_helpers';
import { Nav } from '../Nav';
import { OrdersPage } from '../OrdersPage';
import { Profile } from '../Profile';
import { SearchPage } from '../SearchPage';
import { SignInPage } from '../SignInPage';
import { SignUpPage } from '../SignUpPage';

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
                        <Route path="/signin" component={SignInPage} />
                        <Route path="/signup" component={SignUpPage} />
                        <PrivateRoute exact path="/" component={SearchPage} />
                        <PrivateRoute path="/search" component={SearchPage} />
                        <PrivateRoute path="/orders" component={OrdersPage} />
                        <PrivateRoute path="/profile" component={Profile} />
                        <Redirect from="*" to="/" />
                    </Switch>
                </main>
            </Router>
        </div>
    );
}

export { App };
