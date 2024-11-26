import fs from 'node:fs';

export async function saveImg(img) {

    const stream = fs.createWriteStream(`public/image.png`);
    const bufferedImage = await img.image.arrayBuffer();
  
    stream.write(Buffer.from(bufferedImage), (error) => {
      if (error) {
        throw new Error('Saving image failed!');
      }
    })}