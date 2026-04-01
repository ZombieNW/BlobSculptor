<script>
	import { onMount } from 'svelte';
	import { backend, initBackend, getModels } from '$lib/backend.svelte.js';

	let modelsList = $state([]);
	let status = $state('Initializing...');

	onMount(async () => {
		await initBackend();

		if (backend.isReady) {
			status = 'Connected to Python Backend';
			modelsList = await getModels();
		} else {
			status = 'Connection failed.';
		}
	});

	async function handlePing() {
		const res = await backend.api.process_data('Hello from Svelte!');
		alert(res);
	}
</script>

<h2>Backend Status: {status}</h2>

<button onclick={handlePing} disabled={!backend.isReady}> Ping Python </button>

{#if modelsList.length > 0}
	<h3>Available Models:</h3>
	<ul>
		{#each modelsList as model}
			<li>{model}</li>
		{/each}
	</ul>
{:else if backend.isReady}
	<p>No .obj models found in assets folder.</p>
{/if}
