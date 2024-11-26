'use server';

import {saveImg} from '../lib/save';

export async function saveImage(formData) {
    const img = {
        image: formData.get('image'),
      };

    console.log(img.image)

    await saveImg(img);}
