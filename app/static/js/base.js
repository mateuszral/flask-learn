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

const toggleModal = (modalId, userId = null, email = null, username = null, role = null, first_name = null, last_name = null, age = null, bio = null, featured = null) => {
    const modal = document.querySelector(`#${modalId}`);

    if (modalId === 'editModal') {
        const form = document.querySelector("#editForm");

        document.querySelector("#username").value = username;
        document.querySelector("#email").value = email;
        document.querySelector("#editRole").value = role;
        document.querySelector("#firstName").value = first_name === "None" ? '' : first_name;
        document.querySelector("#lastName").value = last_name === "None" ? '' : last_name;
        document.querySelector("#age").value = age === "None" ? '' : age;
        document.querySelector("#bio").value = bio === "None" ? '' : bio;
        document.querySelector("#featured").checked = featured === "True";

        form.action = `/admin/edit-user/${userId}`;
    }

    if (modalId === 'deleteModal' && userId) {
        const deleteForm = document.querySelector('#deleteForm');
        const deleteMessage = document.querySelector('#deleteMessage');
        deleteMessage.innerHTML = `Are you sure you want to delete user with email <strong>${email}</strong>? This action cannot be undone.`;
        deleteForm.action = `/admin/delete-user/${userId}`;
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

const closeFlash = (button) => {
    const flash = button.closest(".flash");
    removeFlash(flash);
}

const removeFlash = (flash) => {
    flash.classList.add("fade-out");
    setTimeout(() => flash.remove(), 300);
}