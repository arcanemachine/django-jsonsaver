import { ClientFunction } from 'testcafe';

export const getWindowLocation = ClientFunction(() => window.location.href.toString());

export const BACKEND_SERVER_URL = 'http://192.168.1.120:8000'
