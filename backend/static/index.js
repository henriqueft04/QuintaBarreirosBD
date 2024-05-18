document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById('orderModal');
    const closeModal = document.getElementById('closeModal');
    const openModalButtons = document.querySelectorAll('.open-modal');

    openModalButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const orderId = e.currentTarget.getAttribute('data-order-id');
            // Aqui você pode fazer uma chamada AJAX para buscar os detalhes da encomenda
            // e atualizar o conteúdo do modal antes de exibi-lo.

            // Exemplo de atualização de conteúdo:
            const modalContent = modal.querySelector('p');
            modalContent.textContent = `Detalhes da encomenda ${orderId}`;

            modal.classList.remove('hidden');
        });
    });

    closeModal.addEventListener('click', () => {
        modal.classList.add('hidden');
    });
});
