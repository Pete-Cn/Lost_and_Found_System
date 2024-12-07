document.getElementById('submit').addEventListener('click', function () {
    setTimeout(() => {
        this.disabled = true;
    }, 5);
});