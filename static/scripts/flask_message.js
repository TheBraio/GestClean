function removeToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        toast.classList.add('hiding');
        setTimeout(() => {
            if (toast.parentElement) {
                toast.parentElement.removeChild(toast);
            }
        }, 300);
    }
}

// Auto-remove toasts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const toasts = document.querySelectorAll('.toast');
    const btn_close = document.querySelectorAll('.toast-close')
    toasts.forEach((toast, index) => {
        setTimeout(() => {
            removeToast(toast.id);
        }, 5000);
    });

    btn_close.forEach((btn) => {
        btn.addEventListener('click', function() {
            const toastId = btn.parentElement.id;
            removeToast(toastId);
        })
    })
});