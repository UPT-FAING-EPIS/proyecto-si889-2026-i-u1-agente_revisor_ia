"use client";

import { useEffect, useState } from "react";

import { evaluateThesis } from "../lib/api";

function ThesisReviewPanel({ token, documentId, documentName }) {
  const [review, setReview] = useState("");
  const [stats, setStats] = useState(null);
  const [isReviewing, setIsReviewing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setReview("");
    setStats(null);
    setError("");
  }, [documentId]);

  const onReview = async () => {
    if (!token || !documentId) {
      return;
    }

    setIsReviewing(true);
    setError("");

    try {
      const response = await evaluateThesis(token, documentId);
      setReview(response?.review || "No se obtuvo una evaluacion para esta tesis.");
      setStats({
        totalChunks: response?.total_chunks || 0,
        analyzedChunks: response?.analyzed_chunks || 0,
        analyzedCharacters: response?.analyzed_characters || 0,
      });
    } catch (requestError) {
      if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudo evaluar la tesis en este momento.");
      }
    } finally {
      setIsReviewing(false);
    }
  };

  return (
    <div className="review-panel">
      <div className="review-header">
        <h3>Evaluador IA de tesis</h3>
        <p>
          {documentName
            ? `Documento seleccionado: ${documentName}`
            : "Selecciona una tesis para generar su evaluacion integral."}
        </p>
      </div>

      <div className="review-actions">
        <button
          type="button"
          className="button button-primary"
          disabled={!token || !documentId || isReviewing}
          onClick={onReview}
        >
          {isReviewing ? "Analizando tesis completa..." : "Evaluar tesis"}
        </button>
      </div>

      {!review && !isReviewing ? (
        <div className="review-placeholder">
          <p>
            La IA revisara el contenido procesado del PDF y te devolvera un veredicto con
            fortalezas, brechas y mejoras recomendadas.
          </p>
        </div>
      ) : null}

      {stats ? (
        <div className="review-stats">
          <span>Fragmentos: {stats.analyzedChunks}/{stats.totalChunks}</span>
          <span>Caracteres analizados: {stats.analyzedCharacters}</span>
        </div>
      ) : null}

      {review ? (
        <article className="review-result">
          <p>{review}</p>
        </article>
      ) : null}

      {error ? <p className="inline-error">{error}</p> : null}
    </div>
  );
}

export default ThesisReviewPanel;
