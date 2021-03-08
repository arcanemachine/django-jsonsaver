import { Selector, RequestLogger } from 'testcafe';
import * as ht from './helpersTesting.js'


const backendUrl = ht.BACKEND_SERVER_URL;
let testUrl = `${backendUrl}`;

const logger = RequestLogger({testUrl}, {
	logResponseHeaders: true
});


fixture `Homepage`
	.page(testUrl)
	.requestHooks(logger);


test('Page returns 200', async t => {
	await t
		.expect(logger.contains(r => r.response.statusCode === 200))
		.ok();
})

test('First-time viewer sees cookie notice', async t => {
	const cookieNoticeExists = await Selector('#cookie-notice').exists;
	await t.expect(cookieNoticeExists).ok();
})

test('Cookie notice permanently disappears after clicking "I understand" button', async t => {
	// cookie notice is visible before accepting
	const cookieNotice = await Selector('#cookie-notice');
	await t.expect(cookieNotice.getStyleProperty('display')).eql('block');

	// click "I understand" button
	const cookieNoticeAccept = await Selector('#cookie-notice-accept');
	await t.click('#cookie-notice-accept');

	// cookie notice is no longer visible
	await t.expect(cookieNotice.getStyleProperty('display')).eql('none');

	// reload the page
	await t.eval(() => location.reload(true));

	// cookie notice is still not visible
	await t.expect(cookieNotice.getStyleProperty('display')).eql('none');
})
