// Animations using anime.js

class PortfolioAnimations {
    constructor() {
        this.initializeAnimations();
    }
    
    initializeAnimations() {
        this.setupHomeAnimations();
        this.setupScrollAnimations();
        this.setupHoverAnimations();
        this.setupSectionAnimations();
    }
    
    setupHomeAnimations() {
        // Hero section animations
        const heroElements = [
            '.animate-in-home-delay-1',
            '.animate-in-home-delay-2',
            '.animate-in-home-delay-3',
            '.animate-in-home-delay-4',
            '.animate-in-home-delay-5',
            '.animate-in-home-delay-6'
        ];
        
        heroElements.forEach((selector, index) => {
            const elements = document.querySelectorAll(selector);
            if (elements.length > 0) {
                anime({
                    targets: selector,
                    opacity: [0, 1],
                    translateY: [20, 0],
                    easing: 'easeOutSine',
                    duration: 800,
                    delay: 300 * (index + 1)
                });
            }
        });
        
        // Animate profile image
        anime({
            targets: '.profile-image',
            scale: [0.8, 1],
            opacity: [0, 1],
            borderRadius: ['30%', '50%'],
            easing: 'easeOutElastic(1, .5)',
            duration: 1500,
            delay: 500
        });
        
        // Animate social icons
        anime({
            targets: '.social-icons a',
            translateY: [20, 0],
            opacity: [0, 1],
            easing: 'easeOutSine',
            duration: 500,
            delay: anime.stagger(100, {start: 1000})
        });
    }
    
