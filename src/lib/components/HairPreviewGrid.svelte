<script>
	import { onMount, onDestroy, tick } from 'svelte';
	import * as THREE from 'three';
	import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
	import HairPreviewCell from './HairPreviewCell.svelte';

	let {
		modelsList = [],
		selectedModel = $bindable(),
		hairColor = '#3b1f0a',
		onselect = (_model) => {}
	} = $props();

	let canvasElement;
	let containerElement;
	let animationFrameId = -1;

	let cellsElements = $state([]);
	let cellData = [];

	let loadingSet = $state(new Set());
	let errorSet = $state(new Set());

	let renderer = null;
	const loader = new OBJLoader();
	// updates the shared material when the color changes
	// supressing svelte warning because we have an effect that resets the material as intended
	// svelte-ignore state_referenced_locally
	let sharedMaterial = new THREE.MeshStandardMaterial({
		color: hairColor,
		roughness: 0.6,
		metalness: 0.1,
		side: THREE.DoubleSide
	});

	onMount(async () => {
		// init renderer
		renderer = new THREE.WebGLRenderer({
			canvas: canvasElement,
			antialias: true,
			alpha: true,
			powerPreference: 'high-performance'
		});

		renderer.setPixelRatio(window.devicePixelRatio);
		renderer.setClearColor(0x000000, 0);

		// start animation loop
		startLoop();

		// wait for elements to instantiate before starting so positions are accurate
		await tick();

		// on destroy, stop animation loop
		return () => {
			cancelAnimationFrame(animationFrameId);
			renderer?.dispose();
		};
	});

	// rebuild models list as it changes
	$effect(() => {
		if (!renderer || !modelsList.length) return;

		// cleanup old models
		cellData.forEach((c) => c.scene.clear());

		// prep elements array
		cellsElements.length = modelsList.length;

		// make new models
		cellData = modelsList.map(() => ({
			scene: makeScene(),
			camera: makeCamera(),
			mesh: null
		}));

		startLoadingModels(modelsList);
	});

	// modify material when hair color changes
	$effect(() => {
		sharedMaterial.color.set(hairColor);
	});

	async function startLoadingModels(list) {
		for (let i = 0; i < list.length; i++) {
			if (!renderer) return;
			await loadModel(i, list[i]);

			// stagger loading so they don't all load at once
			await new Promise((r) => setTimeout(r, 20));
		}
	}

	async function loadModel(index, name) {
		loadingSet.add(name);

		try {
			const obj = await loader.loadAsync(`/assets/Mii_Hairs/${name}`);
			const box = new THREE.Box3().setFromObject(obj);
			const size = box.getSize(new THREE.Vector3());
			const center = box.getCenter(new THREE.Vector3());
			const scale = 1.3 / Math.max(size.x, size.y, size.z);

			obj.scale.setScalar(scale);
			obj.position.set(-center.x * scale, -center.y * scale, -center.z * scale);
			obj.traverse((c) => {
				if (c.isMesh) c.material = sharedMaterial;
			});

			if (cellData[index]) {
				cellData[index].mesh = obj;
				cellData[index].scene.add(obj);
			}
		} catch (e) {
			errorSet.add(name);
		} finally {
			loadingSet.delete(name);
		}
	}

	function makeScene() {
		const scene = new THREE.Scene();
		scene.add(new THREE.AmbientLight(0xffffff, 1.0));
		const dir = new THREE.DirectionalLight(0xffffff, 1.2);
		dir.position.set(2, 4, 3);
		scene.add(dir);
		return scene;
	}

	function makeCamera() {
		const cam = new THREE.PerspectiveCamera(40, 1, 0.1, 10);
		cam.position.set(0, 0, 3);
		return cam;
	}

	function startLoop() {
		const loop = () => {
			animationFrameId = requestAnimationFrame(loop);
			if (!renderer) return;
			if (!containerElement) return;

			// update canvas size
			const width = window.innerWidth;
			const height = window.innerHeight;
			if (canvasElement.width !== width || canvasElement.height !== height) {
				renderer.setSize(width, height, false);
			}

			// reset scissor
			renderer.setScissorTest(false);
			renderer.clear();
			renderer.setScissorTest(true);

			const dpr = window.devicePixelRatio;

			for (let i = 0; i < cellData.length; i++) {
				const cell = cellData[i];
				const element = cellsElements[i];

				if (!cell?.mesh || !element) continue;

				// get position relative to the screen
				const rect = element.getBoundingClientRect();

				// don't render off screen elements
				if (rect.right < 0 || rect.left > width || rect.bottom < 0 || rect.top > height) continue;

				// rotate :3
				cell.mesh.rotation.y = (Math.sin(performance.now() * 0.001) * Math.PI) / 2 + Math.PI / 2;

				// scissor
				const x = rect.left * dpr;
				const y = (height - rect.bottom) * dpr;
				const w = rect.width * dpr;
				const h = rect.height * dpr;

				renderer.setViewport(x, y, w, h);
				renderer.setScissor(x, y, w, h);

				// render
				cell.camera.aspect = rect.width / rect.height;
				cell.camera.updateProjectionMatrix();
				renderer.render(cell.scene, cell.camera);
			}
		};

		// start the loop
		loop();
	}
</script>

<div class="relative min-h-screen w-full" bind:this={containerElement}>
	<canvas
		bind:this={canvasElement}
		class="pointer-events-none fixed inset-0 z-0"
		aria-hidden="true"
	>
	</canvas>

	<div class="relative z-10 grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] gap-2.5 p-2.5">
		{#each modelsList as name, i (name)}
			<HairPreviewCell
				{name}
				selected={selectedModel === name}
				loading={loadingSet.has(name)}
				errored={errorSet.has(name)}
				onclick={() => {
					selectedModel = name;
					onselect(name);
				}}
				bind:element={cellsElements[i]}
			/>
		{/each}
	</div>
</div>
