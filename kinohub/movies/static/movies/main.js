
// password vision toggle
const passwordInputs = document.querySelectorAll('#password');
const eyeButtons = document.querySelectorAll('#toggle-password');


const eyeOpen = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M5.914 7.591c-1.572 1.45-2.625 3.15-3.143 4.106a.624.624 0 0 0 0 .606c.518.955 1.57 2.656 3.143 4.106C7.482 17.855 9.506 19 12 19s4.518-1.145 6.085-2.591c1.573-1.45 2.626-3.15 3.145-4.106a.624.624 0 0 0 0-.606c-.519-.955-1.572-2.656-3.145-4.106C16.518 6.145 14.495 5 12 5 9.506 5 7.482 6.146 5.914 7.591ZM4.56 6.121C6.36 4.459 8.846 3 12 3s5.64 1.459 7.441 3.12c1.797 1.658 2.974 3.568 3.547 4.624a2.624 2.624 0 0 1 0 2.512c-.573 1.056-1.75 2.966-3.547 4.623C17.64 19.541 15.154 21 12 21s-5.64-1.459-7.441-3.12c-1.797-1.658-2.974-3.568-3.547-4.624a2.624 2.624 0 0 1 0-2.512c.573-1.056 1.75-2.966 3.547-4.623ZM12 9.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5ZM7.5 12a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0Z" clip-rule="evenodd"></path></svg>`;
const eyeClosed = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M2.293 2.293a1 1 0 0 1 1.414 0l18 18a1 1 0 0 1-1.414 1.414l-2.514-2.514C16.204 20.24 14.274 21 12 21c-3.154 0-5.64-1.459-7.441-3.12-1.797-1.658-2.974-3.568-3.547-4.624a2.625 2.625 0 0 1 0-2.513c.578-1.065 1.78-3.017 3.624-4.693L2.293 3.707a1 1 0 0 1 0-1.414Zm3.759 5.173c-1.645 1.473-2.745 3.241-3.281 4.23a.625.625 0 0 0 0 .607c.518.955 1.57 2.656 3.143 4.106C7.482 17.855 9.506 19 12 19c1.65 0 3.09-.5 4.33-1.256l-1.934-1.934A4.502 4.502 0 0 1 8.19 9.604L6.052 7.466Zm3.62 3.62 3.242 3.242a2.5 2.5 0 0 1-3.242-3.242Z" clip-rule="evenodd"/><path fill="currentColor" d="M10.223 5.2c.56-.128 1.152-.2 1.777-.2 2.494 0 4.518 1.146 6.086 2.591 1.572 1.45 2.625 3.15 3.144 4.106a.627.627 0 0 1-.002.608 17.316 17.316 0 0 1-1.344 2.095 1 1 0 0 0 1.6 1.2 19.327 19.327 0 0 0 1.503-2.342 2.627 2.627 0 0 0 0-2.514c-.572-1.056-1.749-2.966-3.546-4.623C17.64 4.459 15.154 3 12 3c-.779 0-1.52.09-2.223.25a1 1 0 0 0 .446 1.95Z"/></svg>`;

// select all toggle buttons


eyeButtons.forEach(button => {
    button.addEventListener('click', () => {
        // find the input in the same input group
        const input = button.closest('.input-group').querySelector('input');

        // toggle type
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';

        // toggle icon (replace with your SVGs)
        if (isPassword) {
            button.innerHTML = eyeClosed; // your "eye closed" SVG
        } else {
            button.innerHTML = eyeOpen;   // your "eye open" SVG
        }
    });
});
