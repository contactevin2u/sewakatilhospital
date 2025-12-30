/**
 * OxygenCare Malaysia - Main JavaScript
 * UI/UX Enhancements for better user experience
 */

(function() {
    'use strict';

    // =========================================
    // 1. SCROLL-TO-TOP BUTTON
    // =========================================
    const scrollToTop = {
        button: null,

        init() {
            this.createButton();
            this.bindEvents();
        },

        createButton() {
            this.button = document.createElement('button');
            this.button.className = 'scroll-to-top';
            this.button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="18 15 12 9 6 15"></polyline>
                </svg>
            `;
            this.button.setAttribute('aria-label', 'Kembali ke atas');
            this.button.setAttribute('title', 'Kembali ke atas');
            document.body.appendChild(this.button);
        },

        bindEvents() {
            // Show/hide button based on scroll position
            let ticking = false;
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        this.toggleVisibility();
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });

            // Smooth scroll to top on click
            this.button.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        },

        toggleVisibility() {
            if (window.scrollY > 400) {
                this.button.classList.add('visible');
            } else {
                this.button.classList.remove('visible');
            }
        }
    };

    // =========================================
    // 2. SCROLL REVEAL ANIMATIONS
    // =========================================
    const scrollReveal = {
        elements: [],

        init() {
            // Select all elements to animate
            this.elements = document.querySelectorAll(
                '.section-header, .service-card, .product-card-simple, .patient-card, ' +
                '.why-us-item, .testimonial-card, .blog-card, .faq-item, ' +
                '.trust-badge, .areas-grid > *, .footer-grid > *'
            );

            if (this.elements.length === 0) return;

            // Add initial state
            this.elements.forEach((el, index) => {
                el.classList.add('reveal');
                el.style.transitionDelay = `${(index % 4) * 0.1}s`;
            });

            // Use Intersection Observer for performance
            this.observe();
        },

        observe() {
            const options = {
                root: null,
                rootMargin: '0px 0px -50px 0px',
                threshold: 0.1
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                        observer.unobserve(entry.target);
                    }
                });
            }, options);

            this.elements.forEach(el => observer.observe(el));
        }
    };

    // =========================================
    // 3. MOBILE MENU TOGGLE
    // =========================================
    const mobileMenu = {
        toggle: null,
        menu: null,
        overlay: null,

        init() {
            this.toggle = document.querySelector('.mobile-menu-toggle, .nav-toggle, .hamburger');
            this.menu = document.querySelector('.nav-menu, .main-nav, .navigation');

            if (!this.menu) return;

            // Create toggle if it doesn't exist
            if (!this.toggle) {
                this.createToggle();
            }

            // Create overlay
            this.createOverlay();
            this.bindEvents();
        },

        createToggle() {
            const header = document.querySelector('.header-inner, .header .container');
            if (!header) return;

            this.toggle = document.createElement('button');
            this.toggle.className = 'mobile-menu-toggle';
            this.toggle.setAttribute('aria-label', 'Toggle menu');
            this.toggle.setAttribute('aria-expanded', 'false');
            this.toggle.innerHTML = `
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            `;
            header.appendChild(this.toggle);
        },

        createOverlay() {
            this.overlay = document.createElement('div');
            this.overlay.className = 'menu-overlay';
            document.body.appendChild(this.overlay);
        },

        bindEvents() {
            if (!this.toggle) return;

            this.toggle.addEventListener('click', () => this.toggleMenu());
            this.overlay.addEventListener('click', () => this.closeMenu());

            // Close on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.menu.classList.contains('active')) {
                    this.closeMenu();
                }
            });

            // Close menu on link click
            this.menu.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => this.closeMenu());
            });
        },

        toggleMenu() {
            const isOpen = this.menu.classList.toggle('active');
            this.toggle.classList.toggle('active');
            this.overlay.classList.toggle('active');
            this.toggle.setAttribute('aria-expanded', isOpen);
            document.body.style.overflow = isOpen ? 'hidden' : '';
        },

        closeMenu() {
            this.menu.classList.remove('active');
            this.toggle.classList.remove('active');
            this.overlay.classList.remove('active');
            this.toggle.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }
    };

    // =========================================
    // 4. FORM VALIDATION & FEEDBACK
    // =========================================
    const formValidation = {
        forms: [],

        init() {
            this.forms = document.querySelectorAll('form');
            if (this.forms.length === 0) return;

            this.forms.forEach(form => this.setupForm(form));
        },

        setupForm(form) {
            const inputs = form.querySelectorAll('input, select, textarea');

            inputs.forEach(input => {
                // Add wrapper for validation icons
                this.wrapInput(input);

                // Real-time validation
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => {
                    if (input.classList.contains('invalid')) {
                        this.validateField(input);
                    }
                });
            });

            // Form submission
            form.addEventListener('submit', (e) => {
                let isValid = true;
                inputs.forEach(input => {
                    if (!this.validateField(input)) {
                        isValid = false;
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                    // Focus first invalid field
                    const firstInvalid = form.querySelector('.invalid');
                    if (firstInvalid) {
                        firstInvalid.focus();
                        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        },

        wrapInput(input) {
            if (input.parentElement.classList.contains('input-wrapper')) return;

            const wrapper = document.createElement('div');
            wrapper.className = 'input-wrapper';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            // Add validation icon container
            const iconContainer = document.createElement('span');
            iconContainer.className = 'validation-icon';
            wrapper.appendChild(iconContainer);
        },

        validateField(input) {
            const wrapper = input.closest('.input-wrapper');
            if (!wrapper) return true;

            // Remove existing states
            input.classList.remove('valid', 'invalid');
            wrapper.classList.remove('valid', 'invalid');

            // Skip if not required and empty
            if (!input.required && !input.value.trim()) {
                return true;
            }

            let isValid = true;
            let errorMessage = '';

            // Check validity
            if (input.required && !input.value.trim()) {
                isValid = false;
                errorMessage = 'Sila isi ruangan ini';
            } else if (input.type === 'email' && input.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(input.value)) {
                    isValid = false;
                    errorMessage = 'Sila masukkan email yang sah';
                }
            } else if (input.type === 'tel' && input.value) {
                const phoneRegex = /^[0-9+\-\s()]{8,}$/;
                if (!phoneRegex.test(input.value)) {
                    isValid = false;
                    errorMessage = 'Sila masukkan nombor telefon yang sah';
                }
            } else if (input.minLength && input.value.length < input.minLength) {
                isValid = false;
                errorMessage = `Minimum ${input.minLength} aksara diperlukan`;
            }

            // Update classes
            const stateClass = isValid ? 'valid' : 'invalid';
            input.classList.add(stateClass);
            wrapper.classList.add(stateClass);

            // Update error message
            let errorEl = wrapper.querySelector('.error-message');
            if (!isValid) {
                if (!errorEl) {
                    errorEl = document.createElement('span');
                    errorEl.className = 'error-message';
                    wrapper.appendChild(errorEl);
                }
                errorEl.textContent = errorMessage;
            } else if (errorEl) {
                errorEl.remove();
            }

            return isValid;
        }
    };

    // =========================================
    // 5. IMAGE LOADING EFFECTS
    // =========================================
    const imageLoader = {
        init() {
            const images = document.querySelectorAll('img[loading="lazy"]');

            images.forEach(img => {
                // Add loading class
                img.classList.add('img-loading');

                // Handle load event
                if (img.complete) {
                    this.handleLoaded(img);
                } else {
                    img.addEventListener('load', () => this.handleLoaded(img));
                    img.addEventListener('error', () => this.handleError(img));
                }
            });
        },

        handleLoaded(img) {
            img.classList.remove('img-loading');
            img.classList.add('img-loaded');
        },

        handleError(img) {
            img.classList.remove('img-loading');
            img.classList.add('img-error');
            // Could add fallback image here
        }
    };

    // =========================================
    // 6. SMOOTH ANCHOR SCROLLING
    // =========================================
    const smoothScroll = {
        init() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => {
                    const targetId = anchor.getAttribute('href');
                    if (targetId === '#') return;

                    const target = document.querySelector(targetId);
                    if (target) {
                        e.preventDefault();
                        const headerOffset = 80;
                        const elementPosition = target.getBoundingClientRect().top;
                        const offsetPosition = elementPosition + window.scrollY - headerOffset;

                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'smooth'
                        });

                        // Update URL without jumping
                        history.pushState(null, null, targetId);
                    }
                });
            });
        }
    };

    // =========================================
    // 7. HEADER SCROLL EFFECT
    // =========================================
    const headerScroll = {
        header: null,
        lastScroll: 0,

        init() {
            this.header = document.querySelector('.header');
            if (!this.header) return;

            let ticking = false;
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        this.handleScroll();
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });
        },

        handleScroll() {
            const currentScroll = window.scrollY;

            // Add shadow when scrolled
            if (currentScroll > 10) {
                this.header.classList.add('scrolled');
            } else {
                this.header.classList.remove('scrolled');
            }

            // Hide/show on scroll direction (optional - for mobile)
            if (window.innerWidth <= 768) {
                if (currentScroll > this.lastScroll && currentScroll > 200) {
                    this.header.classList.add('header-hidden');
                } else {
                    this.header.classList.remove('header-hidden');
                }
            }

            this.lastScroll = currentScroll;
        }
    };

    // =========================================
    // 8. FAQ ACCORDION ENHANCEMENT
    // =========================================
    const faqAccordion = {
        init() {
            const faqItems = document.querySelectorAll('.faq-item, details');

            faqItems.forEach(item => {
                const summary = item.querySelector('summary');
                if (!summary) return;

                summary.addEventListener('click', (e) => {
                    // Close other items (optional - for single open behavior)
                    // faqItems.forEach(other => {
                    //     if (other !== item && other.open) {
                    //         other.open = false;
                    //     }
                    // });
                });
            });
        }
    };

    // =========================================
    // 9. COUNTER ANIMATION
    // =========================================
    const counterAnimation = {
        init() {
            const counters = document.querySelectorAll('.proof-number, .stat-number, [data-count]');
            if (counters.length === 0) return;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            counters.forEach(counter => observer.observe(counter));
        },

        animateCounter(element) {
            const text = element.textContent;
            const match = text.match(/[\d,]+/);
            if (!match) return;

            const target = parseInt(match[0].replace(/,/g, ''));
            const prefix = text.substring(0, text.indexOf(match[0]));
            const suffix = text.substring(text.indexOf(match[0]) + match[0].length);
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                element.textContent = prefix + Math.floor(current).toLocaleString() + suffix;
            }, 16);
        }
    };

    // =========================================
    // 10. LAZY LOAD VIDEOS (if any)
    // =========================================
    const videoLoader = {
        init() {
            const videos = document.querySelectorAll('video[data-src], iframe[data-src]');
            if (videos.length === 0) return;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const video = entry.target;
                        video.src = video.dataset.src;
                        video.removeAttribute('data-src');
                        observer.unobserve(video);
                    }
                });
            }, { rootMargin: '100px' });

            videos.forEach(video => observer.observe(video));
        }
    };

    // =========================================
    // INITIALIZE ALL MODULES
    // =========================================
    function init() {
        // Core functionality
        scrollToTop.init();
        scrollReveal.init();
        mobileMenu.init();
        smoothScroll.init();
        headerScroll.init();

        // Enhanced interactions
        formValidation.init();
        imageLoader.init();
        faqAccordion.init();
        counterAnimation.init();
        videoLoader.init();

        // Log initialization
        console.log('OxygenCare: UI/UX enhancements loaded');
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
