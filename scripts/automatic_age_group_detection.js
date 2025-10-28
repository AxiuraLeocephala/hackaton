const ageInput = document.getElementById('athlete-age');
const groupSelect = document.getElementById('athlete-group');

ageInput.addEventListener('input', () => {
    const age = parseInt(ageInput.value, 10);
    let value = '';

    if (age >= 12 && age <= 13) value = '12-13';
    else if (age >= 14 && age <= 15) value = '14-15';
    else if (age >= 16 && age <= 17) value = '16-17';
    else if (age >= 18 && age <= 20) value = '18-20';
    else if (age >= 21 && age <= 23) value = '21-23';
    else if (age >= 24 && age <= 39) value = '24-39';
    else if (age >= 40 && age <= 49) value = '40-49';
    else if (age >= 50 && age <= 59) value = '50-59';
    else if (age >= 60 && age <= 69) value = '60-69';
    else if (age >= 70 && age <= 79) value = '70-79';
    else if (age >= 80) value = '80+';

    groupSelect.value = value;
});
