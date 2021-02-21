import React from 'react';
import { useDispatch, useSelector } from 'react-redux';

function OrdersPage() {
    const user = useSelector((state) => state.authentication.user);
    const dispatch = useDispatch();

    return <h1>Please see your orders history below!</h1>;
}

export { OrdersPage };
