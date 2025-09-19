// import { createCanvas } from "canvas"; // npm install canvas

// export default function handler(req, res) {
//   const width = 600;
//   const height = 600;

//   const canvas = createCanvas(width, height);
//   const ctx = canvas.getContext("2d");

//   // Transparent background
//   ctx.clearRect(0, 0, width, height);

//   // Example Kolam: draw a white circle in center
//   ctx.fillStyle = "white";
//   ctx.beginPath();
//   ctx.arc(width / 2, height / 2, 100, 0, Math.PI * 2);
//   ctx.fill();

//   // Send image as PNG
//   res.setHeader("Content-Type", "image/png");
//   res.send(canvas.toBuffer());
// }


// import { createCanvas } from "canvas";

// export default function handler(req, res) {
//     const width = 600;
//     const height = 600;

//     const canvas = createCanvas(width, height);
//     const ctx = canvas.getContext("2d");

//     // Transparent background
//     ctx.clearRect(0, 0, width, height);

//     // Draw your Kolam here
//     ctx.strokeStyle = "white";
//     ctx.lineWidth = 2;

//     // Example: simple pattern
//     ctx.beginPath();
//     ctx.moveTo(100, 100);
//     ctx.lineTo(500, 100);
//     ctx.lineTo(500, 500);
//     ctx.lineTo(100, 500);
//     ctx.closePath();
//     ctx.stroke();

//     // Send as PNG
//     res.setHeader("Content-Type", "image/png");
//     res.send(canvas.toBuffer());
// }

import { createCanvas } from "canvas";

export default function handler(req, res) {
  const width = 600;
  const height = 600;

  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext("2d");

  // Transparent background
  ctx.clearRect(0, 0, width, height);

  // --- Real Kolam pattern start ---
  ctx.strokeStyle = "white";
  ctx.lineWidth = 2;

  // Example: draw multiple curves/lines
  // Replace this with your exact Kolam coordinates from front-end
  ctx.beginPath();
  ctx.moveTo(300, 100);
  ctx.bezierCurveTo(500, 100, 500, 500, 300, 500);
  ctx.bezierCurveTo(100, 500, 100, 100, 300, 100);
  ctx.stroke();

  // --- Real Kolam pattern end ---

  // Send as PNG
  res.setHeader("Content-Type", "image/png");
  res.send(canvas.toBuffer());
}
