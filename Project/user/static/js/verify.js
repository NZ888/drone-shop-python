document.addEventListener('DOMContentLoaded', () => {
    const inputs = Array.from(document.querySelectorAll('.code-inputs input'));
    const form = document.getElementById('verify-form');

    inputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            input.value = input.value.replace(/\D/g, '').slice(0, 1);
            if (input.value && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (event) => {
            if (event.key === 'Backspace' && !input.value && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });

    form?.addEventListener('submit', () => {
        const firstEmpty = inputs.find((input) => !input.value);
        if (firstEmpty) {
            firstEmpty.focus();
        }
    });
});