import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { userActions } from '../../_actions';

function HomePage() {
    const user = useSelector((state) => state.authentication.user);
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(userActions.getAll());
    }, []);

    return (
        <div className="col-lg-10 offset-lg-2">
            <h1>Welcome to NoMoreWait!!</h1>
            <p>Hi {user.username}!</p>
            <p>
                <Link to="/signin">Logout</Link>
            </p>
        </div>
    );
}

export { HomePage };
