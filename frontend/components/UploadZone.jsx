"use client";

import { useRef, useState } from "react";

function UploadZone({ onUpload, isUploading }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState("");

  const validateFile = (file) => {
    if (!file) {
      return "No se selecciono ningun archivo.";
    }

    const isPdfMime = file.type === "application/pdf";
    const hasPdfExtension = file.name.toLowerCase().endsWith(".pdf");

    if (!isPdfMime && !hasPdfExtension) {
      return "Solo se aceptan archivos PDF.";
    }

    return "";
  };

  const handleSelectedFile = async (file) => {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError("");
    await onUpload(file);
  };

  const onDrop = async (event) => {
    event.preventDefault();
    setIsDragging(false);

    if (isUploading) {
      return;
    }

    const file = event.dataTransfer.files?.[0];
    await handleSelectedFile(file);
  };

  const onInputChange = async (event) => {
    if (isUploading) {
      return;
    }

    const file = event.target.files?.[0];
    await handleSelectedFile(file);
    event.target.value = "";
  };

  return (
    <div className="upload-wrapper">
      <div
        className={`upload-zone ${isDragging ? "is-active" : ""}`}
        onDragOver={(event) => {
          event.preventDefault();
          if (!isUploading) {
            setIsDragging(true);
          }
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
      >
        <p className="upload-title">Sube tu tesis en PDF</p>
        <p className="upload-subtitle">
          Arrastra el archivo aqui o usa el boton para seleccionarlo.
        </p>
        <button
          type="button"
          className="button button-secondary"
          onClick={() => inputRef.current?.click()}
          disabled={isUploading}
        >
          {isUploading ? "Procesando PDF..." : "Seleccionar PDF"}
        </button>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          className="visually-hidden"
          onChange={onInputChange}
        />
      </div>
      {error ? <p className="inline-error">{error}</p> : null}
    </div>
  );
}

export default UploadZone;
