import { useDispatch, useSelector } from 'react-redux';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import React, { useEffect, useState } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import clsx from 'clsx';
import { axios_instance } from '../../_helpers';

const useStyles = makeStyles((theme) => ({
    root: {
        marginTop: theme.spacing(3),
        backgroundColor: 'white',
    },
    header: {
        fontSize: 26,
        fontWeight: 700,
        marginLeft: theme.spacing(2),
        marginTop: theme.spacing(2),
        marginBottom: theme.spacing(5),
    },
    headerUser: {
        color: '#26c6da',
    },
    table: {
        minWidth: 650,
    },
    completeStatus: {
        color: '#4caf50',
    },
    pendingStatus: {
        color: '#ffb300',
    },
    cancelledStatus: {
        color: '#757575',
    },
}));

function createData(name, calories, fat, carbs, protein) {
    return { name, calories, fat, carbs, protein };
}

const rows = [
    createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
    createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
    createData('Eclair', 262, 16.0, 24, 6.0),
    createData('Cupcake', 305, 3.7, 67, 4.3),
    createData('Gingerbread', 356, 16.0, 49, 3.9),
];

function OrdersPage() {
    const classes = useStyles();
    const user = useSelector((state) => state.authentication.user);
    const [fetchOrderHistory, setFetchOrderHistory] = useState(false);
    const [rows, setRows] = useState([]);

    useEffect(() => {
        setFetchOrderHistory(true);
    }, []);

    useEffect(() => {
        if (fetchOrderHistory) {
            (async () => {
                const ret = await axios_instance.get('/consumer/order-history');
                setRows(ret.data);
                setFetchOrderHistory(false);
            })();
        }
    }, [fetchOrderHistory]);

    const handleCancel = (e) => {
        (async () => {
            const ret = await axios_instance.post('/consumer/cancel-order', {
                ref_id: e.currentTarget.value,
            });
            setFetchOrderHistory(true);
        })();
    };

    return (
        <Container className={classes.root} maxWidth="md">
            <div className={classes.header}>
                Hi <span className={classes.headerUser}>{user.username}</span>,
                please see your orders below
            </div>
            <div>
                <Table className={classes.table} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>BookingTime</TableCell>
                            <TableCell>Restaurant</TableCell>
                            <TableCell>Party Size</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Action</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows.map((row) => {
                            const datetime = new Date(row.booking_time);
                            const bookingTime = `${datetime.toLocaleDateString()} ${datetime.toLocaleTimeString()}`;
                            const btnDisabled =
                                row.status === 'CANCELLED' ? true : false;
                            const statusStyle =
                                row.status === 'COMPLETE'
                                    ? classes.completeStatus
                                    : row.status === 'PENDING'
                                    ? classes.pendingStatus
                                    : classes.cancelledStatus;
                            return (
                                <TableRow key={row.name}>
                                    <TableCell>{bookingTime}</TableCell>
                                    <TableCell>{row.restaurant_name}</TableCell>
                                    <TableCell>{row.party_size}</TableCell>
                                    <TableCell className={statusStyle}>
                                        {row.status}
                                    </TableCell>
                                    <TableCell>
                                        <Button
                                            variant="contained"
                                            color="secondary"
                                            disabled={btnDisabled}
                                            value={row.ref_id}
                                            onClick={handleCancel}
                                        >
                                            Cancel
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            );
                        })}
                    </TableBody>
                </Table>
            </div>
        </Container>
    );
}

export { OrdersPage };
