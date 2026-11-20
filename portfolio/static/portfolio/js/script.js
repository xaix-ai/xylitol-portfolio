/* ==========================================================================
   XY NEX KY YM — OCEAN PIXEL BEACH PORTFOLIO
   script.js

   1. Greeting interaction (29 languages)
   2. Beach time themes
   3. Philippine clock (Asia/Manila)
   4. Testudo's dialogue
   5. Portfolio panel (navbar + bookmarks)
   6. Testudo walking
   ========================================================================== */

(function () {
    "use strict";

    const beach = document.querySelector(".hero");
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");


    /* 1. GREETING INTERACTION ---------------------------------------------- */

    const greetings = [
        "Hello, I'm Xynex Kim.",
        "Kamusta, ako si Xynex Kim.",
        "Hola, soy Xynex Kim.",
        "Bonjour, je m'appelle Xynex Kim.",
        "Ciao, sono Xynex Kim.",
        "Olá, eu sou Xynex Kim.",
        "Hallo, ich bin Xynex Kim.",
        "こんにちは、Xynex Kimです。",
        "안녕하세요, 저는 Xynex Kim입니다.",
        "你好，我是 Xynex Kim。",
        "สวัสดี ฉันชื่อ Xynex Kim",
        "Привет, меня зовут Xynex Kim.",
        "مرحبا، أنا Xynex Kim.",
        "Namaste, main Xynex Kim hoon.",
        "Hej, jag heter Xynex Kim.",
        "Xin chào, tôi là Xynex Kim.",
        "Halo, saya Xynex Kim.",
        "Merhaba, ben Xynex Kim.",
        "Hallo, ik ben Xynex Kim.",
        "Cześć, jestem Xynex Kim.",
        "Γεια σας, είμαι ο Xynex Kim.",
        "Hei, jeg heter Xynex Kim.",
        "Hei, olen Xynex Kim.",
        "Sawubona, ngingu-Xynex Kim.",
        "Jambo, mimi ni Xynex Kim.",
        "שלום, אני Xynex Kim.",
        "سلام، من Xynex Kim هستم.",
        "Bună, eu sunt Xynex Kim.",
        "Ahoj, já jsem Xynex Kim."
    ];

    const greetingElement = document.getElementById("greeting");

    function changeGreeting() {
        const currentGreeting = greetingElement.textContent.trim();

        let newGreeting;

        do {
            newGreeting = greetings[Math.floor(Math.random() * greetings.length)];
        } while (newGreeting === currentGreeting);

        greetingElement.classList.add("fade-out");

        setTimeout(() => {
            greetingElement.textContent = newGreeting;
            greetingElement.classList.remove("fade-out");
        }, 300);
    }

    if (greetingElement) {
        greetingElement.addEventListener("click", changeGreeting);

        // keyboard users can change it too (Enter / Space)
        greetingElement.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                changeGreeting();
            }
        });
    }


    /* 2. BEACH TIME THEMES ------------------------------------------------- */
    // Dawn 5–7 AM · Day 8 AM–3 PM · Sunset 4–6 PM · Night 7 PM–4 AM

    function updateBeachTheme() {
        if (!beach) return;

        const hour = new Date().getHours();

        let theme;

        if (hour >= 5 && hour < 8) {
            theme = "dawn";
        } else if (hour >= 8 && hour < 16) {
            theme = "day";
        } else if (hour >= 16 && hour < 19) {
            theme = "sunset";
        } else {
            theme = "night";
        }

        if (beach.dataset.theme !== theme) {
            beach.dataset.theme = theme;
        }
    }

    updateBeachTheme();

    // Check again every minute
    setInterval(updateBeachTheme, 60000);


    /* 3. PHILIPPINE CLOCK -------------------------------------------------- */

    const clockTime = document.getElementById("ph-clock-time");

    const clockFormat = new Intl.DateTimeFormat("en-PH", {
        timeZone: "Asia/Manila",
        hour: "numeric",
        minute: "2-digit",
        second: "2-digit",
        hour12: true
    });

    const isoFormat = new Intl.DateTimeFormat("sv-SE", {
        timeZone: "Asia/Manila",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });

    function tickClock() {
        if (!clockTime) return;

        const now = new Date();

        clockTime.textContent = clockFormat.format(now).replace(/\s?([ap])\.?m\.?/i, (m, p) => " " + p.toUpperCase() + "M");
        clockTime.setAttribute("datetime", isoFormat.format(now).replace(" ", "T") + "+08:00");

        // line the next tick up with the start of the next second
        setTimeout(tickClock, 1000 - (now.getTime() % 1000) + 10);
    }

    tickClock();


    /* 4. TESTUDO'S DIALOGUE ------------------------------------------------ */

    const TESTUDO_LINES = {
        home: "Psst! Click the greeting to hear it in different languages!",
        about: "Let's get to know the human behind this portfolio!",
        projects: "Ooh! Let's explore some projects!",
        skills: "These are the tools and skills being learned!",
        experience: "Look at all the things they've been working on!",
        education: "Knowledge is power! Let's see their learning journey!",
        certificates: "Achievement unlocked! Check out these certificates!",
        achievements: "Look what they've accomplished!",
        contact: "Want to say hello? Let's get in touch!"
    };

    const DIALOGUE_DURATION = 6500;

    const turtle = document.getElementById("testudo");
    const turtleBody = document.getElementById("turtle-body");
    const dialogue = document.getElementById("turtle-dialogue");
    const dialogueText = document.getElementById("turtle-dialogue-text");

    let dialogueTimer = null;
    let introTimer = null;
    let currentSection = "home";

    function testudoSays(section) {
        if (!dialogue || !dialogueText) return;

        const line = TESTUDO_LINES[section] || TESTUDO_LINES.home;

        clearTimeout(dialogueTimer);
        clearTimeout(introTimer);

        // quick hide/show so a new line visibly "pops" even if one is showing
        dialogue.classList.remove("is-visible");

        requestAnimationFrame(() => {
            dialogueText.textContent = line;
            dialogue.classList.add("is-visible");
        });

        dialogueTimer = setTimeout(() => {
            dialogue.classList.remove("is-visible");
        }, DIALOGUE_DURATION);
    }

    if (turtleBody) {
        turtleBody.addEventListener("click", () => testudoSays(currentSection));
    }


    /* 5. PORTFOLIO PANEL --------------------------------------------------- */

    const PANELS = {
        about:        { title: "About Me",     icon: "icon-user" },
        projects:     { title: "Projects",     icon: "icon-folder" },
        skills:       { title: "Skills",       icon: "icon-code" },
        experience:   { title: "Experience",   icon: "icon-briefcase" },
        education:    { title: "Education",    icon: "icon-graduation" },
        certificates: { title: "Certificates", icon: "icon-certificate" },
        achievements: { title: "Achievements", icon: "icon-trophy" },
        contact:      { title: "Contact",      icon: "icon-mail" }
    };

    const overlay = document.getElementById("panel-overlay");
    const panel = document.getElementById("glass-panel");
    const panelTitle = document.getElementById("panel-title");
    const panelIconUse = document.querySelector("#panel-icon use");
    const panelContent = document.getElementById("panel-content");
    const closeButton = document.getElementById("panel-close");
    const sections = document.querySelectorAll(".panel-section");
    const panelTriggers = document.querySelectorAll("[data-open-panel]");
    const homeLinks = document.querySelectorAll("[data-home]");
    const navLinks = document.querySelectorAll(".nav-links a");
    const bookmarks = document.querySelectorAll(".bookmark");

    let lastTrigger = null;

    function setActive(section) {
        navLinks.forEach((link) => {
            const target = link.dataset.openPanel || (link.hasAttribute("data-home") ? "home" : "");
            const isActive = target === section;
            link.classList.toggle("active", isActive);
            if (isActive) {
                link.setAttribute("aria-current", "page");
            } else {
                link.removeAttribute("aria-current");
            }
        });

        bookmarks.forEach((bookmark) => {
            const isActive = bookmark.dataset.openPanel === section;
            bookmark.classList.toggle("is-active", isActive);
            bookmark.setAttribute("aria-pressed", isActive ? "true" : "false");
        });
    }

    function updateHash(section) {
        const url = section === "home"
            ? window.location.pathname + window.location.search
            : "#" + section;
        history.replaceState(null, "", url);
    }

    function openPanel(section, trigger) {
        const config = PANELS[section];
        if (!config || !overlay || !panel) return;

        const isAlreadyOpen = !overlay.hidden;
        if (!isAlreadyOpen) {
            lastTrigger = trigger || document.activeElement;
        }

        sections.forEach((el) => {
            el.hidden = el.dataset.panel !== section;
        });

        if (panelTitle) panelTitle.textContent = config.title;
        if (panelIconUse) panelIconUse.setAttribute("href", "#" + config.icon);
        if (panelContent) panelContent.scrollTop = 0;

        overlay.hidden = false;
        beach.classList.add("is-panel-open");

        currentSection = section;
        setActive(section);
        updateHash(section);
        testudoSays(section);

        if (!isAlreadyOpen) {
            panel.focus({ preventScroll: true });
        }
    }

    function closePanel(options = {}) {
        if (!overlay || overlay.hidden) return;

        overlay.hidden = true;
        beach.classList.remove("is-panel-open");

        currentSection = "home";
        setActive("home");
        updateHash("home");

        if (options.sayHome) testudoSays("home");

        if (lastTrigger && typeof lastTrigger.focus === "function" && document.contains(lastTrigger)) {
            lastTrigger.focus({ preventScroll: true });
        }
        lastTrigger = null;
    }

    panelTriggers.forEach((trigger) => {
        trigger.addEventListener("click", (event) => {
            event.preventDefault();
            openPanel(trigger.dataset.openPanel, trigger);
        });
    });

    homeLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            if (overlay && !overlay.hidden) {
                closePanel({ sayHome: true });
            } else {
                currentSection = "home";
                setActive("home");
                testudoSays("home");
            }
        });
    });

    if (closeButton) {
        closeButton.addEventListener("click", () => closePanel());
    }

    if (overlay) {
        // click on the dimmed area (not the panel) closes it
        overlay.addEventListener("click", (event) => {
            if (event.target === overlay) closePanel();
        });
    }

    document.addEventListener("keydown", (event) => {
        if (!overlay || overlay.hidden) return;

        if (event.key === "Escape") {
            closePanel();
            return;
        }

        // keep Tab focus inside the panel while it is open
        if (event.key === "Tab" && panel) {
            const focusable = panel.querySelectorAll(
                'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
            );
            const visible = Array.from(focusable).filter((el) => el.offsetParent !== null);
            if (!visible.length) return;

            const first = visible[0];
            const last = visible[visible.length - 1];

            if (event.shiftKey && (document.activeElement === first || document.activeElement === panel)) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        }
    });

    // open straight into a section from a shared link like /#projects
    const initialSection = window.location.hash.replace("#", "");

    if (PANELS[initialSection]) {
        openPanel(initialSection);
    } else {
        introTimer = setTimeout(() => testudoSays("home"), 900);
    }


    /* 6. TESTUDO WALKING ------------------------------------------------------
       One lightweight requestAnimationFrame loop that only moves a transform.
       It pauses by itself when the tab is hidden. */

    const WALK_SPEED = 26;      // px per second
    const PAUSE_AT_EDGE = 1600; // ms Testudo stops to look around before turning

    let x = 0;
    let direction = 1;
    let minX = 0;
    let maxX = 0;
    let pausedUntil = 0;
    let lastTime = 0;
    let walking = false;

    function measureBounds() {
        if (!turtle || !beach) return;

        const beachWidth = beach.clientWidth;
        const turtleWidth = turtle.offsetWidth || 144;
        const sideMargin = beachWidth < 600 ? 10 : 24;

        minX = sideMargin;
        maxX = Math.max(minX, beachWidth - turtleWidth - sideMargin);
        x = Math.min(Math.max(x, minX), maxX);
    }

    function placeTurtle() {
        // snap to 2px steps so the pixel art stays crisp
        const snapped = Math.round(x / 2) * 2;
        turtle.style.transform = `translate3d(${snapped}px, 0, 0)`;

        // keep the speech bubble on screen: point it left on the right half
        if (dialogue) {
            dialogue.classList.toggle("is-flipped", x > (minX + maxX) / 2);
        }
    }

    function setWalking(isWalking) {
        if (walking === isWalking) return;
        walking = isWalking;
        turtle.classList.toggle("is-walking", isWalking);
    }

    function step(time) {
        if (!lastTime) lastTime = time;
        const dt = Math.min(time - lastTime, 100) / 1000;
        lastTime = time;

        if (time < pausedUntil) {
            setWalking(false);
        } else {
            setWalking(true);
            x += direction * WALK_SPEED * dt;

            if (x >= maxX || x <= minX) {
                x = Math.min(Math.max(x, minX), maxX);
                direction *= -1;
                pausedUntil = time + PAUSE_AT_EDGE;
                turtle.classList.toggle("is-facing-left", direction < 0);
            }

            placeTurtle();
        }

        requestAnimationFrame(step);
    }

    if (turtle) {
        measureBounds();
        x = minX + (maxX - minX) * 0.18;
        placeTurtle();

        if (!prefersReducedMotion.matches) {
            requestAnimationFrame(step);
        }

        let resizeTimer = null;
        window.addEventListener("resize", () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                measureBounds();
                placeTurtle();
            }, 120);
        });

        // reset the clock after the tab comes back so he doesn't teleport
        document.addEventListener("visibilitychange", () => {
            lastTime = 0;
        });
    }

})();
