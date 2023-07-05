const buttons = document.querySelectorAll('.button');
const descriptions = document.querySelectorAll('.description');

buttons.forEach((button, index) => {
  button.addEventListener('click', () => {
    const description = descriptions[index];
    if (description.style.display === 'none') {
      description.textContent = 'This is a test';
      description.style.display = 'block';
    } else {
      description.style.display = 'none';
    }
  });
});
document.getElementById('Redo').addEventListener('click', function(e) {
    e.preventDefault(); 
    window.location.href = "MD.html"; 
});