import { Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { DataGrid } from '@material-ui/data-grid';
import React, { useEffect, useState } from 'react';
import { axios_instance } from '../../_helpers';

const limit = 10;
const columns = [
    { field: 'restaurant_id', hide: true },
    { field: 'name', headerName: 'Restaurant Name', width: 230 },
    { field: 'star', headerName: 'Star', width: 80 },
    { field: 'address', headerName: 'Address', width: 300 },
    {
        field: 'available_windows',
        headerName: 'Windows',
        width: 300,
        renderCell: (params) => {
            return (
                <div>
                    {params.value.map((datetime, index) => (
                        <Button
                            variant="contained"
                            color="primary"
                            size="small"
                            style={{ marginLeft: 16 }}
                        >
                            {datetime.slice(11, 16)}
                        </Button>
                    ))}
                </div>
            );
        },
    },
];

const useStyles = makeStyles((theme) => ({
    root: {
        marginTop: theme.spacing(3),
        height: 630,
        width: '100%',
    },
}));

function RestaurantResultTable(props) {
    const classes = useStyles();
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setRows(props.data.items);
    }, []);

    const handlePageChange = (params) => {
        (async () => {
            setLoading(true);
            const link = `${props.data.links.base}?offset=${
                params.page * 10
            }&limit=${limit}`;
            const ret = await axios_instance.post(link, props.payload);
            setRows(ret.data.items);
            setLoading(false);
        })();
    };

    return (
        <div className={classes.root}>
            <DataGrid
                rows={rows}
                columns={columns}
                pagination
                pageSize={limit}
                rowCount={props.data.total}
                paginationMode="server"
                onPageChange={handlePageChange}
                loading={loading}
            />
        </div>
    );
}

export { RestaurantResultTable };
