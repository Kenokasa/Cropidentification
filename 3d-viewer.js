import * as THREE from 'three';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';

function init3DViewer() {
    const container = document.getElementById('3d-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });

    // Load your converted STL file (convert SMG to STL first)
    const loader = new STLLoader();
    loader.load('/static/models/plant_model.stl', function (geometry) {
        const material = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
    });

    // Add lights and controls
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    const light = new THREE.PointLight(0xffffff, 1);
    camera.add(light);
    scene.add(camera);

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
}
// Add orbit controls
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Add click interaction
renderer.domElement.addEventListener('click', (event) => {
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children);

    if (intersects.length > 0) {
        showPartInfo(intersects[0].object.name);
    }
});

function showPartInfo(partName) {
    // Make API call to Django backend
    fetch(`/api/plant-parts/${partName}/`)
        .then(response => response.json())
        .then(data => {
            // Show modal with part information
            const modal = document.getElementById('part-modal');
            modal.querySelector('.part-name').textContent = data.name;
            modal.querySelector('.part-description').textContent = data.description;
            modal.showModal();
        });
}