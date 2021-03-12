import axios from 'axios';
import Config from 'Config';
import { authHeader } from './auth-header';

export const axios_instance = axios.create({
    baseURL: Config.apiV1Url,
    headers: authHeader(),
});