    setupScrollAnimations() {
        // Setup intersection observer for scroll animations
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.playEntranceAnimation(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    playEntranceAnimation(element) {
        // Get animation type from data attribute or use default
        const animationType = element.dataset.animation || 'fadeIn';
        
        switch (animationType) {
            case 'fadeIn':
                anime({
                    targets: element,
                    opacity: [0, 1],
                    easing: 'easeOutSine',
                    duration: 800
                });
                break;
                
            case 'slideUp':
                anime({
                    targets: element,
                    translateY: [50, 0],
                    opacity: [0, 1],
                    easing: 'easeOutSine',
                    duration: 800
                });
                break;
                
            case 'slideRight':
                anime({
                    targets: element,
                    translateX: [-50, 0],
                    opacity: [0, 1],
                    easing: 'easeOutSine',
                    duration: 800
                });
                break;
                
            case 'slideLeft':
                anime({
                    targets: element,
                    translateX: [50, 0],
                    opacity: [0, 1],
                    easing: 'easeOutSine',
                    duration: 800
                });
                break;
                
            case 'zoomIn':
                anime({
                    targets: element,
                    scale: [0.5, 1],
                    opacity: [0, 1],
                    easing: 'easeOutSine',
                    duration: 800
                });
                break;
                
            case 'bounceIn':
                anime({
                    targets: element,
                    scale: [0.3, 1.1, 1],
                    opacity: [0, 1],
                    easing: 'easeOutElastic(1, .5)',
                    duration: 1200
                });
                break;
                
            default:
                anime({
                    targets: element,
                    opacity: [0, 1],
                    easing: 'easeOutSine',
                    duration: 800
                });
        }
    }
    
    setupHoverAnimations() {
        // Project cards hover animation
        const projectCards = document.querySelectorAll('.project-card');
        
        projectCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                anime({
                    targets: card,
                    translateY: -10,
                    scale: 1.03,
                    boxShadow: '0 15px 30px rgba(0, 0, 0, 0.3)',
                    easing: 'easeOutSine',
                    duration: 300
                });
            });
            
            card.addEventListener('mouseleave', () => {
                anime({
                    targets: card,
                    translateY: 0,
                    scale: 1,
                    boxShadow: '0 5px 15px rgba(0, 0, 0, 0.1)',
                    easing: 'easeOutSine',
                    duration: 300
                });
            });
        });
        
        // Skill items hover animation
        const skillItems = document.querySelectorAll('.skill-item');
        
        skillItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                anime({
                    targets: item,
                    translateY: -5,
                    scale: 1.05,
                    easing: 'easeOutSine',
                    duration: 300
                });
            });
            
            item.addEventListener('mouseleave', () => {
                anime({
                    targets: item,
                    translateY: 0,
                    scale: 1,
                    easing: 'easeOutSine',
                    duration: 300
                });
            });
        });
        
        // Certificate items hover animation
        const certificateItems = document.querySelectorAll('.certificate-item');
        
        certificateItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                anime({
                    targets: item,
                    translateY: -5,
                    scale: 1.05,
                    easing: 'easeOutSine',
                    duration: 300
                });
            });
            
            item.addEventListener('mouseleave', () => {
                anime({
                    targets: item,
                    translateY: 0,
                    scale: 1,
                    easing: 'easeOutSine',
                    duration: 300
                });
            });
        });
        
        // Button hover animations
        const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
        
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                anime({
                    targets: button,
                    scale: 1.05,
                    easing: 'easeOutSine',
                    duration: 200
                });
            });
            
            button.addEventListener('mouseleave', () => {
                anime({
                    targets: button,
                    scale: 1,
                    easing: 'easeOutSine',
                    duration: 200
                });
            });
        });
    }
    
    setupSectionAnimations() {
        // About section animations
        this.setupStaggeredAnimations('#about .skill-item', 50);
        
        // Projects section animations
        this.setupStaggeredAnimations('#projects .project-card', 100);
        
        // Experience section timeline animations
        this.setupStaggeredAnimations('#experience .experience-item', 150);
        
        // Certificates section animations
        this.setupStaggeredAnimations('#certificates .certificate-item', 100);
        
        // Contact section form animations
        const contactForm = document.querySelector('#contact form');
        if (contactForm) {
            const formElements = contactForm.querySelectorAll('input, textarea, button');
            
            anime({
                targets: formElements,
                translateY: [20, 0],
                opacity: [0, 1],
                delay: anime.stagger(100),
                easing: 'easeOutSine',
                duration: 800,
                autoplay: false
            });
            
            // Play animation when contact section is in view
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        anime.running.forEach(instance => {
                            if (instance.animatables.some(a => formElements.includes(a.target))) {
                                instance.play();
                            }
                        });
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            observer.observe(contactForm);
        }
    }
    
    setupStaggeredAnimations(selector, staggerDelay = 50) {
        const elements = document.querySelectorAll(selector);
        if (elements.length === 0) return;
        
        const animation = anime({
            targets: elements,
            scale: [0.9, 1],
            opacity: [0, 1],
            translateY: [20, 0],
            delay: anime.stagger(staggerDelay),
            duration: 800,
            easing: 'easeOutElastic(1, .5)',
            autoplay: false
        });
        
        // Play animation when elements are in view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animation.play();
                    observer.unobserve(entry.target.parentElement);
                }
            });
        }, { threshold: 0.1 });
        
        // Observe the parent container
        const container = elements[0].parentElement;
        if (container) {
            observer.observe(container);
        }
    }
    
    // Text scramble effect
    setupTextScramble(selector, texts, options = {}) {
        const element = document.querySelector(selector);
        if (!element) return;
        
        const defaultOptions = {
            duration: 3000,
            delay: 2000,
            loop: true
        };
        
        const config = {...defaultOptions, ...options};
        
        class TextScramble {
            constructor(el) {
                this.el = el;
                this.chars = '!<>-_\\/*&^%$#@[]{}=+?~';
                this.update = this.update.bind(this);
            }
            
            setText(newText) {
                const oldText = this.el.innerText;
                const length = Math.max(oldText.length, newText.length);
                const promise = new Promise(resolve => this.resolve = resolve);
                this.queue = [];
                
                for (let i = 0; i < length; i++) {
                    const from = oldText[i] || '';
                    const to = newText[i] || '';
                    const start = Math.floor(Math.random() * 40);
                    const end = start + Math.floor(Math.random() * 40);
                    this.queue.push({ from, to, start, end });
                }
                
                cancelAnimationFrame(this.frameRequest);
                this.frame = 0;
                this.update();
                return promise;
            }
            
            update() {
                let output = '';
                let complete = 0;
                
                for (let i = 0, n = this.queue.length; i < n; i++) {
                    let { from, to, start, end, char } = this.queue[i];
                    
                    if (this.frame >= end) {
                        complete++;
                        output += to;
                    } else if (this.frame >= start) {
                        if (!char || Math.random() < 0.28) {
                            char = this.randomChar();
                            this.queue[i].char = char;
                        }
                        output += `<span class="text-primary-color">${char}</span>`;
                    } else {
                        output += from;
                    }
                }
                
                this.el.innerHTML = output;
                
                if (complete === this.queue.length) {
                    this.resolve();
                } else {
                    this.frameRequest = requestAnimationFrame(this.update);
                    this.frame++;
                }
            }
            
            randomChar() {
                return this.chars[Math.floor(Math.random() * this.chars.length)];
            }
        }
        
        const fx = new TextScramble(element);
        
        let counter = 0;
        const next = () => {
            fx.setText(texts[counter]).then(() => {
                setTimeout(next, config.delay);
            });
            counter = (counter + 1) % texts.length;
        };
        
        next();
    }
    
    // Particle effect for specific elements
    setupParticleEffect(selector) {
        const elements = document.querySelectorAll(selector);
        
        elements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                this.createParticleExplosion(element);
            });
        });
    }
    
    createParticleExplosion(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const colors = ['#6a35ff', '#35ff6a', '#ff6a35', '#35a0ff'];
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'fixed';
            particle.style.width = '8px';
            particle.style.height = '8px';
            particle.style.borderRadius = '50%';
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.zIndex = '1000';
            particle.style.pointerEvents = 'none';
            
            document.body.appendChild(particle);
            
            const angle = Math.random() * Math.PI * 2;
            const velocity = 2 + Math.random() * 3;
            const posX = centerX;
            const posY = centerY;
            
            anime({
                targets: particle,
                translateX: posX + Math.cos(angle) * 100,
                translateY: posY + Math.sin(angle) * 100,
                opacity: [1, 0],
                scale: [1, 0.1],
                easing: 'easeOutExpo',
                duration: 1000 + Math.random() * 500,
                complete: () => {
                    document.body.removeChild(particle);
                }
            });
        }
    }
}

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const portfolioAnimations = new PortfolioAnimations();
    
    // Setup text scramble for subtitle if needed
    portfolioAnimations.setupTextScramble('.scramble-text', [
        'Web Developer',
        'UI/UX Designer',
        'Full Stack Developer',
        'Problem Solver'
    ]);
    
    // Setup particle effect for buttons
    portfolioAnimations.setupParticleEffect('.btn-primary');
});