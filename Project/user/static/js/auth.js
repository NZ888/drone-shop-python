+35
-0

document.addEventListener('DOMContentLoaded', () => {
    const backdrop = document.getElementById('auth-backdrop');
    const tabs = document.querySelectorAll('.tab');
    const forms = document.querySelectorAll('.form');
    const message = document.getElementById('form-message');

    const toggleForm = (targetId) => {
        forms.forEach((form) => form.classList.remove('active'));
        tabs.forEach((tab) => tab.classList.remove('active'));
        document.getElementById(targetId).classList.add('active');
        document.querySelector(`.tab[data-target="${targetId}"]`).classList.add('active');
        message.textContent = '';
        message.className = 'message';
    };

    const defaultTab = (backdrop?.dataset.defaultTab || 'register') + '-form';
    toggleForm(defaultTab);

    tabs.forEach((tab) => {
        tab.addEventListener('click', () => toggleForm(tab.dataset.target));
    });

    document.querySelectorAll('[data-action="cancel"]').forEach((button) => {
        button.addEventListener('click', () => {
            backdrop.style.display = 'none';
            window.location.href = '/';
        });
    });

    document.getElementById('modal-close')?.addEventListener('click', () => {
        backdrop.style.display = 'none';
        window.location.href = '/';
    });

  });