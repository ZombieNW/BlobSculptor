<script>
	import { onMount } from 'svelte';
	import { backend, initBackend, getModels, runBlenderTask } from '$lib/backend.svelte.js';
	import ControlPanelHeader from '$lib/components/ControlPanelHeader.svelte';
	import HairPreviewGrid from '$lib/components/HairPreviewGrid.svelte';

	let modelsList = $state([]);
	let status = $state('Initializing...');
	let selectedModel = $state(null);
	let currentColor = $state('#3b1f0a');

	let hairYOffset = $state(0.9);
	let hairSize = $state(1.6);

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

	function hexToRgb(hex) {
		// remove hash
		hex = hex.replace(/^#/, '');

		// hex -> 0-255
		const rSrgb = parseInt(hex.substring(0, 2), 16) / 255;
		const gSrgb = parseInt(hex.substring(2, 4), 16) / 255;
		const bSrgb = parseInt(hex.substring(4, 6), 16) / 255;

		// sRGB -> Linear
		return [rSrgb, gSrgb, bSrgb].map((channel) => {
			if (channel <= 0.04045) {
				return channel / 12.92;
			}
			return Math.pow((channel + 0.055) / 1.055, 2.4);
		});
	}

	async function buildModel() {
		// TODO FIX PATH DEPENDING ON ENVIRONMENT
		const template_path = 'static/assets/Rig_V2/rig.blend';
		const hair_path = 'static/assets/Mii_Hairs/' + selectedModel;
		const output_path = 'output.blend';
		const scale = [hairSize, hairSize, hairSize];
		const position = [0.0, 0.0, hairYOffset];
		const base_color = hexToRgb(currentColor);

		const res = await runBlenderTask(
			template_path,
			hair_path,
			output_path,
			scale,
			position,
			base_color
		);
		alert('Done!');
	}
</script>

<div class="flex h-screen w-full overflow-hidden bg-zinc-900 text-zinc-50">
	<!-- Control Panel -->
	<div class="flex h-screen w-1/5 flex-col bg-zinc-950">
		<ControlPanelHeader isReady={backend.isReady} {status} />
		<hr class="border-zinc-700" />
		<div class="flex flex-col gap-2 overflow-hidden p-2">
			<div class="flex items-center">
				<h1 class="mr-2">Selected Hair</h1>
				<h3 class="mx-2 text-zinc-300">{selectedModel}</h3>
			</div>
			<div class="flex items-center">
				<h1 class="mr-2">Hair Color</h1>
				<input type="color" bind:value={currentColor} class="mx-2" />
				<h3 class="mx-2 text-zinc-300">{currentColor}</h3>
			</div>
			<div class="flex items-center">
				<h1 class="mr-2">Y Offset</h1>
				<input
					type="number"
					bind:value={hairYOffset}
					step="0.1"
					class="mx-2 w-1/3 rounded-lg border border-zinc-700 bg-zinc-900 px-2 text-center text-zinc-300 outline-none"
				/>
			</div>
			<div class="flex items-center">
				<h1 class="mr-2">Hair Size</h1>
				<input
					type="number"
					bind:value={hairSize}
					step="0.1"
					class="mx-2 w-1/3 rounded-lg border border-zinc-700 bg-zinc-900 px-2 text-center text-zinc-300 outline-none"
				/>
			</div>
		</div>
		<hr class="border-zinc-700" />
		<div class="flex flex-1 flex-col items-center justify-end gap-2 p-2">
			<button
				class="w-full rounded-lg border border-zinc-700 bg-zinc-900 py-2 hover:bg-zinc-800"
				onclick={buildModel}>Sculpt</button
			>
		</div>
	</div>

	<!-- Model Viewer -->
	<div class="flex h-screen w-4/5 overflow-y-scroll p-2">
		{#if modelsList.length > 0}
			<HairPreviewGrid
				{modelsList}
				bind:selectedModel
				hairColor={currentColor}
				onselect={(name) => console.log('picked', name)}
			/>
		{:else if backend.isReady}
			<p>No models found</p>
		{/if}

		<!-- Bottom Center Button Panel -->
		<div class="fixed inset-x-1/2 bottom-0 z-20 flex transform justify-center p-4">
			<div class="flex gap-0.5 rounded-xl border-2 border-zinc-700 bg-zinc-700">
				<button
					class="w-32 rounded-l-xl bg-zinc-950 py-2 text-zinc-50 hover:bg-zinc-900"
					onclick={handlePing}
				>
					Hair
				</button>
				<button
					class="w-32 rounded-r-xl bg-zinc-950 py-2 text-zinc-50 hover:bg-zinc-900"
					onclick={handlePing}
				>
					Character
				</button>
			</div>
		</div>
	</div>
</div>

<!-- hide number input arrows -->
<style>
	@layer utilities {
		input[type='number']::-webkit-inner-spin-button,
		input[type='number']::-webkit-outer-spin-button {
			@apply appearance-none;
		}
	}
</style>
