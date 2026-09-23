/* ==========================================================================
   Digital Darts - Main JavaScript & Enhanced GSAP Animations + Form Validation
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Navbar Scroll Shrink & Glass Effect
  const navbar = document.querySelector('.navbar-custom');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // 2. GSAP & ScrollTrigger Animations
  if (typeof gsap !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Hero Timeline Reveal
    const heroTl = gsap.timeline();
    heroTl.fromTo('.hero-badge', { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' })
      .fromTo('.hero-title', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '-=0.4')
      .fromTo('.hero-subtitle', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' }, '-=0.5')
      .fromTo('.hero-cta-group', { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }, '-=0.4')
      .fromTo('.hero-img-wrapper', { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.8, ease: 'power3.out' }, '-=0.4');

    // Floating Cards Continuous Parallax Movement
    gsap.to('.hero-floating-card.card-top-right', {
      y: -14,
      duration: 3.2,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });
    gsap.to('.hero-floating-card.card-bottom-left', {
      y: 14,
      duration: 3.8,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
      delay: 0.4
    });

    // Section Title ScrollTrigger Reveal
    gsap.utils.toArray('.section-title-reveal').forEach(title => {
      gsap.fromTo(title, 
        { opacity: 0.2, y: 25 },
        {
          scrollTrigger: {
            trigger: title,
            start: 'top 90%'
          },
          opacity: 1,
          y: 0,
          duration: 0.7,
          ease: 'power3.out'
        }
      );
    });

    // GSAP ScrollTrigger Entrance Animation for Rule Cards
    gsap.fromTo('.rule-card', 
      { opacity: 0.3, y: 30, scale: 0.97 },
      {
        scrollTrigger: {
          trigger: '.rules-section',
          start: 'top 90%'
        },
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.7,
        stagger: 0.12,
        ease: 'power3.out'
      }
    );

    // Service Cards Stagger Reveal
    gsap.fromTo('.service-card', 
      { opacity: 0.3, y: 30, scale: 0.97 },
      {
        scrollTrigger: {
          trigger: '.services-section',
          start: 'top 90%'
        },
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.7,
        stagger: 0.12,
        ease: 'power3.out'
      }
    );

    // Case Study Cards Stagger Reveal
    gsap.fromTo('.case-card', 
      { opacity: 0.3, y: 30, scale: 0.97 },
      {
        scrollTrigger: {
          trigger: '.case-card',
          start: 'top 90%'
        },
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.7,
        stagger: 0.12,
        ease: 'power3.out'
      }
    );

    // Interactive GSAP 3D Mouse Tilt Effect for Rule Cards & Service Cards
    const interactiveCards = document.querySelectorAll('.rule-card, .service-card, .case-card');
    interactiveCards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        gsap.to(card, {
          rotationY: x * 0.05,
          rotationX: -y * 0.05,
          transformPerspective: 1000,
          ease: 'power1.out',
          duration: 0.3
        });
      });

      card.addEventListener('mouseleave', () => {
        gsap.to(card, {
          rotationY: 0,
          rotationX: 0,
          ease: 'power2.out',
          duration: 0.5
        });
      });
    });

    // Count-Up Numbers ScrollTrigger
    const counterElements = document.querySelectorAll('.counter-val');
    counterElements.forEach(counter => {
      const target = parseFloat(counter.getAttribute('data-target'));
      const prefix = counter.getAttribute('data-prefix') || '';
      const suffix = counter.getAttribute('data-suffix') || '';
      const decimals = parseInt(counter.getAttribute('data-decimals') || '0', 10);

      ScrollTrigger.create({
        trigger: counter,
        start: 'top 90%',
        onEnter: () => {
          gsap.to({ val: 0 }, {
            val: target,
            duration: 2.2,
            ease: 'power2.out',
            onUpdate: function () {
              counter.innerText = prefix + this.targets()[0].val.toFixed(decimals) + suffix;
            }
          });
        }
      });
    });
  }

  // 3. Interactive Shopify ROI Calculator
  const trafficSlider = document.getElementById('monthlyTraffic');
  const convSlider = document.getElementById('currentConvRate');
  const aovSlider = document.getElementById('avgOrderValue');

  const trafficValText = document.getElementById('trafficVal');
  const convValText = document.getElementById('convVal');
  const aovValText = document.getElementById('aovVal');

  const estRevenueText = document.getElementById('estMonthlyProfit');
  const estGrowthLiftText = document.getElementById('estGrowthLift');

  function calculateROI() {
    if (!trafficSlider || !convSlider || !aovSlider) return;

    const traffic = parseFloat(trafficSlider.value);
    const currentConv = parseFloat(convSlider.value) / 100;
    const aov = parseFloat(aovSlider.value);

    // Digital Darts benchmark: +75% lift
    const targetConv = currentConv * 1.75; 
    const currentMonthlyRevenue = traffic * currentConv * aov;
    const projectedMonthlyRevenue = traffic * targetConv * aov;
    const monthlyLift = projectedMonthlyRevenue - currentMonthlyRevenue;

    if (trafficValText) trafficValText.innerText = traffic.toLocaleString() + ' visitors';
    if (convValText) convValText.innerText = (currentConv * 100).toFixed(1) + '%';
    if (aovValText) aovValText.innerText = '$' + aov;

    if (estRevenueText) {
      estRevenueText.innerText = '+$' + Math.round(monthlyLift).toLocaleString();
    }
    if (estGrowthLiftText) {
      estGrowthLiftText.innerText = '+$' + Math.round(monthlyLift * 12).toLocaleString() + ' / year';
    }
  }

  if (trafficSlider && convSlider && aovSlider) {
    trafficSlider.addEventListener('input', calculateROI);
    convSlider.addEventListener('input', calculateROI);
    aovSlider.addEventListener('input', calculateROI);
    calculateROI();
  }

  // 4. Case Studies Category Filter
  const filterBtns = document.querySelectorAll('.case-filter-btn');
  const caseCards = document.querySelectorAll('.case-item');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active', 'btn-copper'));
      filterBtns.forEach(b => b.classList.add('btn-outline-espresso'));
      btn.classList.add('active', 'btn-copper');
      btn.classList.remove('btn-outline-espresso');

      const category = btn.getAttribute('data-filter');

      caseCards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category').includes(category)) {
          card.style.display = 'block';
          if (typeof gsap !== 'undefined') {
            gsap.fromTo(card, { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.4 });
          }
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // 5. HTML5 & JavaScript Real-Time Form Validation
  const validateForm = (form) => {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
      let fieldValid = true;
      const val = input.value.trim();

      if (val === '') {
        fieldValid = false;
      } else if (input.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(val)) fieldValid = false;
      } else if (input.type === 'url') {
        const urlRegex = /^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/.*)?$/i;
        if (!urlRegex.test(val)) fieldValid = false;
      }

      if (fieldValid) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
      } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        isValid = false;
      }
    });

    return isValid;
  };

  const auditForm = document.getElementById('auditForm');
  if (auditForm) {
    auditForm.addEventListener('submit', (e) => {
      e.preventDefault();

      if (validateForm(auditForm)) {
        const submitBtn = auditForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting Audit Request...';

        setTimeout(() => {
          submitBtn.innerHTML = '<i class="fas fa-check-circle"></i> Audit Submitted! Senior strategist notified.';
          submitBtn.classList.remove('btn-copper');
          submitBtn.classList.add('btn-sage');
          auditForm.reset();
        }, 1200);
      }
    });
  }

  const playbookForm = document.getElementById('playbookForm');
  if (playbookForm) {
    playbookForm.addEventListener('submit', (e) => {
      e.preventDefault();

      if (validateForm(playbookForm)) {
        const submitBtn = playbookForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating PDF Link...';

        setTimeout(() => {
          submitBtn.innerHTML = '<i class="fas fa-check-circle"></i> Playbook Download Sent to Email!';
          submitBtn.classList.remove('btn-copper');
          submitBtn.classList.add('btn-sage');
          playbookForm.reset();
        }, 1200);
      }
    });
  }
});
