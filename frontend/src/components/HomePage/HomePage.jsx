import React from 'react';
import { useDispatch, useSelector } from 'react-redux';

function HomePage() {
    const user = useSelector((state) => state.authentication.user);
    const dispatch = useDispatch();

    return <h1>Welcome to NoMoreWait!!</h1>;
}

export { HomePage };
