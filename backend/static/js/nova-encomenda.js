
document.getElementById('add-item').addEventListener('click', () => {
    const itemsContainer = document.getElementById('items-container');
    const itemCount = itemsContainer.children.length + 1;
    const newItem = document.createElement('div');
    newItem.className = 'item grid grid-cols-4 space-x-4';

    newItem.innerHTML = `
            <div class="">
                <label for="item-1" class="block text-sm font-medium text-gray-700">Item</label>
                <select id="item-1" name="items[]"   class="mt-1 border border-gray-200 p-1 rounded-lg  h-8 block w-full h  shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
                    <option value="Vinho Tinto">Vinho Tinto</option>
                    <option value="Vinho Branco">Vinho Branco</option>
                    <option value="Vinho Rosé">Vinho Rosé</option>
                    <!-- Adicione outros tipos de vinho aqui -->
                </select>
            </div>
            <div class="">
                <label for="quantity-1" class="block text-sm font-medium text-gray-700">Quantidade Caixas <i class="fas fas fa-box-open"></i></label>
                <input type="number" id="quantity-1" name="quantities[]"  class="mt-1 border border-gray-200 p-1 rounded-lg  h-8 block w-full h  shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
            </div>
            <div class="">
                <label for="quantity-2" class="block text-sm font-medium text-gray-700">Quantidade Garrafas <i class="fas fas fa-wine-bottle"></i></label>
                <input type="number" id="quantity-2" name="quantities[]"  class="mt-1 border border-gray-200 p-1 rounded-lg  h-8 block w-full h  shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
            </div>
            <div class="">
                <label for="quantity-3" class="block text-sm font-medium text-gray-700">Quantidade Garrafões <i class="fa-solid fa-jug-detergent"></i></label>
                <input type="number" id="quantity-2" name="quantities[]"  class="mt-1 border border-gray-200 p-1 rounded-lg  h-8 block w-full h  shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required>
            </div>
    `;

    itemsContainer.appendChild(newItem);
});

document.getElementById('new-order-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    // Process the form data as needed (e.g., send to server or update the table)
});
document.getElementById('remove-item').addEventListener('click', () => {
    const itemsContainer = document.getElementById('items-container');
    if (itemsContainer.children.length > 0) {
        itemsContainer.removeChild(itemsContainer.lastChild);
    }
});

document.getElementById('new-order-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    // Process the form data as needed (e.g., send to server or update the table)
});

