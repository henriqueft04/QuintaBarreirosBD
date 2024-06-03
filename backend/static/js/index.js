document.addEventListener('DOMContentLoaded', (event) => {
    const closeModalButtons = document.querySelectorAll('.close-modal');
    const openModalButtons = document.querySelectorAll('.open-modal');
    openModalButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            
            const modalTarget = e.currentTarget.getAttribute('data-modal-target') || 'orderModal';
            const modal = document.getElementById(modalTarget);
            if (modal.classList === null || modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
            }
            modal.classList.remove('hidden');
        });
    });

    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal'); // Garante que está fechando o modal correto
            if (modal) {
                modal.classList.add('hidden');
            } else {
                console.error("Modal element not found");
            }
        });
    });
});




