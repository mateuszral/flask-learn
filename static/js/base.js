const togglePassword = (id, el) => {
    const input = document.querySelector(`#${id}`);

    if (input.type === 'password') {
        input.type = 'text';
        el.textContent = 'Hide';
    } else {
        input.type = 'password';
        el.textContent = 'Show';
    }
}

const toggleModal =(modalId) => {
    const modal = document.querySelector(`#${modalId}`);
    modal.classList.toggle('visible');
}

const closeAfterClick = document.querySelector('#deleteModal');
if (closeAfterClick) {
    closeAfterClick.addEventListener('click', (e) => {
        if (e.target === closeAfterClick) {
             closeAfterClick.classList.remove('visible');
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash");

    flashes.forEach((flash) => {
        let duration = parseInt(flash.dataset.time || 5000);
        let remaining = duration;
        let startTime;
        let timeout;

        const progress = flash.querySelector(".flash-progress");
        progress.style.animationDuration = duration + "ms";

        const startTimer = () => {
            startTime = Date.now();
            timeout = setTimeout(() => removeFlash(flash), remaining);
        }

        const pauseTimer = () => {
            clearTimeout(timeout);
            remaining -= Date.now() - startTime;
        }

        flash.addEventListener("mouseenter", pauseTimer);
        flash.addEventListener("mouseleave", startTimer);

        startTimer();
    });
});

closeFlash = (button) => {
    const flash = button.closest(".flash");
    removeFlash(flash);
}

removeFlash = (flash) => {
    flash.classList.add("fade-out");
    setTimeout(() => flash.remove(), 300);
}