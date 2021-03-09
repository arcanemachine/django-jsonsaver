import { ClientFunction, RequestLogger, Selector } from 'testcafe';

import * as ht from './helpersTesting.js'
import * as keys from './keys.js'


const backendUrl = ht.BACKEND_SERVER_URL;
let testUrl = `${backendUrl}/users/login/`;

const logger = RequestLogger({testUrl}, {
	logResponseHeaders: true
});


fixture `User Login`
	.page(testUrl)
	.requestHooks(logger)
	.before(() => {
		ht.localStorageSet('cookieNoticeAccepted', '1');
	});


test('sanity check', async t => {
	await t.expect(logger.contains(r => r.response.statusCode === 200)).ok()
})

test('Successful user login', async t => {
	let username = 'testcafe_user';
	let password = keys.TEST_USER_PASSWORD;

	const usernameField = await Selector('#id_username');
	const passwordField = await Selector('#id_password');
	const captchaField = await Selector('#id_captcha_1');

	await t.typeText(usernameField, username);
	await t.typeText(passwordField, password);
	await t.typeText(captchaField, 'PASSED');
	await t.click('#form-button-submit');

	// user is redirected to users:user_detail
	await t.expect(ht.getWindowLocation()).eql(`${backendUrl}/users/me/`);

	// page contains success-message-registration and success-message-registration-debug 
	const successMessage = (await Selector('.message-item').textContent).trim();
	await t.expect(successMessage).eql("You are now logged in.");

})
