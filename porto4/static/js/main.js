// Main JavaScript for Portfolio Website

// DOM Elements
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuLinks = document.querySelectorAll('.mobile-menu a');
const navLinks = document.querySelectorAll('.nav-link');
const scrollToTopBtn = document.getElementById('scroll-to-top');
const colorChangerToggle = document.getElementById('color-changer-toggle');
const colorChangerPanel = document.getElementById('color-changer-panel');
const colorButtons = document.querySelectorAll('.color-btn');
const themeToggle = document.getElementById('theme-toggle');
const loader = document.querySelector('.loader');

// Data for modals
let projectsData = [];
let certificatesData = [];

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Hide loader after page loads
    window.addEventListener('load', () => {
        setTimeout(() => {
            if (loader) {
                loader.classList.add('hidden');
            }
        }, 500);
    });

    // Initialize Three.js background
    initThreeJsBackground();
    
    // Initialize particle background
    createParticles();
    
    // Initialize typing effect
    const typingElement = document.querySelector('.typing-effect');
    const typingElement2 = document.querySelector('.typing-effect-2');
    
    if (typingElement) {
        // Menggunakan teks dari elemen itu sendiri jika tidak ada atribut data-text
        const textToType = typingElement.getAttribute('data-text') || typingElement.textContent.trim();
        // Simpan teks asli terlebih dahulu
        typingElement.textContent = '';
        // Mulai efek typing
        typeWriter(typingElement, textToType, 0, 100);
    }
    
    if (typingElement2) {
        // Menggunakan teks dari elemen itu sendiri jika tidak ada atribut data-text
        const textToType2 = typingElement2.getAttribute('data-text') || typingElement2.textContent.trim();
        // Simpan teks asli terlebih dahulu
        typingElement2.textContent = '';
        // Mulai efek typing
        typeWriter(typingElement2, textToType2, 0, 100);
    }
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Initialize anime.js animations
    initAnimeAnimations();
    
    // Initialize certificate filter
    initCertificateFilter();
    
    // Initialize modals
    initModals();
    
    // Initialize event listeners
    initEventListeners();
    
    // Setup expand/collapse functionality
    setupExpandCollapse();
    
    // Initialize skill animations
    initSkillAnimations();
    
    // Initialize project functionality
    initProjectFunctionality();
});

// Initialize Three.js background
function initThreeJsBackground() {
    const canvas = document.getElementById('bg-canvas');
    if (!canvas) return;
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Create stars
    const starGeometry = new THREE.BufferGeometry();
    const starMaterial = new THREE.PointsMaterial({
        color: 0xffffff,
        size: 0.5,
        transparent: true
    });
    
    const starVertices = [];
    for (let i = 0; i < 1000; i++) {
        const x = (Math.random() - 0.5) * 2000;
        const y = (Math.random() - 0.5) * 2000;
        const z = (Math.random() - 0.5) * 2000;
        starVertices.push(x, y, z);
    }
    
    starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);
    
    // Create floating objects
    const objects = [];
    const colors = [0x6a35ff, 0x35ff6a, 0xff6a35, 0x35a0ff];
    
    for (let i = 0; i < 20; i++) {
        let geometry;
        const random = Math.random();
        
        if (random < 0.3) {
            geometry = new THREE.IcosahedronGeometry(Math.random() * 2 + 0.5, 0);
        } else if (random < 0.6) {
            geometry = new THREE.TetrahedronGeometry(Math.random() * 2 + 0.5, 0);
        } else {
            geometry = new THREE.OctahedronGeometry(Math.random() * 2 + 0.5, 0);
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
        
        // Add random rotation speed
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
        
        objects.push(object);
        scene.add(object);
    }
    
    camera.position.z = 30;
    
    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        // Rotate stars slowly
        stars.rotation.x += 0.0001;
        stars.rotation.y += 0.0001;
        
        // Animate objects
        objects.forEach(obj => {
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
        
        renderer.render(scene, camera);
    }
    
    animate();
}

// Create particle background
function createParticles() {
    const container = document.querySelector('.particles-container');
    if (!container) return;
    
    const colors = ['blue', 'purple', 'orange', 'yellow', 'red'];
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.classList.add(`particle-${i % 5 + 1}`);
        particle.classList.add(colors[Math.floor(Math.random() * colors.length)]);
        
        const size = Math.random() * 20 + 5;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        particle.style.left = `${Math.random() * 100}vw`;
        particle.style.top = `${Math.random() * 100}vh`;
        
        container.appendChild(particle);
    }
}

