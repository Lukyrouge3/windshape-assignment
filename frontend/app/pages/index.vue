<script setup lang="ts">
	import { io } from 'socket.io-client';
	import * as THREE from 'three'

	const ObjectTypes = {
	  Cube: 'CUBE',
	  Sphere: 'SPHERE',
	  Pyramid: 'PYRAMID'
	} as const;

	type SceneObject = {
		objectType: typeof ObjectTypes[keyof typeof ObjectTypes],
		size: number,
		position: {x: number, y: number, z: number},
		color: string
	};

	const typeOptions = [
		{ label: 'Cube', value: ObjectTypes.Cube },
		{ label: 'Sphere', value: ObjectTypes.Sphere },
		{ label: 'Pyramid', value: ObjectTypes.Pyramid }
	]

	const formState = reactive<SceneObject>({
		objectType: ObjectTypes.Cube,
		size: 1,
		position: { x: 0, y: 0, z: 0 },
		color: '#ff0000'
	});

	const socket = io('http://localhost:5000'); // TODO: Get url from env

	socket.emit('scene_data', null, (sceneData: {objects: SceneObject[]}) => {
		sceneObjects.value = sceneData.objects;
		renderScene();
	});

	socket.on('object_added', (newObject: SceneObject) => {
		sceneObjects.value.push(newObject);
		renderScene();
	});

	const scene = new THREE.Scene();
	const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
	const renderer = new THREE.WebGLRenderer({ antialias: true });

	const sceneObjects = ref<SceneObject[]>([]);
	let objects: THREE.Mesh[] = [];

	function addObject() {
		socket.emit("add_object", formState);
	}

	function initLights() {
		const ambient = new THREE.AmbientLight(0xffffff, 0.5);
		scene.add(ambient);
		const directional = new THREE.DirectionalLight(0xffffff, 0.7);
		directional.position.set(5, 10, 7.5);
		scene.add(directional);
	}

	function initThree() {
		const container = document.getElementById('three')!
		const { clientWidth, clientHeight } = container
		renderer.setSize(clientWidth, clientHeight)
		renderer.setPixelRatio(window.devicePixelRatio)
		container.appendChild(renderer.domElement)

		camera.aspect = clientWidth / clientHeight
		camera.updateProjectionMatrix()
		camera.position.set(0, 2, 5)

		initLights()

		// Lancer la boucle de rendu
		const animate = () => {
			requestAnimationFrame(animate)
			renderer.render(scene, camera)
		}
		animate()
	}

	function clearScene() {
		objects.forEach((obj) => {
			scene.remove(obj);
			obj.geometry.dispose();

			// Clear material too
			if ((obj.material as any).dispose) {
				(obj.material as any).dispose();
			}
		})
		objects = [];
	}

	function renderScene() {
		clearScene();
		objects = sceneObjects.value.map((obj) => {
			let geometry: THREE.BufferGeometry;
			switch (obj.objectType) {
				case ObjectTypes.Cube:
					geometry = new THREE.BoxGeometry(obj.size, obj.size, obj.size);
					break;
				case ObjectTypes.Sphere:
					geometry = new THREE.SphereGeometry(obj.size, 32, 32);
					break;
				case ObjectTypes.Pyramid:
					geometry = new THREE.ConeGeometry(obj.size, obj.size, 4);
					break;
			} 
			if (!geometry) throw new Error(`Unknown type ${obj.objectType}`);
			const material = new THREE.MeshStandardMaterial({ color: obj.color });
			const mesh = new THREE.Mesh(geometry, material);
			mesh.position.set(obj.position.x, obj.position.y, obj.position.z);
			scene.add(mesh);
			return mesh;
		});
	}

	onMounted(() => {
		initThree();
	});

</script>

<template>
  <div class="p-4 flex flex-col">
		<div id="three" class="absolute inset-0"/>

		<UCollapsible class="max-w-xl z-10 p-4" default-open>
			<UButton
						label="Add an object"
						color="neutral"
						variant="subtle"
						trailing-icon="i-lucide-chevron-down"
						block
					/>
			<template #content>
				<UForm :state="formState" class="p-4 border border-white/50 rounded-lg" @submit.prevent="addObject">
					<UFormField label="Select Object Type" name="objectType">
						<USelect v-model="formState.objectType" :items="typeOptions" />
					</UFormField>

					<UFormField label="Size" name="size">
						<UInputNumber v-model="formState.size" type="number" :step="0.1" />
					</UFormField>

					<UFormField label="Position" name="position" class="">
						<UInputNumber v-model="formState.position.x" type="number" placeholder="X" />
						<UInputNumber v-model="formState.position.y" type="number" placeholder="Y" />
						<UInputNumber v-model="formState.position.z" type="number" placeholder="Z" />
					</UFormField>

					<UFormField label="Color" name="color">
						<UColorPicker v-model="formState.color" />
					</UFormField>

					<div class="mt-4">
						<UButton type="submit">Ajouter l'objet</UButton>
					</div>
				</UForm>
			</template>
		</UCollapsible>
		
	</div>
</template>