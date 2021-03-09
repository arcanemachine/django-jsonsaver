import { ClientFunction, RequestLogger, Selector } from 'testcafe';

import * as ht from './helpersTesting.js'
import * as keys from './keys.js'


const backendUrl = ht.BACKEND_SERVER_URL;
let testUrl = `${backendUrl}/users/register/`;

const logger = RequestLogger({testUrl}, {
	logResponseHeaders: true
});


fixture `New User Registration`
	.page(testUrl)
	.requestHooks(logger)
	.before(() => {
		ht.localStorageSet('cookieNoticeAccepted', '1');
	});


test('sanity check', async t => {
	await t.expect(logger.contains(r => r.response.statusCode === 200)).ok()
})

test('Successful user registration and activation', async t => {
	let username = 'test_registration';
	let password = keys.TEST_USER_PASSWORD;

	const usernameField = await Selector('#id_username');
	const emailField = await Selector('#id_email');
	const password1Field = await Selector('#id_password1');
	const password2Field = await Selector('#id_password2');
	const captchaField = await Selector('#id_captcha_1');

	await t.typeText(usernameField, username);
	await t.typeText(emailField, username + '@email.com');
	await t.typeText(password1Field, password);
	await t.typeText(password2Field, password);
	await t.typeText(captchaField, 'PASSED');
	await t.click('#form-button-submit');

	// user is redirected to login view
	await t.expect(ht.getWindowLocation()).eql(`${backendUrl}/users/login/`);

	// page contains success-message-registration and success-message-registration-debug 
	const registrationSuccessMessage = (await Selector('.success-message-user-register').textContent).trim();
	const activationCode = (await Selector('.success-message-user-register-debug').textContent).trim();
	await t.expect(registrationSuccessMessage).eql('Success! Please check your email inbox for your confirmation message.');

	// navigate to activation url
	await t.navigateTo(`${backendUrl}/users/activate/${activationCode}`)

	// user is redirected to login view
	await t.expect(ht.getWindowLocation()).eql(`${backendUrl}/users/login/`);

	// success message is displayed
	const activationSuccessMessage = (await Selector('.success-message-user-activate').textContent).trim();
	await t.expect(activationSuccessMessage).eql('Account confirmed! You may now login.');

})
