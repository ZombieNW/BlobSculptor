<script>
	import { onMount } from 'svelte';
	import { waitForBackend } from '$lib/pywebview';

	let response = $state('waiting for python backend...');
	let pyApi = $state(null);

	onMount(async () => {
		pyApi = await waitForBackend();
		response = 'Python backend loaded !';
	});

	async function callPython() {
		if (pyApi) {
			try {
				const result = await pyApi.get_system_info();
				response = result.message;
			} catch (err) {
				response = 'Error calling backend';
				console.error(err);
			}
		} else {
			response = 'Backend not linked yet.';
		}
	}
</script>

<button onclick={callPython} disabled={!pyApi}> Ping backend </button>

<p>Backend says: {response}</p>