// Typing effect
function typeWriter(element, text, i, speed) {
    // Pastikan text tidak null atau undefined
    if (!text) {
        console.warn('Text untuk typing effect tidak ditemukan');
        return;
    }
    
    if (i < text.length) {
        element.innerHTML = text.substring(0, i + 1);
        setTimeout(() => {
            typeWriter(element, text, i + 1, speed);
        }, speed);
    }
}

// Initialize scroll animations
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Home section animations
    const homeAnimElements = [
        document.querySelector('.animate-in-home-delay-1'),
        document.querySelector('.animate-in-home-delay-2'),
        document.querySelector('.animate-in-home-delay-3'),
        document.querySelector('.animate-in-home-delay-4'),
        document.querySelector('.animate-in-home-delay-5'),
        document.querySelector('.animate-in-home-delay-6')
    ];
    
    homeAnimElements.forEach((element, index) => {
        if (element) {
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 300 * (index + 1));
        }
    });
}

// Initialize anime.js animations
function initAnimeAnimations() {
    // Animate project cards
    anime({
        targets: '.project-card',
        scale: [0.9, 1],
        opacity: [0, 1],
        delay: anime.stagger(150),
        duration: 800,
        easing: 'easeOutElastic(1, .5)'
    });
    
    // Animate skill items
    anime({
        targets: '.skill-item',
        scale: [0.9, 1],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 800,
        easing: 'easeOutElastic(1, .5)'
    });
    
    // Animate certificate items
    anime({
        targets: '.certificate-item',
        scale: [0.9, 1],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 800,
        easing: 'easeOutElastic(1, .5)'
    });
    
    // Text animations
    anime({
        targets: '.section-title',
        opacity: [0, 1],
        translateY: [20, 0],
        delay: anime.stagger(200),
        duration: 800,
        easing: 'easeOutSine'
    });
}

// Initialize certificate filter
function initCertificateFilter() {
    const filterButtons = document.querySelectorAll('.certificate-filter-btn');
    const certificateItems = document.querySelectorAll('.certificate-item');
    
    if (filterButtons.length === 0 || certificateItems.length === 0) return;
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            const category = button.getAttribute('data-category');
            
            // Filter certificates
            certificateItems.forEach(item => {
                if (category === 'all') {
                    // Show all certificates with animation
                    anime({
                        targets: item,
                        scale: [0.9, 1],
                        opacity: [0, 1],
                        duration: 500,
                        easing: 'easeOutSine'
                    });
                } else if (item.getAttribute('data-category') === category) {
                    // Show certificates of selected category with animation
                    anime({
                        targets: item,
                        scale: [0.9, 1],
                        opacity: [0, 1],
                        duration: 500,
                        easing: 'easeOutSine'
                    });
                } else {
                    // Hide certificates of other categories with animation
                    anime({
                        targets: item,
                        scale: [1, 0.9],
                        opacity: [1, 0],
                        duration: 500,
                        easing: 'easeOutSine'
                    });
                }
            });
        });
    });
    
    // Set 'All' as default active filter
    const allButton = document.querySelector('.certificate-filter-btn[data-category="all"]');
    if (allButton) {
        allButton.classList.add('active');
    }
}

