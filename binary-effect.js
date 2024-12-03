// Binary effect setup
const canvas = document.createElement('canvas');
document.body.appendChild(canvas);

const ctx = canvas.getContext('2d');
canvas.id = "binary-canvas";
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Binary characters
const binary = "01";
const binaryArray = binary.split("");

// Columns for falling text
const fontSize = 16;
const columns = canvas.width / fontSize;

// Array to track falling positions
const drops = Array(Math.floor(columns)).fill(0);

function drawBinary() {
  // Set background for left and right areas
  ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Set text style
  ctx.fillStyle = "#0F0"; // Green
  ctx.font = `${fontSize}px monospace`;

  // Draw characters only on left and right edges
  for (let i = 0; i < drops.length; i++) {
    if (i < columns / 4 || i > (3 * columns) / 4) {
      const text = binaryArray[Math.floor(Math.random() * binaryArray.length)];
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);

      // Reset drop position when it reaches the bottom
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }

      // Increment Y-coordinate
      drops[i]++;
    }
  }
}

setInterval(drawBinary, 50);

// Handle window resize
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});
