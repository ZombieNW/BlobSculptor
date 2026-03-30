export function waitForBackend() {
	return new Promise((resolve) => {
		if (window.pywebview && window.pywebview.api) {
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
}