// Initialize modals
function initModals() {
    // Project modals
    const projectCards = document.querySelectorAll('.project-card');
    const projectModal = document.getElementById('project-modal');
    
    if (projectCards.length > 0 && projectModal) {
        projectCards.forEach(card => {
            card.addEventListener('click', () => {
                const projectId = card.getAttribute('data-id');
                const project = projectsData.find(p => p.id.toString() === projectId);
                
                if (project) {
                    // Fill modal with project data
                    document.getElementById('project-modal-image').src = project.image;
                    document.getElementById('project-modal-title').textContent = project.title;
                    document.getElementById('project-modal-description').textContent = project.description;
                    
                    // Tech stack
                    const techStackContainer = document.getElementById('project-modal-tech-stack');
                    techStackContainer.innerHTML = '';
                    project.tech_stack.forEach(tech => {
                        const techBadge = document.createElement('span');
                        techBadge.className = 'inline-block bg-gray-800 text-white text-xs px-3 py-1 rounded-full mr-2 mb-2';
                        techBadge.textContent = tech;
                        techStackContainer.appendChild(techBadge);
                    });
                    
                    // Links
                    const liveLink = document.getElementById('project-modal-live-link');
                    const githubLink = document.getElementById('project-modal-github-link');
                    
                    if (project.live_link) {
                        liveLink.href = project.live_link;
                        liveLink.style.display = 'inline-flex';
                    } else {
                        liveLink.style.display = 'none';
                    }
                    
                    if (project.github_link) {
                        githubLink.href = project.github_link;
                        githubLink.style.display = 'inline-flex';
                    } else {
                        githubLink.style.display = 'none';
                    }
                    
                    // Open modal with animation
                    projectModal.classList.add('open');
                    document.body.style.overflow = 'hidden';
                }
            });
        });
    }
    
    // Certificate modals
    const certificateCards = document.querySelectorAll('.certificate-item');
    const certificateModal = document.getElementById('certificate-modal');
    
    if (certificateCards.length > 0 && certificateModal) {
        certificateCards.forEach(card => {
            card.addEventListener('click', () => {
                const certificateId = card.getAttribute('data-id');
                const certificate = certificatesData.find(c => c.id.toString() === certificateId);
                
                if (certificate) {
                    // Fill modal with certificate data
                    document.getElementById('certificate-modal-image').src = certificate.image || '';
                    document.getElementById('certificate-modal-title').textContent = certificate.title;
                    document.getElementById('certificate-modal-issuer').textContent = certificate.organization;
                    document.getElementById('certificate-modal-date').textContent = certificate.issue_date;
                    
                    const credentialId = document.getElementById('certificate-modal-credential-id');
                    const credentialIdContainer = document.getElementById('certificate-credential-id-container');
                    
                    if (certificate.credential_id) {
                        credentialId.textContent = certificate.credential_id;
                        credentialIdContainer.style.display = 'block';
                    } else {
                        credentialIdContainer.style.display = 'none';
                    }
                    
                    const certificateLink = document.getElementById('certificate-modal-link');
                    const certificateLinkContainer = document.getElementById('certificate-link-container');
                    
                    if (certificate.url) {
                        certificateLink.href = certificate.url;
                        certificateLinkContainer.style.display = 'block';
                    } else {
                        certificateLinkContainer.style.display = 'none';
                    }
                    
                    // Open modal with animation
                    certificateModal.classList.add('open');
                    document.body.style.overflow = 'hidden';
                }
            });
        });
    }
    
    // Close modals
    const closeButtons = document.querySelectorAll('.close-btn');
    const modals = document.querySelectorAll('.modal');
    
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            modals.forEach(modal => {
                modal.classList.remove('open');
            });
            document.body.style.overflow = 'auto';
        });
    });
    
    // Close modal when clicking outside
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('open');
                document.body.style.overflow = 'auto';
            }
        });
    });
}

