import { browser } from '$app/environment';

export const backend = $state({
	api: null,
	isReady: false,
	error: null
});

// connect to backend
export async function initBackend() {
	if (!browser) return;

	const waitForApi = () => {
		return new Promise((resolve) => {
			if (window.pywebview?.api) {
				resolve(window.pywebview.api);
			} else {
				window.addEventListener(
					'pywebviewready',
					() => {
						resolve(window.pywebview.api);
					},
					{ once: true }
				);
			}
		});
	};

	try {
		backend.api = await waitForApi();
		backend.isReady = true;
	} catch (err) {
		backend.error = 'Failed to connect to Python';
		console.error(err);
	}
}

// wrap api calls
export async function getModels() {
	if (!backend.isReady) return [];
	return await backend.api.get_models_list();
}

export async function runBlenderTask(
	template_path,
	obj_path,
	output_path,
	scale,
	position,
	base_color
) {
	if (!backend.isReady) return;
	console.log(scale, position, base_color);
	return await backend.api.run_blender_task(
		template_path,
		obj_path,
		output_path,
		scale,
		position,
		base_color
	);
}
