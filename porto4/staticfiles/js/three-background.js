// Three.js Background Animation

class ThreeBackground {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.init();
    }
    
    init() {
        // Setup scene
        this.scene = new THREE.Scene();
        
        // Setup camera
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.z = 30;
        
        // Setup renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            alpha: true,
            antialias: true
        });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        
        // Create objects
        this.createStars();
        this.createFloatingObjects();
        
        // Handle window resize
        window.addEventListener('resize', this.handleResize.bind(this));
        
        // Start animation loop
        this.animate();
    }
    
    createStars() {
        const starGeometry = new THREE.BufferGeometry();
        const starMaterial = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 0.5,
            transparent: true
        });
        
        const starVertices = [];
        for (let i = 0; i < 1500; i++) {
            const x = (Math.random() - 0.5) * 2000;
            const y = (Math.random() - 0.5) * 2000;
            const z = (Math.random() - 0.5) * 2000;
            starVertices.push(x, y, z);
        }
        
        starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
        this.stars = new THREE.Points(starGeometry, starMaterial);
        this.scene.add(this.stars);
    }
    
    createFloatingObjects() {
        this.objects = [];
        const colors = [0x6a35ff, 0x35ff6a, 0xff6a35, 0x35a0ff];
        
        for (let i = 0; i < 25; i++) {
            let geometry;
            const random = Math.random();
            
            if (random < 0.25) {
                geometry = new THREE.IcosahedronGeometry(Math.random() * 2 + 0.5, 0);
            } else if (random < 0.5) {
                geometry = new THREE.TetrahedronGeometry(Math.random() * 2 + 0.5, 0);
            } else if (random < 0.75) {
                geometry = new THREE.OctahedronGeometry(Math.random() * 2 + 0.5, 0);
            } else {
                geometry = new THREE.TorusKnotGeometry(
                    Math.random() * 1.5 + 0.5, // radius
                    Math.random() * 0.5 + 0.1, // tube
                    Math.floor(Math.random() * 5) + 3, // tubularSegments
                    Math.floor(Math.random() * 5) + 3, // radialSegments
                    Math.floor(Math.random() * 3) + 1, // p
                    Math.floor(Math.random() * 3) + 1  // q
                );
            }
            
            const material = new THREE.MeshBasicMaterial({
                color: colors[Math.floor(Math.random() * colors.length)],
                wireframe: true
            });
            
            const object = new THREE.Mesh(geometry, material);
            object.position.x = (Math.random() - 0.5) * 100;
            object.position.y = (Math.random() - 0.5) * 100;
            object.position.z = (Math.random() - 0.5) * 100;
            
            object.rotation.x = Math.random() * Math.PI;
            object.rotation.y = Math.random() * Math.PI;
            
            // Add random rotation and movement properties
            object.userData = {
                rotationSpeed: {
                    x: (Math.random() - 0.5) * 0.01,
                    y: (Math.random() - 0.5) * 0.01,
                    z: (Math.random() - 0.5) * 0.01
                },
                floatSpeed: {
                    x: (Math.random() - 0.5) * 0.05,
                    y: (Math.random() - 0.5) * 0.05,
                    z: (Math.random() - 0.5) * 0.05
                },
                floatDistance: {
                    x: Math.random() * 10,
                    y: Math.random() * 10,
                    z: Math.random() * 10
                },
                initialPosition: {
                    x: object.position.x,
                    y: object.position.y,
                    z: object.position.z
                },
                time: Math.random() * Math.PI * 2
            };
            
            this.objects.push(object);
            this.scene.add(object);
        }
    }
    
    handleResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
    
    animate() {
        requestAnimationFrame(this.animate.bind(this));
        
        // Rotate stars slowly
        if (this.stars) {
            this.stars.rotation.x += 0.0001;
            this.stars.rotation.y += 0.0001;
        }
        
        // Animate objects
        if (this.objects) {
            this.objects.forEach(obj => {
                // Rotate
                obj.rotation.x += obj.userData.rotationSpeed.x;
                obj.rotation.y += obj.userData.rotationSpeed.y;
                obj.rotation.z += obj.userData.rotationSpeed.z;
                
                // Float movement
                obj.userData.time += 0.01;
                
                obj.position.x = obj.userData.initialPosition.x + 
                    Math.sin(obj.userData.time) * obj.userData.floatDistance.x;
                obj.position.y = obj.userData.initialPosition.y + 
                    Math.cos(obj.userData.time) * obj.userData.floatDistance.y;
                obj.position.z = obj.userData.initialPosition.z + 
                    Math.sin(obj.userData.time * 0.5) * obj.userData.floatDistance.z;
            });
        }
        
        // Mouse interaction
        if (this.mouseX && this.mouseY) {
            this.camera.position.x += (this.mouseX - this.camera.position.x) * 0.05;
            this.camera.position.y += (-this.mouseY - this.camera.position.y) * 0.05;
            this.camera.lookAt(this.scene.position);
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    // Add mouse interaction
    enableMouseInteraction() {
        this.mouseX = 0;
        this.mouseY = 0;
        
        document.addEventListener('mousemove', (event) => {
            this.mouseX = (event.clientX - window.innerWidth / 2) * 0.01;
            this.mouseY = (event.clientY - window.innerHeight / 2) * 0.01;
        });
    }
    
    // Add scroll interaction
    enableScrollInteraction() {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY || window.pageYOffset;
            const maxScroll = document.body.scrollHeight - window.innerHeight;
            const scrollPercent = scrollY / maxScroll;
            
            // Rotate scene based on scroll position
            if (this.scene) {
                this.scene.rotation.y = scrollPercent * Math.PI * 0.5;
            }
        });
    }
    
    // Add touch interaction for mobile
    enableTouchInteraction() {
        document.addEventListener('touchmove', (event) => {
            if (event.touches.length === 1) {
                this.mouseX = (event.touches[0].clientX - window.innerWidth / 2) * 0.01;
                this.mouseY = (event.touches[0].clientY - window.innerHeight / 2) * 0.01;
            }
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const threeBackground = new ThreeBackground('bg-canvas');
    threeBackground.enableMouseInteraction();
    threeBackground.enableScrollInteraction();
    threeBackground.enableTouchInteraction();
});