// Initialize event listeners
function initEventListeners() {
    // Mobile menu toggle
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
            document.body.classList.toggle('overflow-hidden');
        });
        
        // Close mobile menu when clicking a link
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                document.body.classList.remove('overflow-hidden');
            });
        });
    }
    
    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Remove active class from all links
                navLinks.forEach(navLink => navLink.classList.remove('active'));
                
                // Add active class to clicked link
                link.classList.add('active');
                
                // Scroll to section
                window.scrollTo({
                    top: targetSection.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Scroll to top button
    if (scrollToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.style.opacity = '1';
                scrollToTopBtn.style.pointerEvents = 'auto';
            } else {
                scrollToTopBtn.style.opacity = '0';
                scrollToTopBtn.style.pointerEvents = 'none';
            }
        });
        
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Color changer toggle
    if (colorChangerToggle && colorChangerPanel) {
        colorChangerToggle.addEventListener('click', () => {
            colorChangerPanel.classList.toggle('open');
        });
        
        // Change primary color
        colorButtons.forEach(button => {
            button.addEventListener('click', () => {
                const color = button.getAttribute('data-color');
                document.documentElement.style.setProperty('--primary-color', color);
                
                // Remove active class from all buttons
                colorButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                button.classList.add('active');
                
                // Save color preference to localStorage
                localStorage.setItem('primary-color', color);
            });
        });
    }
    
    // Theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            
            // Save theme preference to localStorage
            const isLightTheme = document.body.classList.contains('light-theme');
            localStorage.setItem('light-theme', isLightTheme);
            
            // Update theme toggle icon
            const themeIcon = themeToggle.querySelector('i');
            if (isLightTheme) {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            } else {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            }
        });
    }
    
    // Copy to clipboard function
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const textToCopy = button.getAttribute('data-copy');
            copyToClipboard(textToCopy);
            
            // Show notification
            const notification = document.createElement('div');
            notification.className = 'fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
            notification.textContent = 'Copied to clipboard!';
            document.body.appendChild(notification);
            
            // Remove notification after 2 seconds
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 2000);
        });
    });
}

// Copy to clipboard function
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

// Load saved preferences
function loadSavedPreferences() {
    // Load primary color
    const savedColor = localStorage.getItem('primary-color');
    if (savedColor) {
        document.documentElement.style.setProperty('--primary-color', savedColor);
        
        // Set active class on color button
        const activeColorButton = document.querySelector(`.color-btn[data-color="${savedColor}"]`);
        if (activeColorButton) {
            activeColorButton.classList.add('active');
        }
    }
    
    // Load theme
    const isLightTheme = localStorage.getItem('light-theme') === 'true';
    if (isLightTheme) {
        document.body.classList.add('light-theme');
        
        // Update theme toggle icon
        const themeIcon = document.querySelector('#theme-toggle i');
        if (themeIcon) {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
    }
}

// Call load preferences on page load
loadSavedPreferences();

// Setup expand/collapse functionality
function setupExpandCollapse() {
    // About Me expand/collapse
    const aboutToggle = document.getElementById('about-toggle');
    const aboutContent = document.getElementById('about-content');
    const aboutToggleText = document.getElementById('about-toggle-text');
    const aboutToggleIcon = document.getElementById('about-toggle-icon');
    
    if (aboutToggle && aboutContent) {
        // Initially collapsed on mobile
        if (window.innerWidth <= 768) {
            aboutContent.classList.add('collapsed');
        }
        
        aboutToggle.addEventListener('click', () => {
            aboutContent.classList.toggle('collapsed');
            const isCollapsed = aboutContent.classList.contains('collapsed');
            
            if (aboutToggleText && aboutToggleIcon) {
                aboutToggleText.textContent = isCollapsed ? 'Selengkapnya' : 'Sembunyikan';
                aboutToggleIcon.style.transform = isCollapsed ? 'rotate(0deg)' : 'rotate(180deg)';
            }
        });
    }
    
    // Projects expand/collapse
    const projectsToggle = document.getElementById('projects-toggle');
    const projectsContent = document.getElementById('projects-content');
    const projectsToggleText = document.getElementById('projects-toggle-text');
    const projectsToggleIcon = document.getElementById('projects-toggle-icon');
    
    if (projectsToggle && projectsContent) {
        // Initially collapsed on mobile
        if (window.innerWidth <= 768) {
            projectsContent.classList.add('collapsed');
        }
        
        projectsToggle.addEventListener('click', () => {
            projectsContent.classList.toggle('collapsed');
            const isCollapsed = projectsContent.classList.contains('collapsed');
            
            if (projectsToggleText && projectsToggleIcon) {
                projectsToggleText.textContent = isCollapsed ? 'Lihat Semua Proyek' : 'Sembunyikan';
                projectsToggleIcon.style.transform = isCollapsed ? 'rotate(0deg)' : 'rotate(180deg)';
            }
        });
    }
    
    // Certificates expand/collapse
    const certificatesToggle = document.getElementById('certificates-toggle');
    const certificatesContent = document.getElementById('certificates-content');
    const certificatesToggleText = document.getElementById('certificates-toggle-text');
    const certificatesToggleIcon = document.getElementById('certificates-toggle-icon');
    
    if (certificatesToggle && certificatesContent) {
        // Initially collapsed on mobile
        if (window.innerWidth <= 768) {
            certificatesContent.classList.add('collapsed');
        }
        
        certificatesToggle.addEventListener('click', () => {
            certificatesContent.classList.toggle('collapsed');
            const isCollapsed = certificatesContent.classList.contains('collapsed');
            
            if (certificatesToggleText && certificatesToggleIcon) {
                certificatesToggleText.textContent = isCollapsed ? 'Lihat Semua Sertifikat' : 'Sembunyikan';
                certificatesToggleIcon.style.transform = isCollapsed ? 'rotate(0deg)' : 'rotate(180deg)';
            }
        });
    }
    
    // Handle window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            // Remove collapsed class on desktop
            if (aboutContent) aboutContent.classList.remove('collapsed');
            if (projectsContent) projectsContent.classList.remove('collapsed');
            if (certificatesContent) certificatesContent.classList.remove('collapsed');
        } else {
            // Add collapsed class on mobile if not already expanded
            if (aboutContent && !aboutContent.classList.contains('expanded')) {
                aboutContent.classList.add('collapsed');
            }
            if (projectsContent && !projectsContent.classList.contains('expanded')) {
                projectsContent.classList.add('collapsed');
            }
            if (certificatesContent && !certificatesContent.classList.contains('expanded')) {
                certificatesContent.classList.add('collapsed');
            }
        }
    });
}

