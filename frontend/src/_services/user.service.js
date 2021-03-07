import Config from 'Config';
import { authHeader } from '../_helpers';

export const userService = {
    login,
    logout,
    register,
    getAll,
    getById,
    update,
    delete: _delete,
};

function login(username, password) {
    const formBody = `username=${username}&password=${password}&grant_type=&scope=&client_id=&client_secret=`;
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        },
        body: formBody,
    };

    return fetch(`${Config.apiUrl}/token`, requestOptions)
        .then(handleResponse)
        .then((data) => {
            const user = { username, token: data.access_token };
            // store user details and jwt token in local storage to keep user logged in between page refreshes
            localStorage.setItem('user', JSON.stringify(user));
            return user;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

function getAll() {
    const requestOptions = {
        method: 'GET',
        headers: authHeader(),
    };

    return fetch(`${Config.apiV1Url}/users`, requestOptions).then(handleResponse);
}

function getById(id) {
    const requestOptions = {
        method: 'GET',
        headers: authHeader(),
    };

    return fetch(`${Config.apiV1Url}/users/${id}`, requestOptions).then(
        handleResponse,
    );
}

function register(user) {
    const formBody = `username=${user.username}&password=${user.password}`;
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        },
        body: formBody,
    };

    return fetch(`${Config.apiUrl}/signup`, requestOptions).then(
        handleResponse,
    );
}

function update(user) {
    const requestOptions = {
        method: 'PUT',
        headers: {
            ...authHeader(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
    };

    return fetch(`${Config.apiV1Url}/users/${user.id}`, requestOptions).then(
        handleResponse,
    );
}

// prefixed function name with underscore because delete is a reserved word in javascript
function _delete(id) {
    const requestOptions = {
        method: 'DELETE',
        headers: authHeader(),
    };

    return fetch(`${Config.apiV1Url}/users/${id}`, requestOptions).then(
        handleResponse,
    );
}

function handleResponse(response) {
    return response.text().then((text) => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                window.location.reload();
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}
