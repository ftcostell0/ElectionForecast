document.getElementById('changeColorButton').addEventListener('click', function() {
    const colors = ['#f44336', '#2196F3', '#4CAF50', '#FFEB3B', '#673AB7'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.style.backgroundColor = randomColor;
});