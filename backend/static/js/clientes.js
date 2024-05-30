 document.addEventListener('DOMContentLoaded', function() {
        var modals = document.querySelectorAll('.open-modal');
        modals.forEach(function(button) {
            button.addEventListener('htmx:afterSwap', function() {
                var modal = document.querySelector(button.getAttribute('hx-target'));
                modal.classList.remove('hidden');
            });
        });


            function openModal() {
            document.getElementById("form-modal").classList.remove("hidden");
        }
        
        function closeModal() {
            document.getElementById("form-modal").classList.add("hidden");
        }
        
        function resetForm() {
            document.querySelector("#form-modal form").reset();
        }
        
        function attachModalListeners() {
            document.querySelectorAll('.open-modal').forEach(button => {
                button.addEventListener('click', function() {
                    var orderId = this.getAttribute('data-order-id');
                    console.log("Order ID: " + orderId); // Exibe o ID da encomenda no console
                    
                    // Obter o modal
                    var modalId = this.getAttribute('data-modal-target');
                    var modal = document.getElementById(modalId);
                    
                    if (modal) {
                        modal.classList.remove('hidden');
                    } else {
                        console.error('Modal not found: ' + modalId);
                    }
                });
            });
        }

        attachModalListeners();


        function setClientFilter(type, value) {
            let filters = new URLSearchParams(window.location.search);
            filters.set(type.toLowerCase(), value);

            let url = '/clientes?' + filters.toString();
            let paginationUrl = '/clientes/paginacao?' + filters.toString();
            console.log(url);
            console.log(paginationUrl);

            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('tabela-clientes-container').innerHTML = html;
                attachModalListeners();
            })
            .catch(error => console.error('Error:', error));

            fetch(paginationUrl, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('pagination-container').innerHTML = html;
            })
            .catch(error => console.error('Error:', error));

            let urltotal = '/clientes/total?' + filters.toString();
            fetch(urltotal, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(text => {
                document.getElementById('total-clientes').innerText = text + ' Clientes';
            })
            .catch(error => console.error('Error:', error));
            
        }

        window.setClientFilter = setClientFilter;

        // Adicionar listeners ao input de busca
        document.getElementById('search').addEventListener('keyup', function(event) {
            let searchParam = event.target.value;
            setClientFilter('search_param', searchParam);
        });
});
