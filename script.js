// ===========================
// Three.js 3D Background
// ===========================
(function initThreeJS() {
    const canvas = document.getElementById('three-canvas');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    camera.position.z = 30;

    // Floating particles
    const particlesCount = 600;
    const particlesGeometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particlesCount * 3);
    const colors = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount; i++) {
        const i3 = i * 3;
        positions[i3]     = (Math.random() - 0.5) * 80;
        positions[i3 + 1] = (Math.random() - 0.5) * 80;
        positions[i3 + 2] = (Math.random() - 0.5) * 80;

        // Purple/blue tones
        colors[i3]     = 0.3 + Math.random() * 0.3;
        colors[i3 + 1] = 0.2 + Math.random() * 0.2;
        colors[i3 + 2] = 0.8 + Math.random() * 0.2;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.12,
        vertexColors: true,
        transparent: true,
        opacity: 0.7,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });

    const particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);

    // Wireframe torus
    const torusGeometry = new THREE.TorusGeometry(10, 3, 16, 100);
    const torusMaterial = new THREE.MeshBasicMaterial({
        color: 0x6c63ff,
        wireframe: true,
        transparent: true,
        opacity: 0.08,
    });
    const torus = new THREE.Mesh(torusGeometry, torusMaterial);
    torus.position.set(20, -5, -15);
    scene.add(torus);

    // Wireframe icosahedron
    const icoGeometry = new THREE.IcosahedronGeometry(6, 1);
    const icoMaterial = new THREE.MeshBasicMaterial({
        color: 0x48c6ef,
        wireframe: true,
        transparent: true,
        opacity: 0.08,
    });
    const ico = new THREE.Mesh(icoGeometry, icoMaterial);
    ico.position.set(-18, 8, -10);
    scene.add(ico);

    // Wireframe octahedron
    const octGeometry = new THREE.OctahedronGeometry(4, 0);
    const octMaterial = new THREE.MeshBasicMaterial({
        color: 0xf093fb,
        wireframe: true,
        transparent: true,
        opacity: 0.06,
    });
    const oct = new THREE.Mesh(octGeometry, octMaterial);
    oct.position.set(15, 12, -8);
    scene.add(oct);

    // Connecting lines between random particles
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x6c63ff,
        transparent: true,
        opacity: 0.04,
    });

    const lineSegments = [];
    for (let i = 0; i < 40; i++) {
        const lineGeometry = new THREE.BufferGeometry();
        const a = Math.floor(Math.random() * particlesCount) * 3;
        const b = Math.floor(Math.random() * particlesCount) * 3;
        const linePositions = new Float32Array([
            positions[a], positions[a+1], positions[a+2],
            positions[b], positions[b+1], positions[b+2],
        ]);
        lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
        const line = new THREE.Line(lineGeometry, lineMaterial);
        scene.add(line);
        lineSegments.push(line);
    }

    // Mouse interaction
    let mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    });

    // Scroll offset for parallax
    let scrollY = 0;
    window.addEventListener('scroll', () => {
        scrollY = window.scrollY;
    });

    // Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Animate
    function animate() {
        requestAnimationFrame(animate);

        const time = Date.now() * 0.001;

        particles.rotation.y = time * 0.02 + mouseX * 0.1;
        particles.rotation.x = time * 0.015 + mouseY * 0.1;

        torus.rotation.x = time * 0.12;
        torus.rotation.y = time * 0.08;

        ico.rotation.x = time * 0.1;
        ico.rotation.z = time * 0.06;

        oct.rotation.y = time * 0.15;
        oct.rotation.z = time * 0.1;

        // Parallax with scroll
        camera.position.y = -scrollY * 0.005;

        renderer.render(scene, camera);
    }

    animate();
})();

// ===========================
// Typing Effect
// ===========================
(function initTypingEffect() {
    const titles = [
        'Software Engineer',
        'Full-Stack Developer',
        'Cloud & DevOps Engineer',
        'Flutter Developer',
    ];
    const el = document.getElementById('typedText');
    let titleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
        const current = titles[titleIndex];

        if (isDeleting) {
            el.textContent = current.substring(0, charIndex - 1);
            charIndex--;
        } else {
            el.textContent = current.substring(0, charIndex + 1);
            charIndex++;
        }

        let speed = isDeleting ? 40 : 80;

        if (!isDeleting && charIndex === current.length) {
            speed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            titleIndex = (titleIndex + 1) % titles.length;
            speed = 500;
        }

        setTimeout(type, speed);
    }

    type();
})();

// ===========================
// Navbar Scroll Effects
// ===========================
(function initNavbar() {
    const nav = document.getElementById('navbar');
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.section');
    const navToggle = document.getElementById('navToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileLinks = mobileMenu.querySelectorAll('a');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }

        // Active section detection
        let current = '';
        sections.forEach(section => {
            const top = section.offsetTop - 200;
            if (window.scrollY >= top) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });

    // Mobile toggle
    navToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
    });

    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
        });
    });
})();

// ===========================
// Scroll Animations
// ===========================
(function initScrollAnimations() {
    const animatedElements = document.querySelectorAll(
        '.timeline-item, .project-card, .skill-category, .education-card, .cert-card, .lang-card'
    );

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');

                    // Animate language bars
                    const langFill = entry.target.querySelector('.lang-fill');
                    if (langFill) {
                        langFill.classList.add('animated');
                        langFill.style.width = langFill.parentElement.parentElement.querySelector('.lang-fill').style.width || langFill.getAttribute('style').match(/width:\s*(\d+%)/)?.[1] || '0%';
                    }
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px',
    });

    animatedElements.forEach(el => observer.observe(el));
})();

// ===========================
// Counter Animation
// ===========================
(function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    let started = false;

    function animateCounters() {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 1500;
            const startTime = Date.now();

            function updateCounter() {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease-out cubic
                const eased = 1 - Math.pow(1 - progress, 3);
                counter.textContent = Math.round(eased * target);

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                }
            }

            updateCounter();
        });
    }

    const statsObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && !started) {
            started = true;
            animateCounters();
        }
    }, { threshold: 0.5 });

    const statsSection = document.querySelector('.about-stats');
    if (statsSection) statsObserver.observe(statsSection);
})();

// ===========================
// Language Bar Fix
// ===========================
(function initLangBars() {
    const langCards = document.querySelectorAll('.lang-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fill = entry.target.querySelector('.lang-fill');
                if (fill) {
                    const targetWidth = fill.closest('.lang-card').querySelector('.lang-fill').getAttribute('style');
                    const match = targetWidth && targetWidth.match(/width:\s*(\d+%)/);
                    if (match) {
                        fill.style.setProperty('width', match[1], 'important');
                    }
                }
            }
        });
    }, { threshold: 0.5 });

    langCards.forEach(card => observer.observe(card));
})();

// ===========================
// Smooth Scroll for Anchors
// ===========================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
