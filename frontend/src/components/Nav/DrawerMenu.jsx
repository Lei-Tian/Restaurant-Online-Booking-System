import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import { makeStyles } from '@material-ui/core/styles';
import HistoryIcon from '@material-ui/icons/History';
import SearchIcon from '@material-ui/icons/Search';
import React from 'react';

const useStyle = makeStyles((theme) => ({
    listIcon: {
        minWidth: 40,
    },
}));

function DrawerMenu() {
    const classes = useStyle();

    return (
        <div>
            <ListItem button>
                <ListItemIcon className={classes.listIcon}>
                    <SearchIcon />
                </ListItemIcon>
                <ListItemText primary="Search" />
            </ListItem>
            <ListItem button>
                <ListItemIcon className={classes.listIcon}>
                    <HistoryIcon />
                </ListItemIcon>
                <ListItemText primary="Orders" />
            </ListItem>
        </div>
    );
}

export { DrawerMenu };
