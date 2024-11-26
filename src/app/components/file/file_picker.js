'use client';

import { useRef, useState } from 'react';
import classes from './file_picker.module.css';

export default function FilePicker({ label, name, onFileSelect }) {
  const [pickedFile, setPickedFile] = useState(null);
  const fileInput = useRef();

  function handlePickClick() {
    fileInput.current.click();
  }

  function handleFileChange(event) {
    const file = event.target.files[0];

    if (!file) return;

    // Check if it's a PDF
    if (file.type === 'application/pdf') {
      setPickedFile(file);
      onFileSelect(file);  // Pass the selected file to the parent component
    } else {
      alert("Please upload a PDF file.");
    }
  }

  return (
    <div className={classes.picker}>
      <label htmlFor={name}>{label}</label>
      <div className={classes.controls}>
        <div className={classes.preview}>
          {!pickedFile && <p>No file picked yet.</p>}
          {pickedFile && (
            <p>
              Selected File: <a href={URL.createObjectURL(pickedFile)} target="_blank" rel="noopener noreferrer">{pickedFile.name}</a>
            </p>
          )}
        </div>
        <input
          className={classes.input}
          type="file"
          id={name}
          accept="application/pdf"
          name={name}
          ref={fileInput}
          onChange={handleFileChange}
        />
        <button
          className={classes.button}
          type="button"
          onClick={handlePickClick}
        >
          Pick a PDF File
        </button>
      </div>
    </div>
  );
}