import React from 'react';
import { useSelector } from 'react-redux';

function OrderCompletePage() {
    const user = useSelector((state) => state.authentication.user);

    return <h1>Please see your orders history below!</h1>;
}

export { OrderCompletePage };
