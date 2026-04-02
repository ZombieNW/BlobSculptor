<script>
	import { onMount } from 'svelte';
	import { backend, initBackend, getModels, runBlenderTask } from '$lib/backend.svelte.js';
	import ControlPanelHeader from '$lib/components/ControlPanelHeader.svelte';
	import HairPreviewGrid from '$lib/components/HairPreviewGrid.svelte';

	// Program state
	let currentTab = $state('hair');
	let blenderLogs = $state(['No Blender Task Running...']);
	let modelsList = $state([]);
	let status = $state('Initializing...');

	// Model State
	let selectedModel = $state(null);
	let currentColor = $state('#3b1f0a');
	let hairYOffset = $state(0.9);
	let hairSize = $state(1.6);

	onMount(async () => {
		await initBackend();

		if (backend.isReady) {
			status = 'Connected!';
			modelsList = await getModels();
			selectedModel = modelsList[0];
		} else {
			status = 'Failed!';
		}

		window.onBlenderLog = (message) => {
			blenderLogs.push(message);
		};
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
		currentTab = 'logs';

		blenderLogs = ['Starting Blender task...'];

		const isProd = import.meta.env.PROD;
		const base = isProd ? 'build/assets' : 'static/assets';

		const template_path = `${base}/Rig_V2/rig.blend`;
		const hair_path = `${base}/Mii_Hairs/${selectedModel}`;
		const output_path = 'output.blend';

		const scale = [hairSize, hairSize, hairSize];
		const position = [0.0, 0.0, hairYOffset];
		const base_color = hexToRgb(currentColor);

		try {
			const res = await runBlenderTask(
				template_path,
				hair_path,
				output_path,
				scale,
				position,
				base_color
			);
			console.log('Backend response:', res);
		} catch (err) {
			console.error('Blender Task Failed:', err);
		}
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
	<div class="relative flex h-screen w-4/5 flex-col">
		<div class="flex-1 overflow-y-auto p-4">
			<!-- Hair Preview -->
			<div class="h-full" class:hidden={currentTab !== 'hair'}>
				{#if modelsList.length > 0}
					<HairPreviewGrid
						{modelsList}
						bind:selectedModel
						hairColor={currentColor}
						onselect={(name) => console.log('picked', name)}
					/>
				{:else if backend.isReady}
					<p class="text-zinc-500">No models found</p>
				{/if}
			</div>

			<!-- Blender Logs -->
			<div class="h-full font-mono text-sm" class:hidden={currentTab !== 'logs'}>
				<div class="h-full overflow-y-auto rounded border border-zinc-800 bg-black p-4">
					{#each blenderLogs as log}
						{#if log.toLowerCase().includes('error')}
							<div class="border-b border-zinc-800 py-1 text-rose-600">> {log}</div>
						{:else}
							<div class="border-b border-zinc-800 py-1 text-emerald-600">> {log}</div>
						{/if}
					{/each}
				</div>
			</div>

			<!-- Character Preview -->
			<div class="h-full" class:hidden={currentTab !== 'character'}>
				<div class="flex h-full items-center justify-center text-zinc-600">
					Character Preview Go Here Soon
				</div>
			</div>
		</div>

		<!-- Tab Selector -->
		<div class="pointer-events-none absolute inset-x-0 bottom-8 flex justify-center">
			<div
				class="pointer-events-auto z-20 flex gap-1 rounded-xl border border-zinc-700 bg-zinc-950 p-1 shadow-2xl"
			>
				{#each ['hair', 'logs', 'character'] as tab}
					<button
						class="w-32 rounded-lg py-2 transition-all duration-150 ease-out hover:cursor-pointer hover:bg-zinc-800"
						class:bg-zinc-800={currentTab === tab}
						class:text-white={currentTab === tab}
						class:text-zinc-500={currentTab !== tab}
						onclick={() => (currentTab = tab)}
					>
						{tab.charAt(0).toUpperCase() + tab.slice(1)}
					</button>
				{/each}
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
