import { createCanvas, loadImage } from 'canvas';

type ColorResolvable = string | number;

export async function getDominantColour(imageUrl: string): Promise<any> {
  const img = await loadImage(imageUrl);
  const canvas = createCanvas(img.width, img.height);
  const ctx = canvas.getContext('2d');

  ctx.drawImage(img, 0, 0);
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

  const colorCount: Record<string, number> = {};
  let dominantColor = '';
  let maxCount = 0;

  for (let i = 0; i < imageData.length; i += 4) {
    const r = imageData[i];
    const g = imageData[i + 1];
    const b = imageData[i + 2];
    const hex = `#${((1 << 24) | (r << 16) | (g << 8) | b).toString(16).slice(1)}`;

    colorCount[hex] = (colorCount[hex] || 0) + 1;

    if (colorCount[hex] > maxCount) {
      maxCount = colorCount[hex];
      dominantColor = hex;
    }
  }

  // Convert to a number for ColorResolvable
  const colorNumber = parseInt(dominantColor.slice(1), 16);
  return colorNumber;
}

