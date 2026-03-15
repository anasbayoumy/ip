const display = document.getElementById('display');
const numButtons = document.querySelectorAll('.num');
const opButtons = document.querySelectorAll('.op');
const equalsBtn = document.querySelector('.equals');
const clearBtn = document.querySelector('.clear');

let currentValue = '0';
let previousValue = '';
let operator = null;
let shouldResetDisplay = false;

function updateDisplay(value) {
    display.value = value;
}

function appendNumber(num) {
    if (shouldResetDisplay) {
        currentValue = num;
        shouldResetDisplay = false;
    } else {
        if (num === '.' && currentValue.includes('.')) return;
        if (currentValue === '0' && num !== '.') currentValue = '';
        currentValue += num;
    }
    updateDisplay(currentValue);
}

function setOperator(op) {
    if (operator !== null && !shouldResetDisplay) {
        calculate();
    }
    previousValue = currentValue;
    operator = op;
    shouldResetDisplay = true;
}

function calculate() {
    const prev = parseFloat(previousValue);
    const curr = parseFloat(currentValue);
    
    if (isNaN(prev) || isNaN(curr)) return;
    
    let result;
    switch (operator) {
        case '+': result = prev + curr; break;
        case '-': result = prev - curr; break;
        case '*': result = prev * curr; break;
        case '/': result = curr === 0 ? 'Error!' : prev / curr; break;
        default: return;
    }
    
    currentValue = String(result);
    previousValue = '';
    operator = null;
    shouldResetDisplay = true;
    updateDisplay(currentValue);
}

function clear() {
    currentValue = '0';
    previousValue = '';
    operator = null;
    shouldResetDisplay = false;
    updateDisplay(currentValue);
}

numButtons.forEach(btn => {
    btn.addEventListener('click', () => appendNumber(btn.dataset.value));
});

opButtons.forEach(btn => {
    btn.addEventListener('click', () => setOperator(btn.dataset.value));
});

equalsBtn.addEventListener('click', calculate);
clearBtn.addEventListener('click', clear);
