import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import { makeStyles } from '@material-ui/core/styles';
import HistoryIcon from '@material-ui/icons/History';
import SearchIcon from '@material-ui/icons/Search';
import React from 'react';
import { Link } from 'react-router-dom';

const useStyle = makeStyles((theme) => ({
    listIcon: {
        minWidth: 40,
    },
}));

function DrawerMenu() {
    const classes = useStyle();

    return (
        <List>
            <ListItem button component={Link} to="/search">
                <ListItemIcon className={classes.listIcon}>
                    <SearchIcon />
                </ListItemIcon>
                <ListItemText primary="Search" />
            </ListItem>
            <ListItem button component={Link} to="/orders">
                <ListItemIcon className={classes.listIcon}>
                    <HistoryIcon />
                </ListItemIcon>
                <ListItemText primary="Orders" />
            </ListItem>
        </List>
    );
}

export { DrawerMenu };
