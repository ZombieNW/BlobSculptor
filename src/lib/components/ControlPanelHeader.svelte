<script>
	const { isReady, status } = $props();
</script>

<div class="my-2 flex items-center justify-center overflow-hidden">
	<h1 class="text-xl font-bold">BlobSculptor</h1>
	{#if isReady}
		<span class="mx-2 h-4 w-4 rounded-full bg-emerald-600"></span>
	{:else}
		<span class="mx-2 h-4 w-4 rounded-full bg-rose-600"></span>
	{/if}
	<h3 class="text-zinc-300" title="Python Backend connection status">{status}</h3>
</div>
