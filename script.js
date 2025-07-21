// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize particles background
    initParticlesBackground();
    
    // Add a force-show for project cards after 3 seconds as a fallback
    setTimeout(() => {
        const projectCards = document.querySelectorAll('.project-card-container, [data-aos]');
        projectCards.forEach(card => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            card.classList.add('visible');
            card.classList.add('aos-animate'); // 🛠️ This is the fix
        });
    
        // Also make sure AOS is refreshed
        if (typeof AOS !== 'undefined') {
            AOS.refreshHard();
        }
    }, 3000);
    
    
    // Initialize other components if they haven't been initialized already
    if (!window.componentsInitialized) {
        // Initialize project hover effects
        initProjectHoverEffects();
        
        // Initialize project filters
        initProjectFilter();
        
        // Initialize form validation
        initFormValidation();
        
        // Initialize dark mode toggle
        initDarkModeToggle();
        
        // Initialize smooth scrolling
        initSmoothScrolling();
        
        // Flag that components are initialized
        window.componentsInitialized = true;
    }
});

// Initialize particles background
function initParticlesBackground() {
    // This prevents creating duplicate canvases
    if (document.getElementById('particles-canvas')) return;
    
    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    document.body.appendChild(canvas);
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-2';
    canvas.style.pointerEvents = 'none';

    const ctx = canvas.getContext('2d');
    const particles = [];
    const particleCount = 50;
    
    // Set canvas to full screen
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    // Create particles
    function createParticles() {
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 2 + 1,
                baseOpacity: 0.3 + Math.random() * 0.3,
                twinkle: Math.random() * Math.PI * 2,
                    colorRGB: {
                        r: 23 + Math.random() * 20,
                        g: 133 + Math.random() * 20,
                        b: 130 + Math.random() * 20
                    },
    speedX: Math.random() * 0.5 - 0.25,
    speedY: Math.random() * 0.5 - 0.25
            });
        }
    }
    
    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    
        particles.forEach(particle => {
            // Move particle
            particle.x += particle.speedX;
            particle.y += particle.speedY;
    
            // Wrap around edges
            if (particle.x < 0) particle.x = canvas.width;
            if (particle.x > canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = canvas.height;
            if (particle.y > canvas.height) particle.y = 0;
    
            // Twinkle animation
            particle.twinkle += 0.05; // Increase for faster pulsing
            const opacity = particle.baseOpacity + 0.2 * Math.sin(particle.twinkle);
    
            // Draw particle with twinkling opacity
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${particle.colorRGB.r}, ${particle.colorRGB.g}, ${particle.colorRGB.b}, ${opacity})`;
            ctx.fill();
        });
    
        // Draw connections between nearby particles
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
    
                if (distance < 100) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(23, 133, 130, ${0.1 * (1 - distance / 100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    
        requestAnimationFrame(drawParticles);
    }
    
    
    // Initialize
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    createParticles();
    drawParticles();
}

// Typed.js effect for hero heading
function initTypedEffect() {
    if (typeof Typed !== 'undefined') {
        const typedElement = document.querySelector('.typed-element');
        if (typedElement && !typedElement.hasChildNodes()) {
            new Typed(typedElement, {
                strings: [
                    'Quantum Chemistry Developer',
                    'Chemical Engineering Specialist',
                    'Computational Science Enthusiast'
                ],
                typeSpeed: 60,
                backSpeed: 40,
                backDelay: 1500,
                startDelay: 1000,
                loop: true
            });
        }
    }
}

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        if (!link.hasAttribute('data-smooth-scroll-init')) {
            link.setAttribute('data-smooth-scroll-init', 'true');
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            });
        }
    });
}

// Project card hover effects
function initProjectHoverEffects() {
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        if (!card.hasAttribute('data-hover-init')) {
            card.setAttribute('data-hover-init', 'true');
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-15px)';
                this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.4)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            });
        }
    });
}

// Project filter functionality
function initProjectFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-card-container');
    
    if (filterButtons.length && projectItems.length) {
        filterButtons.forEach(btn => {
            if (!btn.hasAttribute('data-filter-init')) {
                btn.setAttribute('data-filter-init', 'true');
                btn.addEventListener('click', function() {
                    const filterValue = this.getAttribute('data-filter');
                    
                    // Update active button
                    filterButtons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Filter projects
                    projectItems.forEach(item => {
                        if (filterValue === 'all' || item.classList.contains(filterValue)) {
                            item.style.display = 'block';
                            setTimeout(() => {
                                item.style.opacity = '1';
                                item.style.transform = 'translateY(0)';
                            }, 50);
                        } else {
                            item.style.opacity = '0';
                            item.style.transform = 'translateY(20px)';
                            setTimeout(() => {
                                item.style.display = 'none';
                            }, 300);
                        }
                    });
                });
            }
        });
    }
}

// Form validation
function initFormValidation() {
    const form = document.querySelector('.contact-form');
    
    if (form && !form.hasAttribute('data-validation-init')) {
        form.setAttribute('data-validation-init', 'true');
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            // Email validation
            const emailField = form.querySelector('input[type="email"]');
            if (emailField && emailField.value) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    isValid = false;
                    emailField.classList.add('error');
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                
                // Add error message
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.textContent = 'Please fill in all required fields correctly.';
                
                const existingError = form.querySelector('.error-message');
                if (existingError) {
                    existingError.remove();
                }
                
                form.prepend(errorMessage);
            }
        });
        
        // Clear error on input
        form.querySelectorAll('input, textarea').forEach(field => {
            field.addEventListener('input', function() {
                this.classList.remove('error');
            });
        });
    }
}

// Dark mode toggle
function initDarkModeToggle() {
    const toggle = document.querySelector('.dark-mode-toggle');
    
    if (toggle && !toggle.hasAttribute('data-toggle-init')) {
        toggle.setAttribute('data-toggle-init', 'true');
        
        // Check for saved user preference
        const darkMode = localStorage.getItem('darkMode') === 'enabled';
        if (darkMode) {
            document.body.classList.add('dark-mode');
            toggle.classList.add('active');
        }
        
        toggle.addEventListener('click', function() {
            // Store animation states before toggling
            const animatedElements = document.querySelectorAll('.project-card-container, [data-aos], .fade-in, .slide-up');
            
            // Add a class to prevent animations during theme change
            document.body.classList.add('theme-transitioning');
            
            // Toggle dark mode
            if (document.body.classList.contains('dark-mode')) {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'disabled');
                this.classList.remove('active');
            } else {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
                this.classList.add('active');
            }
            
            // Force all animated elements to stay visible
            animatedElements.forEach(el => {
                el.style.opacity = '1';
                el.style.transform = 'none';
                el.classList.add('visible');
                el.classList.add('aos-animate');
            });
            
            // Remove the transitioning class after the theme change is complete
            setTimeout(() => {
                document.body.classList.remove('theme-transitioning');
            }, 500);
        });
    }
}
const projectLinks = document.querySelectorAll(".view-project");

projectLinks.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        const overlay = document.getElementById("transition-overlay");
        const text = document.getElementById("transition-text");
        const gifContainer = document.getElementById("transition-gif-container");
        const gif = document.getElementById("transition-gif");

        if (link.dataset.project === "bioplastic") {
            text.textContent = "Next station: A sustainable planet 🌱";
            gif.src = "earth.gif";
        } else if (link.dataset.project === "hartree") {
            text.textContent = "Warping into quantum space-time... 🌀";
            gif.src = "warp.gif";
        } else if (link.dataset.project === "lab") {
            text.textContent = "Loading your lab goggles... 🧪";
            gif.src = "flask.gif";
        }
        

overlay.classList.add("active");

        let message = "Preparing for launch...";

        if (link.dataset.project === "bioplastic") {
            message = "Next station: A sustainable planet 🌱";
        } else if (link.dataset.project === "hartree") {
            message = "Warping into quantum space-time... 🌀";
        } else if (link.dataset.project === "lab") {
            message = "Loading your lab goggles... 🧪";
        }

        text.textContent = message;
        overlay.classList.add("active");

        setTimeout(() => {
            window.location.href = link.getAttribute("href");
        }, 5000);
    });
});

