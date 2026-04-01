<script>
	import { onMount } from 'svelte';
	import { backend, initBackend, getModels } from '$lib/backend.svelte.js';
	import ControlPanelHeader from '$lib/components/ControlPanelHeader.svelte';

	let modelsList = $state([]);
	let status = $state('Initializing...');

	onMount(async () => {
		await initBackend();

		if (backend.isReady) {
			status = 'Connected!';
			modelsList = await getModels();
		} else {
			status = 'Failed!';
		}
	});

	async function handlePing() {
		const res = await backend.api.process_data('Hello from Svelte!');
		alert(res);
	}
</script>

<div class="flex h-screen w-full overflow-hidden bg-zinc-900 text-zinc-50">
	<!-- Control Panel -->
	<div class="flex h-screen w-1/5 flex-col bg-zinc-950">
		<ControlPanelHeader isReady={backend.isReady} {status} />
		<hr class="border-zinc-700" />
	</div>

	<!-- Model Viewer -->
	<div class="flex h-screen w-4/5 p-2">
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

		<!-- Bottom Center Button Panel -->
		<div class="fixed inset-x-1/2 bottom-0 flex transform justify-center p-4">
			<div class="flex gap-0.5 rounded-xl border-2 border-zinc-700 bg-zinc-700">
				<button
					class="w-32 rounded-l-xl bg-zinc-900 py-2 text-zinc-50 hover:bg-zinc-800"
					onclick={handlePing}
				>
					Hair
				</button>
				<button
					class="w-32 rounded-r-xl bg-zinc-900 py-2 text-zinc-50 hover:bg-zinc-800"
					onclick={handlePing}
				>
					Character
				</button>
			</div>
		</div>
	</div>
</div>
