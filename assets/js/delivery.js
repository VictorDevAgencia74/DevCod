let cart = [];

function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartFloat = document.querySelector('.cart-float');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');

    if (!cartCount || !cartFloat || !cartItems || !cartTotal) return;

    // Soma total de itens (quantidade)
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.innerText = totalItems;
    
    if (cart.length > 0) {
        cartFloat.style.display = 'block';
        
        let html = '<ul class="list-group list-group-flush bg-transparent">';
        let total = 0;
        
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            html += `
                <li class="list-group-item bg-transparent text-light border-secondary px-0">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="fw-bold">${item.name}</span>
                        <span class="text-success">R$ ${itemTotal.toFixed(2)}</span>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-secondary text-light" onclick="changeQuantity(${index}, -1)">
                                <i class="fas fa-minus"></i>
                            </button>
                            <span class="btn btn-outline-secondary text-light disabled" style="width: 40px; border-color: #6c757d;">
                                ${item.quantity}
                            </span>
                            <button class="btn btn-outline-secondary text-light" onclick="changeQuantity(${index}, 1)">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                        <button class="btn btn-sm btn-outline-danger border-0" onclick="removeFromCart(${index})" title="Remover item">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </li>
            `;
        });
        html += '</ul>';
        
        cartItems.innerHTML = html;
        cartTotal.innerText = `R$ ${total.toFixed(2)}`;
    } else {
        cartFloat.style.display = 'none';
        cartItems.innerHTML = '<p class="text-muted text-center py-4"><i class="fas fa-shopping-basket fa-3x mb-3 d-block opacity-50"></i>Seu carrinho está vazio.</p>';
        cartTotal.innerText = 'R$ 0.00';
    }
}

function addToCart(id, name, price) {
    // Procura se o item já existe no carrinho
    const existingItem = cart.find(item => item.id === id);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ 
            id: id, 
            name: name, 
            price: parseFloat(price), 
            quantity: 1 
        });
    }
    
    updateCartUI();
    
    // Feedback visual opcional (toast ou animação)
    // alert(`${name} adicionado ao carrinho!`);
}

// Função para alterar quantidade (+ ou -)
window.changeQuantity = function(index, change) {
    if (cart[index]) {
        cart[index].quantity += change;
        
        // Se quantidade for 0 ou menor, remove o item
        if (cart[index].quantity <= 0) {
            cart.splice(index, 1);
        }
        
        updateCartUI();
    }
}

// Remove o item completamente
window.removeFromCart = function(index) {
    cart.splice(index, 1);
    updateCartUI();
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-add').forEach(btn => {
        btn.addEventListener('click', function() {
            const { id, name, price } = this.dataset;
            addToCart(id, name, price);
        });
    });

    const btnCheckout = document.getElementById('btnCheckout');
    if (btnCheckout) {
        btnCheckout.addEventListener('click', function() {
            if (cart.length === 0) return;

            let message = "*Olá! Gostaria de fazer um pedido:*\n\n";
            let total = 0;

            cart.forEach(item => {
                const itemTotal = item.price * item.quantity;
                message += `${item.quantity}x ${item.name} ... R$ ${itemTotal.toFixed(2)}\n`;
                total += itemTotal;
            });

            message += `\n*Total Geral: R$ ${total.toFixed(2)}*`;
            message += `\n\n_Pedido gerado via Cardápio Digital Fuosteck_`;
            
            // Número fictício para demo
            const phone = "5511999999999"; 
            const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
            
            window.open(url, '_blank');
        });
    }

    // Lógica do Modal de Detalhes
    const detailsModalEl = document.getElementById('detailsModal');
    if (detailsModalEl) {
        const detailsModal = new bootstrap.Modal(detailsModalEl);
        let currentDetailItem = null;

        document.querySelectorAll('.btn-details').forEach(btn => {
            btn.addEventListener('click', function() {
                const { id, name, price, desc, img } = this.dataset;
                currentDetailItem = { id, name, price };
                
                document.getElementById('detailTitle').innerText = name;
                document.getElementById('detailName').innerText = name;
                document.getElementById('detailPrice').innerText = `R$ ${parseFloat(price).toFixed(2)}`;
                document.getElementById('detailDesc').innerText = desc;
                document.getElementById('detailImage').src = img;
                
                detailsModal.show();
            });
        });

        const btnDetailAdd = document.getElementById('btnDetailAdd');
        if (btnDetailAdd) {
            btnDetailAdd.addEventListener('click', function() {
                if(currentDetailItem) {
                    addToCart(currentDetailItem.id, currentDetailItem.name, currentDetailItem.price);
                    detailsModal.hide();
                }
            });
        }
    }
});
