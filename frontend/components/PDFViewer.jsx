function PDFViewer({ pdfUrl, filename }) {
  if (!pdfUrl) {
    return (
      <div className="pdf-placeholder">
        <h3>Visor de tesis</h3>
        <p>
          Cuando subas un PDF, aqui podras leerlo mientras conversas con el asesor de IA.
        </p>
      </div>
    );
  }

  return (
    <div className="pdf-viewer">
      <div className="pdf-header">Documento activo: {filename || "tesis.pdf"}</div>
      <iframe
        className="pdf-frame"
        src={pdfUrl}
        title="Vista previa de tesis"
      />
    </div>
  );
}

export default PDFViewer;
