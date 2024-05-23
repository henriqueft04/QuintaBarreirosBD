// Função para abrir o modal
document.querySelector('button[hx-get]').addEventListener('click', function () {
    document.getElementById('newOrderModal').classList.remove('hidden');
});

// Função para fechar o modal
document.getElementById('closeModal').addEventListener('click', function () {
    document.getElementById('newOrderModal').classList.add('hidden');
});

// Aplicar event listeners iniciais
applyEventListeners();

function applyEventListeners() {
    // Listener para adicionar item
    document.getElementById('add-item').addEventListener('click', () => {
        const itemsContainer = document.getElementById('items-container');
        const itemCount = itemsContainer.children.length + 1;
        const newItem = document.createElement('div');
        newItem.className = 'item grid grid-cols-4 space-x-4';

        newItem.innerHTML = `
            <div class="">
                <label for="item-${itemCount}" class="block text-sm font-medium text-gray-700">Item</label>
                <select id="item-${itemCount}" name="items[]" class="mt-1 border border-gray-200 p-1 rounded-lg h-8 block w-full shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
                    <option value="Vinho Tinto">Vinho Tinto</option>
                    <option value="Vinho Branco">Vinho Branco</option>
                    <option value="Vinho Rosé">Vinho Rosé</option>
                    <!-- Adicione outros tipos de vinho aqui -->
                </select>
            </div>
            <div class="">
                <label for="quantity-${itemCount}" class="block text-sm font-medium text-gray-700">Quantidade Caixas <i class="fas fas fa-box-open"></i></label>
                <input type="number" id="quantity-${itemCount}" name="quantities[]" class="mt-1 border border-gray-200 p-1 rounded-lg h-8 block w-full shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
            </div>
            <div class="">
                <label for="quantity-bottles-${itemCount}" class="block text-sm font-medium text-gray-700">Quantidade Garrafas <i class="fas fas fa-wine-bottle"></i></label>
                <input type="number" id="quantity-bottles-${itemCount}" name="quantities[]" class="mt-1 border border-gray-200 p-1 rounded-lg h-8 block w-full shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
            </div>
            <div class="">
                <label for="quantity-jugs-${itemCount}" class="block text-sm font-medium text-gray-700">Quantidade Garrafões <i class="fa-solid fa-jug-detergent"></i></label>
                <input type="number" id="quantity-jugs-${itemCount}" name="quantities[]" class="mt-1 border border-gray-200 p-1 rounded-lg h-8 block w-full shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
            </div>
        `;

        itemsContainer.appendChild(newItem);
    });

    // Listener para remover item
    document.getElementById('remove-item').addEventListener('click', () => {
        const itemsContainer = document.getElementById('items-container');
        if (itemsContainer.children.length > 0) {
            itemsContainer.removeChild(itemsContainer.lastChild);
        }
    });

    // Listener para submissão do formulário
    document.getElementById('new-order-form').addEventListener('submit', (event) => {
        // Verificar se o formulário é válido
        if (!event.target.checkValidity()) {
            // Se não for válido, exibir os avisos padrão do navegador
            event.target.reportValidity();
        } else {
            // Se for válido, prevenir o comportamento padrão e processar o formulário
            event.preventDefault();
            const formData = new FormData(event.target);
            // Processar os dados do formulário conforme necessário (por exemplo, enviar ao servidor ou atualizar a tabela)
        }
    });
}
