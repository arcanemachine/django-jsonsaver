import { ClientFunction, RequestLogger, Selector } from 'testcafe';

import * as ht from './helpersTesting.js';
import * as keys from './keys.js';
import * as roles from './roles.js';


const backendUrl = ht.BACKEND_SERVER_URL;
const testUrl = `${backendUrl}/stores/new/`;

const getUrlDetail = (id) => `${backendUrl}/stores/${id}/`;
const getUrlUpdate = (id) => `${backendUrl}/stores/${id}/update/`;
const getUrlDelete = (id) => `${backendUrl}/stores/${id}/delete/`;

// create

const logger = RequestLogger({testUrl}, {
	logResponseHeaders: true
});

fixture `CRUD JSON store`
	.page(testUrl)
	.requestHooks(logger)

test('sanity check', async t => {
	await t.expect(logger.contains(r => r.response.statusCode === 200)).ok()
})

test('CRUD JSON store with no name', async t => {
	// CREATE
	
	await t.useRole(roles.testUser);
	await t.click('#form-button-submit');

	// next page contains jsonstore_create success message
	const successMessageCreate = (await Selector('.jsonstore-create-success').textContent).trim();
	await t.expect(successMessageCreate).eql('Store created successfully');


	// DETAIL

	// page title matches jsonstore_detail body_title
	await t.expect(Selector('#body-title').textContent).eql('JSON Store');

	// UPDATE

	// save current store id to json file
	const currentStoreId = (await ht.getWindowLocation()).split('/').slice(-2, -1);

	// navigate to jsonstore_update
	await t.navigateTo(getUrlUpdate(currentStoreId));

	// update data field
	let updatedData = `{"message": "${ht.TEST_MESSAGE}"}`;
	await t
		.click('#id_data')
		.pressKey('ctrl+a delete')
		.typeText('#id_data', updatedData);
	await t.click('#form-button-submit');

	// page contains jsonstore_update success message
	const successMessageUpdate = (await Selector('.message-item').textContent).trim();
	await t.expect(successMessageUpdate).eql('Store updated successfully');


	// DELETE

	// navigate to jsonstore_delete
	await t.navigateTo(getUrlDelete(currentStoreId));

	// click on the confirmation checkbox and submit the form
	await t.click('#confirm_checkbox');
	await t.click('#form-button-submit');

	// page contains jsonstore_delete success message
	const successMessageDelete = (await Selector('.jsonstore-delete-success').textContent).trim();
	await t.expect(successMessageDelete).eql('Store deleted successfully');
})
