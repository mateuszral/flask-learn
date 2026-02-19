const closeFlash = () => {
    const flash = document.querySelector('.flash');
    flash.classList.remove('visible');
    setTimeout(() => {
        flash.style.display = 'none';
    }, 300)
}