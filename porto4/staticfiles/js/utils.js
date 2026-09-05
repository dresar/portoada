// Utility functions for Portfolio Website

// Loader functionality
class PageLoader {
    constructor() {
        this.loader = document.querySelector('.loader');
        this.init();
    }
    
    init() {
        if (!this.loader) return;
        
        // Hide loader after page loads
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.hideLoader();
            }, 500);
        });
        
        // Fallback to hide loader if load event doesn't fire
        setTimeout(() => {
            this.hideLoader();
        }, 3000);
    }
    
    hideLoader() {
        if (!this.loader) return;
        this.loader.classList.add('hidden');
    }
}

// Theme management
class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.colorChangerToggle = document.getElementById('color-changer-toggle');
        this.colorChangerPanel = document.getElementById('color-changer-panel');
        this.colorButtons = document.querySelectorAll('.color-btn');
        
        this.init();
    }
    
    init() {
        this.loadSavedPreferences();
        this.setupEventListeners();
    }
    
    loadSavedPreferences() {
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
    
    setupEventListeners() {
        // Theme toggle
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => {
                document.body.classList.toggle('light-theme');
                
                // Save theme preference to localStorage
                const isLightTheme = document.body.classList.contains('light-theme');
                localStorage.setItem('light-theme', isLightTheme);
                
                // Update theme toggle icon
                const themeIcon = this.themeToggle.querySelector('i');
                if (isLightTheme) {
                    themeIcon.classList.remove('fa-sun');
                    themeIcon.classList.add('fa-moon');
                } else {
                    themeIcon.classList.remove('fa-moon');
                    themeIcon.classList.add('fa-sun');
                }
            });
        }
        
        // Color changer toggle
        if (this.colorChangerToggle && this.colorChangerPanel) {
            this.colorChangerToggle.addEventListener('click', () => {
                this.colorChangerPanel.classList.toggle('open');
            });
            
            // Change primary color
            this.colorButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const color = button.getAttribute('data-color');
                    document.documentElement.style.setProperty('--primary-color', color);
                    
                    // Remove active class from all buttons
                    this.colorButtons.forEach(btn => btn.classList.remove('active'));
                    
                    // Add active class to clicked button
                    button.classList.add('active');
                    
                    // Save color preference to localStorage
                    localStorage.setItem('primary-color', color);
                });
            });
        }
    }
}

// Navigation functionality
class Navigation {
    constructor() {
        this.mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        this.mobileMenu = document.getElementById('mobile-menu');
        this.mobileMenuLinks = document.querySelectorAll('.mobile-menu a');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.scrollToTopBtn = document.getElementById('scroll-to-top');
        
        this.init();
    }
    
    init() {
        this.setupMobileMenu();
        this.setupSmoothScroll();
        this.setupScrollToTop();
        this.setupActiveNavOnScroll();
    }
    
    setupMobileMenu() {
        // Mobile menu toggle
        if (this.mobileMenuToggle && this.mobileMenu) {
            this.mobileMenuToggle.addEventListener('click', () => {
                this.mobileMenu.classList.toggle('open');
                document.body.classList.toggle('overflow-hidden');
            });
            
            // Close mobile menu when clicking a link
            this.mobileMenuLinks.forEach(link => {
                link.addEventListener('click', () => {
                    this.mobileMenu.classList.remove('open');
                    document.body.classList.remove('overflow-hidden');
                });
            });
        }
    }
    
    setupSmoothScroll() {
        // Smooth scroll for navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = link.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    // Remove active class from all links
                    this.navLinks.forEach(navLink => navLink.classList.remove('active'));
                    
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
    }
    
    setupScrollToTop() {
        // Scroll to top button
        if (this.scrollToTopBtn) {
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 300) {
                    this.scrollToTopBtn.style.opacity = '1';
                    this.scrollToTopBtn.style.pointerEvents = 'auto';
                } else {
                    this.scrollToTopBtn.style.opacity = '0';
                    this.scrollToTopBtn.style.pointerEvents = 'none';
                }
            });
            
            this.scrollToTopBtn.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }
    
    setupActiveNavOnScroll() {
        // Set active nav link based on scroll position
        window.addEventListener('scroll', () => {
            const scrollPosition = window.scrollY;
            
            // Get all sections
            const sections = document.querySelectorAll('section');
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');
                
                if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                    // Remove active class from all links
                    this.navLinks.forEach(navLink => navLink.classList.remove('active'));
                    
                    // Add active class to corresponding link
                    const activeLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
                    if (activeLink) {
                        activeLink.classList.add('active');
                    }
                }
            });
        });
    }
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    
    // Show notification
    showNotification('Copied to clipboard!');
}

// Show notification
function showNotification(message, type = 'success', duration = 2000) {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 left-1/2 transform -translate-x-1/2 px-4 py-2 rounded-lg shadow-lg z-50 ${type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white`;
    notification.textContent = message;
    notification.style.transition = 'opacity 0.3s ease';
    document.body.appendChild(notification);
    
    // Remove notification after duration
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, duration);
}

// Initialize utilities when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PageLoader();
    new ThemeManager();
    new Navigation();
    
    // Setup copy buttons
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const textToCopy = button.getAttribute('data-copy');
            copyToClipboard(textToCopy);
        });
    });
});