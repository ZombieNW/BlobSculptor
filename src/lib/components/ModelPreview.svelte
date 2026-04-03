<script>
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
	import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
	import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

	// Keep props as a single object for better reactivity tracking
	let props = $props();
	let container = $state();
	let scene, camera, renderer, controls, hairGroup;
	let currentHairObject = $state(null);

	// reactive stuff
	$effect(() => {
		if (currentHairObject) {
			currentHairObject.position.set(...props.hairPosition);
			currentHairObject.scale.set(...props.hairScale);

			currentHairObject.traverse((child) => {
				if (child.isMesh) child.material.color.set(props.hairColor);
			});
		}
	});

	$effect(() => {
		if (props.hairModel && scene) loadHair(props.hairModel);
	});

	// load hair from name
	async function loadHair(name) {
		if (!hairGroup) return;
		while (hairGroup.children.length > 0) hairGroup.remove(hairGroup.children[0]);

		const loader = new OBJLoader();
		loader.load(`/assets/Mii_Hairs/${name}`, (obj) => {
			obj.traverse((child) => {
				if (child instanceof THREE.Mesh) {
					child.rotation.set(0, Math.PI / 2, 0);

					child.material = new THREE.MeshStandardMaterial({
						color: props.hairColor,
						side: THREE.DoubleSide
					});
				}
			});

			obj.position.set(...props.hairPosition);
			obj.scale.set(...props.hairScale);

			hairGroup.add(obj);
			currentHairObject = obj;
		});
	}

	onMount(() => {
		scene = new THREE.Scene();
		scene.background = new THREE.Color('#222');

		// setup camera
		camera = new THREE.PerspectiveCamera(
			75,
			container.clientWidth / container.clientHeight,
			0.1,
			1000
		);
		camera.position.set(0, 1.6, 4);

		// add reference grid to scene
		const grid = new THREE.GridHelper(10, 10, 0x444444, 0x888888);
		scene.add(grid);

		// setup renderer
		renderer = new THREE.WebGLRenderer({ antialias: true });
		renderer.setPixelRatio(window.devicePixelRatio);
		container.appendChild(renderer.domElement);

		// setup controls
		controls = new OrbitControls(camera, renderer.domElement);
		controls.enableDamping = true;
		controls.target.set(0, 1, 0);

		// setup lights
		const light = new THREE.DirectionalLight(0xffffff, 1);
		light.position.set(2, 2, 5);
		scene.add(light, new THREE.AmbientLight(0xffffff, 0.6));

		// add rig
		const gltfLoader = new GLTFLoader();
		gltfLoader.load('/assets/Rig_V2/rig.glb', (gltf) => scene.add(gltf.scene));

		// add hair group
		hairGroup = new THREE.Group();
		scene.add(hairGroup);

		// resizing logic
		const resizeObserver = new ResizeObserver(() => {
			if (!container) return;
			camera.aspect = container.clientWidth / container.clientHeight;
			camera.updateProjectionMatrix();
			renderer.setSize(container.clientWidth, container.clientHeight);
		});
		resizeObserver.observe(container);

		// animation loop
		let frame;
		const animate = () => {
			frame = requestAnimationFrame(animate);
			if (controls) controls.update();
			renderer.render(scene, camera);
		};
		animate();

		// things to do when component is destroyed
		return () => {
			cancelAnimationFrame(frame);
			resizeObserver.disconnect();
			renderer.dispose();
			controls.dispose();
		};
	});
</script>

<div
	bind:this={container}
	class="relative block h-screen w-full overflow-hidden bg-neutral-900"
></div>

<style>
	div :global(canvas) {
		display: block;
		width: 100% !important;
		height: 100% !important;
	}
</style>
