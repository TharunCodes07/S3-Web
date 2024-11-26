'use server';

import {fileSave} from '../lib/filesave';

export async function saveFile(formData) {
    const pdf = {
        file: formData.get('file'),
      };

    console.log(pdf.file)

    await fileSave(pdf);}