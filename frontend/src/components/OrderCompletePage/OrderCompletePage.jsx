import Button from '@material-ui/core/Button';
import grey from '@material-ui/core/colors/grey';
import lightBlue from '@material-ui/core/colors/lightBlue';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
import DateIcon from '@material-ui/icons/EventOutlined';
import UserIcon from '@material-ui/icons/FaceOutlined';
import PeopleIcon from '@material-ui/icons/PeopleOutlined';
import TimeIcon from '@material-ui/icons/ScheduleOutlined';
import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { axios_instance } from '../../_helpers';

const useStyles = makeStyles((theme) => ({
    root: {
        marginTop: theme.spacing(3),
        backgroundColor: 'white',
    },
    header: {
        fontSize: 26,
        fontWeight: 700,
        marginTop: theme.spacing(2),
        marginBottom: theme.spacing(2),
    },
    infoRoot: {
        border: '2px solid',
        borderColor: grey[300],
        borderRadius: '5px',
        marginBottom: theme.spacing(3),
    },
    infoHeader: {
        padding: theme.spacing(2),
        borderBottom: '2px solid',
        borderBottomColor: grey[300],
    },
    infoContent: {
        padding: theme.spacing(2),
    },
    restaurantName: {
        fontSize: 20,
        fontWeight: 700,
        color: lightBlue[600],
        marginBottom: 3,
    },
    icon: {
        fontSize: 30,
        marginRight: theme.spacing(1),
    },
    infoItem: {
        paddingTop: 6,
        fontSize: 16,
    },
    completeBtn: {
        textAlign: 'center',
        paddingBottom: theme.spacing(3),
    },
}));

function OrderCompletePage(props) {
    const classes = useStyles();
    const user = useSelector((state) => state.authentication.user);
    const [bookTime, setBookTime] = useState();
    const [partySize, setPartySize] = useState();
    const [restaurantName, setRestaurantName] = useState();

    useEffect(() => {
        const refId = props.location.pathname.split('/').slice(-1)[0];
        (async () => {
            const ret = await axios_instance.get(
                `/consumer/order-info?order_ref_id=${refId}`,
            );
            setBookTime(new Date(ret.data.booking_time));
            setPartySize(ret.data.party_size);
            setRestaurantName(ret.data.restaurant_name);
        })();
    }, [props.location.pathname]);

    return (
        <Container className={classes.root} maxWidth="md">
            <div className={classes.header}>
                Thanks! Your order has been confirm
            </div>
            <div className={classes.infoRoot}>
                <div className={classes.infoHeader}>
                    <div className={classes.restaurantName}>
                        {restaurantName}
                    </div>
                    <div>Indoor Dining Reservation</div>
                </div>
                <div className={classes.infoContent}>
                    <Grid container>
                        <Grid item>
                            <DateIcon className={classes.icon} />
                        </Grid>
                        <Grid item>
                            <div className={classes.infoItem}>
                                {bookTime && bookTime.toLocaleDateString()}
                            </div>
                        </Grid>
                    </Grid>
                    <Grid container>
                        <Grid item>
                            <TimeIcon className={classes.icon} />
                        </Grid>
                        <Grid item>
                            <div className={classes.infoItem}>
                                {bookTime && bookTime.toLocaleTimeString()}
                            </div>
                        </Grid>
                    </Grid>
                    <Grid container>
                        <Grid item>
                            <PeopleIcon className={classes.icon} />
                        </Grid>
                        <Grid item>
                            <div className={classes.infoItem}>
                                {partySize} guests for {user.username}
                            </div>
                        </Grid>
                    </Grid>
                    <Grid container>
                        <Grid item>
                            <UserIcon className={classes.icon} />
                        </Grid>
                        <Grid item>
                            <div className={classes.infoItem}>
                                {user.username}
                            </div>
                        </Grid>
                    </Grid>
                </div>
            </div>
            <div className={classes.completeBtn}>
                <Link href="/" underline="none">
                    <Button variant="contained" color="primary">
                        Return to Home
                    </Button>
                </Link>
            </div>
        </Container>
    );
}

export { OrderCompletePage };
