// 1. GREETING INTERACTION

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

if (greetingElement) {

    greetingElement.addEventListener("click", function () {

        const currentGreeting = greetingElement.textContent.trim();

        let newGreeting;

        do {
            newGreeting =
                greetings[Math.floor(Math.random() * greetings.length)];
        } while (newGreeting === currentGreeting);

        greetingElement.classList.add("fade-out");

        setTimeout(() => {
            greetingElement.textContent = newGreeting;
            greetingElement.classList.remove("fade-out");
        }, 300);

    });
}


// BEACH TIME THEMES

const beach = document.querySelector(".hero");

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

    beach.dataset.theme = theme;
}

updateBeachTheme();

// Check again every minute
setInterval(updateBeachTheme, 60000);