// Initialize skill animations
function initSkillAnimations() {
    const skillItems = document.querySelectorAll('.skill-item');
    
    // Intersection Observer for skill animations
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target.querySelector('.skill-progress');
                if (progressBar) {
                    const targetWidth = progressBar.getAttribute('data-width');
                    setTimeout(() => {
                        progressBar.style.width = targetWidth;
                    }, 200);
                }
                skillObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5
    });
    
    skillItems.forEach(item => {
        skillObserver.observe(item);
    });
}

// Initialize project functionality
function initProjectFunctionality() {
    // Handle "Show More Projects" buttons
    const showMoreButtons = document.querySelectorAll('.show-more-projects');
    
    showMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            const hiddenProjects = document.querySelectorAll(`#projects-grid-${category} .project-hidden, #projects-grid .project-hidden`);
            const buttonText = this.querySelector('.button-text');
            const buttonIcon = this.querySelector('i');
            
            const isExpanded = this.classList.contains('expanded');
            
            if (isExpanded) {
                // Hide projects
                hiddenProjects.forEach(project => {
                    project.classList.add('hidden');
                });
                buttonText.textContent = buttonText.textContent.replace('Sembunyikan', 'Lihat Semua Proyek');
                buttonIcon.style.transform = 'rotate(0deg)';
                this.classList.remove('expanded');
            } else {
                // Show projects
                hiddenProjects.forEach((project, index) => {
                    setTimeout(() => {
                        project.classList.remove('hidden');
                        project.style.animation = 'fadeInUp 0.5s ease forwards';
                    }, index * 100);
                });
                buttonText.textContent = buttonText.textContent.replace(/Lihat Semua Proyek \(\d+\)/, 'Sembunyikan');
                buttonIcon.style.transform = 'rotate(180deg)';
                this.classList.add('expanded');
            }
        });
    });
    
    // Handle project card clicks for modal
    const projectCards = document.querySelectorAll('.project-card');
    const projectModal = document.getElementById('project-modal');
    const closeModalBtn = document.getElementById('close-project-modal');
    
    projectCards.forEach(card => {
        card.addEventListener('click', function() {
            const projectId = this.getAttribute('data-project-id');
            openProjectModal(projectId);
        });
    });
    
    // Close modal events
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeProjectModal);
    }
    
    if (projectModal) {
        projectModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeProjectModal();
            }
        });
    }
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && projectModal && !projectModal.classList.contains('invisible')) {
            closeProjectModal();
        }
    });
}

