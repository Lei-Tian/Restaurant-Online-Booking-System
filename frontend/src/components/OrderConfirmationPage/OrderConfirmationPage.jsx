import React from 'react';
import { useSelector } from 'react-redux';

function OrderConfirmationPage() {
    const user = useSelector((state) => state.authentication.user);
    debugger;

    return <h1>Please see your orders history below!</h1>;
}

export { OrderConfirmationPage };
