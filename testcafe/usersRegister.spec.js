import { Selector, RequestLogger } from 'testcafe';
import * as ht from './helpersTesting.js'


const backendUrl = ht.BACKEND_SERVER_URL;
let testUrl = `${backendUrl}/`;

const logger = RequestLogger({testUrl}, {
	logResponseHeaders: true
});


fixture `New User Registration`
