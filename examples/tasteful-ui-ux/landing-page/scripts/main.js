(() => {
  "use strict";

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Scroll reveal: fade/slide elements into view once, then stop observing them. */
  const revealTargets = document.querySelectorAll("[data-reveal]");

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    revealTargets.forEach((el) => el.classList.add("is-visible"));
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -10% 0px" }
    );

    revealTargets.forEach((el) => revealObserver.observe(el));
  }

  /* Magnetic CTA: nudges the primary hero button toward the pointer. Desktop, fine-pointer only. */
  const magneticCta = document.getElementById("magnetic-cta");
  const supportsHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  if (magneticCta && supportsHover && !prefersReducedMotion) {
    const strength = 0.25;

    magneticCta.addEventListener("mousemove", (event) => {
      const rect = magneticCta.getBoundingClientRect();
      const offsetX = (event.clientX - (rect.left + rect.width / 2)) * strength;
      const offsetY = (event.clientY - (rect.top + rect.height / 2)) * strength;
      magneticCta.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
    });

    magneticCta.addEventListener("mouseleave", () => {
      magneticCta.style.transform = "translate(0, 0)";
    });
  }
})();
