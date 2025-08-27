// Функции для работы с модальными окнами баланса

// Показать окно выбора действия
function showBalanceOptions() {
    document.getElementById('balanceModal').style.display = 'block';
}

// Закрыть все модальные окна
function closeAllModals() {
    document.getElementById('balanceModal').style.display = 'none';
    document.getElementById('addBalanceModal').style.display = 'none';
    document.getElementById('promoCodeModal').style.display = 'none';
}

// Показать форму пополнения счета
function showAddBalanceForm() {
    document.getElementById('balanceModal').style.display = 'none';
    document.getElementById('addBalanceModal').style.display = 'block';
}

// Закрыть форму пополнения счета
function closeAddBalanceModal() {
    document.getElementById('addBalanceModal').style.display = 'none';
    document.getElementById('balanceModal').style.display = 'block';
}

// Показать форму промокода
function showPromoCodeForm() {
    document.getElementById('balanceModal').style.display = 'none';
    document.getElementById('promoCodeModal').style.display = 'block';
}

// Закрыть форму промокода
function closePromoCodeModal() {
    document.getElementById('promoCodeModal').style.display = 'none';
    document.getElementById('balanceModal').style.display = 'block';
}

// Закрытие модальных окон при клике вне их области
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            closeAllModals();
        }
    });
}

// Обработка формы пополнения баланса
document.getElementById('addBalanceForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const amount = document.getElementById('amount').value;
    if (amount > 0) {
        alert(`Баланс успешно пополнен на ${amount} ₽`);
        closeAllModals();
        document.getElementById('addBalanceForm').reset();
    } else {
        alert('Пожалуйста, введите корректную сумму');
    }
});

// Обработка формы промокода
document.getElementById('promoCodeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const promoCode = document.getElementById('promoCode').value;
    if (promoCode.trim() !== '') {
        alert(`Промокод "${promoCode}" активирован!`);
        closeAllModals();
        document.getElementById('promoCodeForm').reset();
    } else {
        alert('Пожалуйста, введите промокод');
    }
});

// Закрытие по ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeAllModals();
    }
});