// Open project modal
function openProjectModal(projectId) {
    const modal = document.getElementById('project-modal');
    if (!modal) return;
    
    // Show modal with animation
    modal.classList.remove('invisible', 'opacity-0');
    modal.classList.add('opacity-100');
    modal.querySelector('.bg-\\[\\#1a1a2e\\]').classList.remove('scale-95');
    modal.querySelector('.bg-\\[\\#1a1a2e\\]').classList.add('scale-100');
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
    
    // Load project data (this would typically fetch from an API)
    loadProjectData(projectId);
}

// Close project modal
function closeProjectModal() {
    const modal = document.getElementById('project-modal');
    if (!modal) return;
    
    // Hide modal with animation
    modal.classList.remove('opacity-100');
    modal.classList.add('opacity-0');
    modal.querySelector('.bg-\\[\\#1a1a2e\\]').classList.remove('scale-100');
    modal.querySelector('.bg-\\[\\#1a1a2e\\]').classList.add('scale-95');
    
    setTimeout(() => {
        modal.classList.add('invisible');
        document.body.style.overflow = 'auto';
    }, 300);
}

// Load project data for modal
function loadProjectData(projectId) {
    // This is a placeholder function. In a real application, you would fetch data from an API
    // For now, we'll populate with sample data
    
    const modalTitle = document.getElementById('modal-project-title');
    const modalMainImage = document.getElementById('modal-project-main-image');
    const modalDescription = document.getElementById('modal-project-description');
    const modalFeatures = document.getElementById('modal-project-features');
    const modalTechnologies = document.getElementById('modal-project-technologies');
    const modalLinks = document.getElementById('modal-project-links');
    const modalStatus = document.getElementById('modal-project-status');
    const modalDate = document.getElementById('modal-project-date');
    const modalCategory = document.getElementById('modal-project-category');
    
    // Sample data - replace with actual API call
    const sampleData = {
        title: 'Sample Project',
        image: '/static/img/project-placeholder.svg',
        description: 'Ini adalah deskripsi detail dari project yang sedang ditampilkan. Project ini dibuat dengan teknologi modern dan mengikuti best practices dalam pengembangan web.',
        features: [
            'Responsive design untuk semua perangkat',
            'Optimasi performa dan SEO',
            'Integrasi dengan API eksternal',
            'Sistem autentikasi yang aman',
            'Dashboard admin yang user-friendly'
        ],
        technologies: ['Django', 'JavaScript', 'Tailwind CSS', 'PostgreSQL'],
        github: '#',
        live: '#',
        status: 'Completed',
        date: 'Januari 2024',
        category: 'Web Development'
    };
    
    // Populate modal with data
    if (modalTitle) modalTitle.textContent = sampleData.title;
    if (modalMainImage) {
        modalMainImage.src = sampleData.image;
        modalMainImage.alt = sampleData.title;
    }
    if (modalDescription) modalDescription.textContent = sampleData.description;
    
    if (modalFeatures) {
        modalFeatures.innerHTML = sampleData.features.map(feature => 
            `<li class="flex items-start gap-2">
                <i class="fas fa-check text-primary-color mt-1 flex-shrink-0"></i>
                <span>${feature}</span>
            </li>`
        ).join('');
    }
    
    if (modalTechnologies) {
        modalTechnologies.innerHTML = sampleData.technologies.map(tech => 
            `<span class="bg-gray-700 text-gray-300 text-xs font-semibold px-2.5 py-1 rounded-full">${tech}</span>`
        ).join('');
    }
    
    if (modalLinks) {
        modalLinks.innerHTML = `
            <a href="${sampleData.github}" target="_blank" class="flex items-center gap-2 text-gray-300 hover:text-primary-color transition-colors duration-300">
                <i class="fab fa-github"></i>
                <span>Source Code</span>
            </a>
            <a href="${sampleData.live}" target="_blank" class="flex items-center gap-2 text-gray-300 hover:text-primary-color transition-colors duration-300">
                <i class="fas fa-external-link-alt"></i>
                <span>Live Demo</span>
            </a>
        `;
    }
    
    if (modalStatus) modalStatus.textContent = sampleData.status;
    if (modalDate) modalDate.textContent = sampleData.date;
    if (modalCategory) modalCategory.textContent = sampleData.category;
}