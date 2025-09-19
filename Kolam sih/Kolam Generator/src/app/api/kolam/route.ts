import { NextResponse } from "next/server";
import { createCanvas } from "canvas";

export async function GET() {
  // Create canvas with transparent background
  const size = 512;
  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext("2d");

  // Clear with transparency
  ctx.clearRect(0, 0, size, size);

  // Draw white kolam
  ctx.strokeStyle = "white";  // Kolam line color
  ctx.lineWidth = 3;

  ctx.beginPath();
  ctx.arc(size / 2, size / 2, 200, 0, 2 * Math.PI); // simple circle kolam
  ctx.stroke();

  // Export as transparent PNG
  const buffer = canvas.toBuffer("image/png");
  return new NextResponse(buffer, {
    headers: {
      "Content-Type": "image/png",
      "Content-Disposition": "inline; filename=kolam.png",
    },
  });
}
