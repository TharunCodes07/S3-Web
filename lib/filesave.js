import fs from 'node:fs';

export async function fileSave(pdf) {

  const stream = fs.createWriteStream('public/uploaded_file.pdf');
  const bufferedfile = await pdf.file.arrayBuffer();
  
  stream.write(Buffer.from(bufferedfile), (error) => {
    if (error) {
      throw new Error('Saving file failed!');
    }
  });
}