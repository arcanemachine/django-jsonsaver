import { Selector, RequestLogger } from 'testcafe';
import * as ht from './helpersTesting.js'


const backendUrl = ht.BACKEND_SERVER_URL;
let testUrl = `${backendUrl}/users/register/`;

const logger = RequestLogger({testUrl}, {
	logResponseHeaders: true
});


fixture `New User Registration`
	.page(testUrl)
	.requestHooks(logger);

test('sanity check', async t => {
	await t.expect(logger.contains(r => r.response.statusCode === 200)).ok()
})
