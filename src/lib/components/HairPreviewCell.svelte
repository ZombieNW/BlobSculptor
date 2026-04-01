<script>
	let {
		name = '',
		selected = false,
		loading = false,
		errored = false,
		onclick = () => {},
		element = $bindable() // bundable for grid to track position
	} = $props();

	// Model name with fallback
	const label = $derived(name ? name.replace(/\.obj$/i, '').replace('.', ' ') : 'Unknown');
</script>

<button
	bind:this={element}
	class:border-cyan-600={selected}
	class:border-zinc-700={!selected}
	class="relative flex h-40 w-full cursor-pointer flex-col items-center justify-end
           overflow-hidden rounded-xl border-2 bg-transparent px-1 pb-2
           transition-all duration-150 ease-out"
	{onclick}
>
	<span class="pointer-events-none relative z-10 w-full truncate text-center text-sm text-zinc-300">
		{label}
	</span>
</button>
