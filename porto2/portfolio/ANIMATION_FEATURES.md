# Fitur Animasi 3D - Portfolio Civil Engineer

## Overview
Halaman home telah diperbarui dengan berbagai animasi 3D dan efek visual yang menarik menggunakan Three.js, GSAP, dan CSS animations.

## Fitur Animasi yang Ditambahkan

### 1. Hero Section Enhancements
- **3D Background Canvas**: Canvas 3D untuk background hero section
- **Particle System**: Sistem partikel yang bergerak di background
- **Enhanced Floating Elements**: Elemen mengambang dengan animasi yang lebih kompleks
- **Interactive 3D Models**: Model 3D interaktif (bridge, building, tower)
- **Text Gradient Animation**: Animasi gradient pada judul
- **Button Animations**: Animasi pulse dan glow pada tombol

### 2. About Section Animations
- **Slide-in Animations**: Animasi slide dari kiri dan kanan
- **Text Reveal**: Animasi reveal untuk teks
- **Staggered Stats**: Animasi counter untuk statistik
- **Image Float**: Animasi mengambang untuk gambar profil

### 3. Services Section Enhancements
- **Service Card Animations**: Animasi stagger untuk kartu layanan
- **Icon Float**: Animasi mengambang untuk ikon layanan
- **Text Reveal**: Animasi reveal untuk judul dan deskripsi

### 4. 3D Models Features
- **Bridge Model**: Model 3D jembatan dengan rotasi
- **Building Model**: Model 3D bangunan dengan animasi
- **Tower Model**: Model 3D menara dengan geometri cone
- **Interactive Hover**: Efek hover pada model 3D

### 5. Particle System
- **Background Particles**: 50 partikel dengan warna biru-ungu
- **Rotation Animation**: Rotasi partikel yang smooth
- **Responsive**: Menyesuaikan dengan ukuran layar

## File yang Dimodifikasi

### 1. `templates/main_app/home.html`
- Menambahkan canvas 3D dan container partikel
- Menambahkan class animasi untuk elemen-elemen
- Menambahkan container model 3D
- Menambahkan floating elements yang enhanced

### 2. `static/css/home.css`
- Menambahkan animasi CSS untuk floating elements
- Menambahkan animasi text gradient
- Menambahkan animasi button
- Menambahkan animasi service cards
- Menambahkan animasi about section

### 3. `static/js/animations.js`
- Menambahkan setup 3D models
- Menambahkan particle system
- Menambahkan interactive elements
- Menambahkan scroll-based animations
- Menambahkan enhanced hover effects

### 4. `static/js/home.js`
- Menambahkan init3DModels()
- Menambahkan initParticleSystem()
- Menambahkan initEnhancedScrollAnimations()
- Menambahkan create3DModel()
- Menambahkan observer untuk animasi scroll

## Cara Kerja Animasi

### 1. Scroll-Based Animations
```javascript
// Observer untuk mendeteksi elemen yang masuk viewport
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
});
```

### 2. 3D Models
```javascript
// Membuat model 3D berdasarkan tipe
function create3DModel(container, modelType) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    
    // Animasi loop
    function animate() {
        requestAnimationFrame(animate);
        mesh.rotation.x += 0.01;
        mesh.rotation.y += 0.02;
        renderer.render(scene, camera);
    }
}
```

### 3. Particle System
```javascript
// Membuat sistem partikel
function initParticleSystem() {
    const particleCount = 50;
    const particles = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    
    // Animasi partikel
    function animate() {
        requestAnimationFrame(animate);
        particleSystem.rotation.x += 0.001;
        particleSystem.rotation.y += 0.002;
        renderer.render(scene, camera);
    }
}
```

## Dependencies

### CDN Libraries (sudah ada di base.html)
- **Three.js**: Untuk rendering 3D
- **GSAP**: Untuk animasi advanced
- **ScrollTrigger**: Untuk scroll-based animations
- **TextPlugin**: Untuk text animations
- **Font Awesome**: Untuk ikon

### CSS Animations
- **@keyframes**: Untuk animasi custom
- **CSS Transitions**: Untuk smooth transitions
- **CSS Transforms**: Untuk transformasi elemen

## Performance Considerations

### 1. Lazy Loading
- Model 3D hanya dibuat saat diperlukan
- Partikel system hanya diinisialisasi jika Three.js tersedia

### 2. Responsive Design
- Canvas menyesuaikan ukuran container
- Animasi dioptimalkan untuk mobile

### 3. Memory Management
- Cleanup function untuk menghapus renderer
- Observer cleanup saat komponen dihapus

## Browser Support

### Required Features
- **WebGL**: Untuk rendering 3D
- **Intersection Observer**: Untuk scroll animations
- **CSS Grid/Flexbox**: Untuk layout
- **ES6+**: Untuk JavaScript features

### Fallbacks
- Animasi CSS tetap berfungsi tanpa JavaScript
- 3D models tidak akan render jika WebGL tidak tersedia
- Particle system akan di-skip jika Three.js tidak tersedia

## Customization

### 1. Mengubah Warna
```css
/* Ubah warna gradient */
.animate-text-gradient {
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
```

### 2. Mengubah Animasi
```javascript
// Ubah kecepatan rotasi model 3D
mesh.rotation.x += 0.005; // Lebih lambat
mesh.rotation.y += 0.01;  // Lebih lambat
```

### 3. Menambah Model 3D
```javascript
// Tambah case baru di create3DModel
case 'your-model':
    geometry = new THREE.YourGeometry();
    material = new THREE.MeshPhongMaterial({ color: 0xyour-color });
    break;
```

## Troubleshooting

### 1. Model 3D Tidak Muncul
- Pastikan Three.js sudah dimuat
- Cek console untuk error WebGL
- Pastikan container memiliki ukuran yang valid

### 2. Animasi Tidak Berfungsi
- Pastikan GSAP sudah dimuat
- Cek apakah elemen memiliki class yang benar
- Pastikan Intersection Observer tersedia

### 3. Performance Issues
- Kurangi jumlah partikel
- Kurangi kompleksitas model 3D
- Gunakan `will-change` CSS untuk optimasi

## Future Enhancements

### 1. Advanced 3D Features
- Loading GLTF models
- Physics simulations
- VR/AR support

### 2. Animation Improvements
- Morphing animations
- Advanced particle effects
- Sound effects

### 3. Performance Optimizations
- Web Workers untuk calculations
- Level of Detail (LOD)
- Frustum culling

## Credits

- **Three.js**: 3D Graphics Library
- **GSAP**: Animation Library
- **Font Awesome**: Icon Library
- **Tailwind CSS**: Utility-first CSS Framework 