import { createCanvas } from "canvas";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const size = parseInt(searchParams.get("size") || "500");

  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext("2d");

  // ✅ Do NOT draw a background → transparent
  ctx.clearRect(0, 0, size, size);

  // Draw kolam in white
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 3;

  for (let x = 50; x < size; x += 100) {
    for (let y = 50; y < size; y += 100) {
      ctx.beginPath();
      ctx.arc(x, y, 20, 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  const buffer = canvas.toBuffer("image/png");

  return new Response(buffer, {
    headers: {
      "Content-Type": "image/png",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
