(function () {
    "use strict";

    const beach = document.querySelector(".hero");
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");


    /* 1. GREETING INTERACTION  */

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
        "Ahoj, já jsem Xynex Kim.",
        "Salut, je suis Xynex Kim.",             
    "Moikka, olen Xynex Kim.",               
    "God dag, jeg er Xynex Kim.",            
    "Terve, olen Xynex Kim.",               
    "Shalom, ani Xynex Kim.",                
    "Kia ora, ko Xynex Kim ahau.",          
    "Bula, o au o Xynex Kim.",               
    "Talofa, o aʻu o Xynex Kim.",            
    "Mālō e lelei, ko Xynex Kim au.",       
    "Ia ora na, ʻo Xynex Kim vau.",         
    "नमस्ते, मैं Xynex Kim हूँ।",             
    "নমস্কার, আমি Xynex Kim।",              
    "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਮੈਂ Xynex Kim ਹਾਂ।",       
    "வணக்கம், நான் Xynex Kim.",              
    "నమస్కారం, నేను Xynex Kim.",             
    "ನಮಸ್ಕಾರ, ನಾನು Xynex Kim.",              
    "നമസ്കാരം, ഞാൻ Xynex Kim.",             
    "สวัสดีครับ/ค่ะ ฉันชื่อ Xynex Kim",       
    "សួស្តី ខ្ញុំឈ្មោះ Xynex Kim។",         
    "ສະບາຍດີ, ຂ້ອຍຊື່ Xynex Kim.",       
    "မင်္ဂလာပါ၊ ကျွန်တော်/ကျွန်မ Xynex Kim ပါ။", 
    "Assalamu alaikum, saya Xynex Kim.",    
    "Selamat sejahtera, saya Xynex Kim.",    
    "გამარჯობა, მე Xynex Kim ვარ.",          
    "გამარჯობა, Xynex Kim ვარ.",             
    "Здравейте, аз съм Xynex Kim.",          
    "Zdravo, ja sam Xynex Kim.",            
    "Здраво, јас сум Xynex Kim.",            
    "გამარჯობა, მე მქვია Xynex Kim.",        
    "Բարև, ես Xynex Kim եմ։",                
    "გამარჯობა!",                            
    "Dzień dobry, jestem Xynex Kim.",        
    "Dobro jutro, ja sam Xynex Kim.",        
    "Dobré ráno, jsem Xynex Kim.",           
    "Guten Tag, ich bin Xynex Kim.",        
    "God morgen, jeg heter Xynex Kim.",      
    "Hyvää päivää, olen Xynex Kim.",         
    "Bună ziua, sunt Xynex Kim.",           
    "Konnichiwa, watashi wa Xynex Kim desu.", 
    "Annyeonghaseyo, jeoneun Xynex Kim imnida.", 
    "Ni hao, wo shi Xynex Kim.",             
    "Sawasdee, chan chue Xynex Kim.",        
    "Ahlan, ana Xynex Kim.",                 
    "Habari, mimi ni Xynex Kim.",           
    "Molo, ndingu-Xynex Kim.",               
    "Dumela, ke Xynex Kim.",                 
    "Kumusta, ako si Xynex Kim.",            
    "Maayong adlaw, ako si Xynex Kim.",      
    "Madayaw, ako si Xynex Kim.",           
    "Yá'át'ééh, Xynex Kim yinishyé.",       
    "Hola, em dic Xynex Kim.",               
    "Kaixo, Xynex Kim naiz.",                
    "Cześć, mam na imię Xynex Kim.",         
    "Ahoj, volám sa Xynex Kim.",             
    "Sveiki, es esmu Xynex Kim.",            
    "Tere, mina olen Xynex Kim.",            
    "Labas, aš esu Xynex Kim.",              
    "Привіт, мене звати Xynex Kim.",         
    "Сәлем, мен Xynex Kim.",                 
    "Сайн байна уу, намайг Xynex Kim гэдэг.", 
    "Xin chào! Mình là Xynex Kim.",         
    "Yassas, eimai o Xynex Kim.",           
    "Olá! Meu nome é Xynex Kim.",            
    "E aí, eu sou Xynex Kim.",               
    "Qué tal, soy Xynex Kim.",               
    "Ciao! Mi chiamo Xynex Kim.",            
    "Hey, ik ben Xynex Kim.",                
    "Hej! Jag är Xynex Kim.",                
    "Hei! Jeg er Xynex Kim.",                
    "Moi, olen Xynex Kim.",                 
    "Halló, ég heiti Xynex Kim.",            
    "Dia dhuit, is mise Xynex Kim.",        
    "Bore da, Xynex Kim ydw i.",             
    "Bonjou, mwen se Xynex Kim.",            
    "Hola, yo soy Xynex Kim.",              
    "Salve, ego Xynex Kim sum.",             
    "Привет! Я Xynex Kim.",                
    "Merhaba! Benim adım Xynex Kim.",        
    "नमस्कार, मेरा नाम Xynex Kim है।",        
    "வணக்கம்! என் பெயர் Xynex Kim.",         
    "你好！我叫 Xynex Kim。",                  
    "안녕! 나는 Xynex Kim이야.",              
    "こんにちは！Xynex Kimと申します。",          
    "مرحبا! اسمي Xynex Kim.",               
    "שלום! קוראים לי Xynex Kim.",             
    "Բարև, իմ անունը Xynex Kim է։",         
    "გამარჯობა, ჩემი სახელია Xynex Kim.",    
    "Zdravo! Moje ime je Xynex Kim.",        
    "Здравей! Казвам се Xynex Kim.",         
    "Ahoj! Jmenuji se Xynex Kim.",           
    "Sveiki! Mani sauc Xynex Kim.",          
    "Tere! Minu nimi on Xynex Kim.",         
    "Labas! Mano vardas Xynex Kim.",         
    "Сәлеметсіз бе, менің атым Xynex Kim.", 
    "Сайн уу, би Xynex Kim.",              
    "Kia ora! Ko Xynex Kim tōku ingoa.",    
    "Talofa! O loʻu igoa o Xynex Kim.",     
    "Bula! Na yacaqu o Xynex Kim.",         
    "Habari za asubuhi, mimi ni Xynex Kim.", 
    "Sawubona! Igama lami ngu-Xynex Kim.",   
    "Molo! Igama lam ngu-Xynex Kim.",        
    "Dumela! Leina la me ke Xynex Kim.",     
    "Bonjou! Non mwen se Xynex Kim.",        
    "Maayong buntag! Ako si Xynex Kim.",     
    "Magandang araw! Ako si Xynex Kim.",     
    "नमस्कार! मैं Xynex Kim हूँ।",             
    "வணக்கம்! நான் Xynex Kim.",              
    "ನಮಸ್ಕಾರ! ನಾನು Xynex Kim.",             
    "నమస్కారం! నేను Xynex Kim.",             
    "നമസ്കാരം! ഞാൻ Xynex Kim.",              
    "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ Xynex Kim ਹਾਂ।",       
    "নমস্কার! আমি Xynex Kim।",              
    "សួស្តី! ខ្ញុំគឺ Xynex Kim។",             
    "ສະບາຍດີ! ຂ້ອຍແມ່ນ Xynex Kim.",    
    "မင်္ဂလာပါ! ကျွန်ုပ် Xynex Kim ဖြစ်ပါတယ်။"
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


    /* 2. BEACH TIME THEMES  */
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


    /* 3. PHILIPPINE CLOCK  */

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


    /* 4. TESTUDO'S DIALOGUE  */

    const TESTUDO_LINES = {
        home: "Psst! Click the greeting above to switch up the language!",
        about: "Let's get to know the little missy behind this portfolio!",
        projects: "Ooh! Let's explore some of her projects!",
        skills: "These are the tools and skills she's learning and leveling up!",
        experience: "Look at all the things she's been working on!",
        education: "Come follow along on her learning journey!",
        certificates: "Achievement unlocked! Check out these certificates!",
        achievements: "Look at all the awesome things she's accomplished!",
        contact: "Want to say hello? Feel free to drop her a message anytime!"
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


    /* 5. PORTFOLIO PANEL  */

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


    /* 6. TESTUDO WALKING 
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


    /* 7. BEACH SOUNDS 
       Ambient soundscapes made live with the Web Audio API (no audio files):
         dawn   – soft breeze + waves + a few early birds
         day    – waves + light breeze
         sunset – slower, warmer waves + breeze
         night  – calm waves + crickets
       Browsers only allow sound after a click, so it starts from the 🔈 button.
       The soundscape follows the beach theme automatically. */

    const SOUND_KEY = "beach-sound";

    const SOUNDSCAPES = {
        //        waves  wave tone  breeze  breeze tone  birds  crickets
        dawn:   { waves: .30, waveHz: 520, breeze: .16, breezeHz: 1100, birds: true,  crickets: false },
        day:    { waves: .42, waveHz: 680, breeze: .08, breezeHz: 1400, birds: false, crickets: false },
        sunset: { waves: .36, waveHz: 480, breeze: .12, breezeHz: 900,  birds: false, crickets: false },
        night:  { waves: .26, waveHz: 380, breeze: .04, breezeHz: 700,  birds: false, crickets: true }
    };

    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const navbar = document.querySelector(".navbar");
    const clock = document.querySelector(".nav-clock");

    let audio = null;          // built on first use
    let soundOn = false;
    let chirpTimer = null;

    function readPreference() {
        try { return localStorage.getItem(SOUND_KEY) === "on"; } catch (e) { return false; }
    }

    function savePreference(on) {
        try { localStorage.setItem(SOUND_KEY, on ? "on" : "off"); } catch (e) { /* private mode */ }
    }

    function makeNoise(ctx) {
        // 4 seconds of soft "brown" noise, looped: the raw material for wind and surf
        const length = ctx.sampleRate * 4;
        const buffer = ctx.createBuffer(1, length, ctx.sampleRate);
        const data = buffer.getChannelData(0);
        let last = 0;
        for (let i = 0; i < length; i++) {
            last = (last + 0.02 * (Math.random() * 2 - 1)) / 1.02;
            data[i] = last * 3.5;
        }
        const source = ctx.createBufferSource();
        source.buffer = buffer;
        source.loop = true;
        // start each copy at a random point so wind and surf don't sound in sync
        source.start(0, Math.random() * 4);
        return source;
    }

    function lfo(ctx, rate, depth, target) {
        // slow wobble connected to an AudioParam (gain or frequency)
        const osc = ctx.createOscillator();
        const amount = ctx.createGain();
        osc.frequency.value = rate;
        amount.gain.value = depth;
        osc.connect(amount).connect(target);
        osc.start();
    }

    function buildAudio() {
        const ctx = new AudioCtx();
        const master = ctx.createGain();
        master.gain.value = 0;
        master.connect(ctx.destination);

        // WAVES: low rumble that swells every ~8 s, in time with the CSS swash
        const waveFilter = ctx.createBiquadFilter();
        waveFilter.type = "lowpass";
        waveFilter.frequency.value = 600;
        const waveSwell = ctx.createGain();
        waveSwell.gain.value = 0.6;
        lfo(ctx, 1 / 8, 0.4, waveSwell.gain);
        const waves = ctx.createGain();
        waves.gain.value = 0;
        makeNoise(ctx).connect(waveFilter).connect(waveSwell).connect(waves).connect(master);

        // BREEZE: airy band of noise that drifts in pitch and strength
        const breezeFilter = ctx.createBiquadFilter();
        breezeFilter.type = "bandpass";
        breezeFilter.frequency.value = 1100;
        breezeFilter.Q.value = 0.6;
        lfo(ctx, 0.05, 350, breezeFilter.frequency);
        const breezeGust = ctx.createGain();
        breezeGust.gain.value = 0.7;
        lfo(ctx, 0.07, 0.3, breezeGust.gain);
        const breeze = ctx.createGain();
        breeze.gain.value = 0;
        makeNoise(ctx).connect(breezeFilter).connect(breezeGust).connect(breeze).connect(master);

        // CHIRPS (birds at dawn, crickets at night) are short notes played on a timer
        const chirps = ctx.createGain();
        chirps.gain.value = 0.5;
        chirps.connect(master);

        return { ctx, master, waves, waveFilter, breeze, breezeFilter, chirps };
    }

    function chirp(freqStart, freqEnd, duration, volume, when) {
        const { ctx, chirps } = audio;
        const osc = ctx.createOscillator();
        const env = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freqStart, when);
        osc.frequency.exponentialRampToValueAtTime(freqEnd, when + duration);
        env.gain.setValueAtTime(0, when);
        env.gain.linearRampToValueAtTime(volume, when + 0.01);
        env.gain.exponentialRampToValueAtTime(0.0001, when + duration);
        osc.connect(env).connect(chirps);
        osc.start(when);
        osc.stop(when + duration + 0.05);
    }

    function scheduleChirps() {
        clearTimeout(chirpTimer);
        if (!soundOn || !audio) return;

        const scape = SOUNDSCAPES[beach.dataset.theme] || SOUNDSCAPES.day;
        const now = audio.ctx.currentTime + 0.05;

        if (scape.birds) {
            // a little two- or three-note bird call
            const base = 2400 + Math.random() * 1200;
            const notes = 2 + Math.floor(Math.random() * 2);
            for (let i = 0; i < notes; i++) {
                chirp(base, base * 1.35, 0.09, 0.05, now + i * 0.14);
            }
        }

        if (scape.crickets) {
            // cricket trill: a quick burst of tiny pulses
            for (let i = 0; i < 4; i++) {
                chirp(4600, 4500, 0.035, 0.018, now + i * 0.06);
            }
        }

        const wait = scape.birds ? 2500 + Math.random() * 5000 : 700 + Math.random() * 1400;
        chirpTimer = setTimeout(scheduleChirps, wait);
    }

    function applySoundscape() {
        if (!audio) return;
        const scape = SOUNDSCAPES[beach.dataset.theme] || SOUNDSCAPES.day;
        const t = audio.ctx.currentTime;
        // setTargetAtTime gives a smooth ~3 s crossfade between times of day
        audio.waves.gain.setTargetAtTime(scape.waves, t, 1);
        audio.waveFilter.frequency.setTargetAtTime(scape.waveHz, t, 1);
        audio.breeze.gain.setTargetAtTime(scape.breeze, t, 1);
        audio.breezeFilter.frequency.setTargetAtTime(scape.breezeHz, t, 1);
        scheduleChirps();
    }

    function setSound(on) {
        if (!AudioCtx) return;

        if (on && !audio) {
            audio = buildAudio();
        }

        soundOn = on;
        savePreference(on);
        soundButton.setAttribute("aria-pressed", on ? "true" : "false");
        soundButton.setAttribute("aria-label", on ? "Turn beach sounds off" : "Turn beach sounds on");
        soundButton.title = on ? "Sound on" : "Sound off";

        if (!audio) return;

        const t = audio.ctx.currentTime;
        if (on) {
            audio.ctx.resume();
            audio.master.gain.cancelScheduledValues(t);
            audio.master.gain.setTargetAtTime(0.9, t, 0.6);   // fade in
            applySoundscape();
        } else {
            audio.master.gain.cancelScheduledValues(t);
            audio.master.gain.setTargetAtTime(0, t, 0.3);     // fade out
            clearTimeout(chirpTimer);
            setTimeout(() => { if (!soundOn) audio.ctx.suspend(); }, 1500);
        }
    }

    // the toggle button lives in the navbar, just before the clock
    const soundButton = document.createElement("button");
    soundButton.type = "button";
    soundButton.className = "nav-sound";
    soundButton.setAttribute("aria-pressed", "false");
    soundButton.setAttribute("aria-label", "Turn beach sounds on");
    soundButton.title = "Sound off";
    soundButton.innerHTML =
        '<svg class="sound-icon" viewBox="0 0 24 24" aria-hidden="true">' +
            '<path d="M4 9h4l5-4v14l-5-4H4z"/>' +
            '<path class="sound-waves" d="M16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/>' +
            '<path class="sound-mute" d="m16 9 6 6m0-6-6 6"/>' +
        '</svg>';

    if (AudioCtx && navbar) {
        navbar.insertBefore(soundButton, clock || null);

        soundButton.addEventListener("click", () => setSound(!soundOn));

        // follow the time-of-day theme
        new MutationObserver(applySoundscape).observe(beach, {
            attributes: true,
            attributeFilter: ["data-theme"]
        });

        // stay quiet while the tab is in the background
        document.addEventListener("visibilitychange", () => {
            if (!audio || !soundOn) return;
            if (document.hidden) {
                audio.ctx.suspend();
                clearTimeout(chirpTimer);
            } else {
                audio.ctx.resume();
                scheduleChirps();
            }
        });

        // if they turned sound on during an earlier visit, start it on their first tap
        if (readPreference()) {
            soundButton.classList.add("is-waiting");
            const resumeOnce = (event) => {
                if (event.target.closest(".nav-sound")) return; // the button handles itself
                soundButton.classList.remove("is-waiting");
                setSound(true);
            };
            document.addEventListener("pointerdown", resumeOnce, { once: true, capture: true });
        }
    }


})();
