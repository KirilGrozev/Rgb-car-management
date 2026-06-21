function toggleOtherFields() {
    const otherCheckbox = document.querySelector('input[value="other"].issue-checkbox');
    const otherContainer = document.getElementById('other-container');
    const otherDescription = document.getElementById('other-description');

    if (otherCheckbox && otherCheckbox.checked) {
        otherContainer.style.display = 'block';
        otherDescription.style.display = 'block';
    } else {
        otherContainer.style.display = 'none';
        otherDescription.style.display = 'none';
        otherDescription.value = '';
    }
}