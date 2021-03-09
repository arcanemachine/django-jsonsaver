import { Role } from 'testcafe';
import * as ht from './helpersTesting.js';
import * as keys from './keys.js';

const backendUrl = ht.BACKEND_SERVER_URL;
let loginUrl = `${backendUrl}/users/login/`;

export const testUser = Role(loginUrl, async t => {
	let username = 'testcafe_user';
	let password = ht.TEST_USER_PASSWORD;

	await t.typeText('#id_username', username);
	await t.typeText('#id_password', password);
	await t.typeText('#id_captcha_1', 'PASSED');
	await t.click('#form-button-submit');
})
