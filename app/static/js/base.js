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

const toggleModal =(modalId, userId = null, email = null, username = null, role = null, first_name = null, last_name = null, age = null, bio = null, featured = null) => {
    const modal = document.querySelector(`#${modalId}`);

    if (modalId === 'editModal') {
        const form = document.getElementById("editForm");

        document.getElementById("username").value = username;
        document.getElementById("email").value = email;
        document.getElementById("role").value = role;
        document.getElementById("firstName").value = first_name;
        document.getElementById("lastName").value = last_name;
        document.getElementById("age").value = age;
        document.getElementById("bio").value = bio;
        document.getElementById("featured").checked = featured === "True";

        form.action = `/edit-account/${userId}`;
    }

    if (modalId === 'deleteModal' && userId) {
        const deleteForm = document.getElementById('deleteForm');
        const deleteMessage = document.getElementById('deleteMessage');
        deleteMessage.innerHTML = `Are you sure you want to delete user with email <strong>${email}</strong>? This action cannot be undone.`;
        deleteForm.action = `/delete-account/${userId}`;
    }

    modal.classList.toggle('visible');
}

const closeAfterClick = document.querySelectorAll('.modal-overlay');
if (closeAfterClick) {
    closeAfterClick.forEach((overlay) => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('visible');
            }
        });
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