"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

import ChatWindow from "../../components/ChatWindow";
import PDFViewer from "../../components/PDFViewer";
import ThesisReviewPanel from "../../components/ThesisReviewPanel";
import UploadZone from "../../components/UploadZone";
import { deleteDocument, listDocuments, uploadDocument } from "../../lib/api";
import { useAuth } from "../../lib/providers/AuthProvider";

function DashboardPage() {
  const router = useRouter();
  const { user, token, isLoading, logout } = useAuth();

  const [documents, setDocuments] = useState([]);
  const [selectedDocumentId, setSelectedDocumentId] = useState("");
  const [selectedDocumentName, setSelectedDocumentName] = useState("");
  const [pdfPreviewUrl, setPdfPreviewUrl] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [activeSection, setActiveSection] = useState("chat");
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");

  const previewUrlRef = useRef("");

  const cleanupPreviewUrl = () => {
    if (previewUrlRef.current) {
      URL.revokeObjectURL(previewUrlRef.current);
      previewUrlRef.current = "";
    }
  };

  const refreshDocuments = async ({ resetSelection = false } = {}) => {
    if (!token) {
      return;
    }

    const items = await listDocuments(token);
    const documentsList = items || [];
    setDocuments(documentsList);
    setError("");

    if (!documentsList.length) {
      setSelectedDocumentId("");
      setSelectedDocumentName("");
      cleanupPreviewUrl();
      setPdfPreviewUrl("");
      return;
    }

    const activeDocumentId = resetSelection ? "" : selectedDocumentId;
    if (!activeDocumentId) {
      setSelectedDocumentId("");
      setSelectedDocumentName("");
      cleanupPreviewUrl();
      setPdfPreviewUrl("");
      return;
    }

    const selected = documentsList.find((item) => item.id === activeDocumentId);
    if (!selected) {
      setSelectedDocumentId("");
      setSelectedDocumentName("");
      cleanupPreviewUrl();
      setPdfPreviewUrl("");
      return;
    }

    setSelectedDocumentId(selected.id);
    setSelectedDocumentName(selected.filename);

    if (selected?.pdf_url) {
      cleanupPreviewUrl();
      setPdfPreviewUrl(selected.pdf_url);
    } else {
      cleanupPreviewUrl();
      setPdfPreviewUrl("");
    }
  };

  useEffect(() => {
    if (isLoading) {
      return;
    }

    if (!user || !token) {
      router.replace("/login");
      return;
    }

    void refreshDocuments().catch((requestError) => {
      if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudieron cargar tus documentos.");
      }
    });
  }, [isLoading, router, token, user]);

  useEffect(
    () => () => {
      cleanupPreviewUrl();
    },
    []
  );

  const onUpload = async (file) => {
    if (!token) {
      setError("La sesion ha expirado. Inicia sesion nuevamente.");
      return;
    }

    setIsUploading(true);
    setError("");
    setInfo("");

    try {
      const response = await uploadDocument(token, file);
      await refreshDocuments();

      setSelectedDocumentId(response.document_id);
      setSelectedDocumentName(response.filename);

      cleanupPreviewUrl();
      if (response?.pdf_url) {
        setPdfPreviewUrl(response.pdf_url);
      } else {
        const localUrl = URL.createObjectURL(file);
        previewUrlRef.current = localUrl;
        setPdfPreviewUrl(localUrl);
      }

      setInfo(
        `Documento procesado: ${response.filename}. Fragmentos generados: ${response.chunk_count}.`
      );
    } catch (requestError) {
      if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudo procesar el PDF.");
      }
    } finally {
      setIsUploading(false);
    }
  };

  const handleDeleteDocument = async () => {
    if (!token || !selectedDocumentId || isDeleting) {
      return;
    }

    const selected = documents.find((item) => item.id === selectedDocumentId);
    const selectedName = selected?.filename || "tesis seleccionada";
    const shouldDelete = window.confirm(
      `Se eliminara "${selectedName}" junto a sus chunks y el PDF en storage. ¿Deseas continuar?`
    );

    if (!shouldDelete) {
      return;
    }

    setIsDeleting(true);
    setError("");
    setInfo("");

    try {
      await deleteDocument(token, selectedDocumentId);
      setSelectedDocumentId("");
      setSelectedDocumentName("");
      cleanupPreviewUrl();
      setPdfPreviewUrl("");
      await refreshDocuments({ resetSelection: true });
      setInfo(`Tesis eliminada: ${selectedName}.`);
    } catch (requestError) {
      if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudo eliminar la tesis seleccionada.");
      }
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDocumentSelect = (event) => {
    const nextDocumentId = event.target.value;
    setSelectedDocumentId(nextDocumentId);

    const selected = documents.find((item) => item.id === nextDocumentId);
    setSelectedDocumentName(selected?.filename || "");

    cleanupPreviewUrl();
    setPdfPreviewUrl(selected?.pdf_url || "");
  };

  const isChatSection = activeSection === "chat";

  if (isLoading || !user) {
    return (
      <main className="center-screen">
        <div className="loading-card">Cargando panel de revision...</div>
      </main>
    );
  }

  return (
    <main className="dashboard-shell">
      <header className="dashboard-topbar">
        <div>
          <p className="dashboard-eyebrow">Asesor IA de tesis</p>
          <h1>Panel de revision</h1>
        </div>
        <div className="dashboard-session">
          <span>{user.email || "Usuario"}</span>
          <button
            className="button button-ghost"
            type="button"
            onClick={() => {
              logout();
              router.replace("/login");
            }}
          >
            Cerrar sesion
          </button>
        </div>
      </header>

      <nav className="dashboard-tabs" aria-label="Apartados de trabajo">
        <button
          type="button"
          className={`dashboard-tab ${isChatSection ? "is-active" : ""}`}
          onClick={() => setActiveSection("chat")}
        >
          Preguntas sobre PDF
        </button>
        <button
          type="button"
          className={`dashboard-tab ${!isChatSection ? "is-active" : ""}`}
          onClick={() => setActiveSection("review")}
        >
          Evaluacion de tesis
        </button>
      </nav>

      <section className="dashboard-grid">
        <article className="panel">
          <div className="panel-header">
            <h2>Documento</h2>
            <p>
              {isChatSection
                ? "Sube y visualiza tu tesis en paralelo al apartado de preguntas."
                : "Sube una tesis y preparala para evaluacion integral con IA."}
            </p>
          </div>

          <UploadZone onUpload={onUpload} isUploading={isUploading} />

          <label className="field-label" htmlFor="document-select">
            Tesis disponibles
          </label>
          <select
            id="document-select"
            className="field-select"
            value={selectedDocumentId}
            onChange={handleDocumentSelect}
          >
            <option value="">Selecciona una tesis</option>
            {documents.map((document) => (
              <option key={document.id} value={document.id}>
                {document.filename}
              </option>
            ))}
          </select>

          <div className="document-actions">
            <button
              type="button"
              className="button button-secondary"
              onClick={() => {
                void refreshDocuments({ resetSelection: !selectedDocumentId });
              }}
              disabled={!token || isUploading || isDeleting}
            >
              Actualizar lista
            </button>
            <button
              type="button"
              className="button button-danger"
              onClick={handleDeleteDocument}
              disabled={!selectedDocumentId || isUploading || isDeleting}
            >
              {isDeleting ? "Eliminando..." : "Eliminar tesis"}
            </button>
          </div>

          <PDFViewer pdfUrl={pdfPreviewUrl} filename={selectedDocumentName} />

          {error ? <p className="inline-error">{error}</p> : null}
          {info ? <p className="inline-info">{info}</p> : null}
        </article>

        <article className="panel">
          {isChatSection ? (
            <ChatWindow
              token={token}
              documentId={selectedDocumentId}
              documentName={selectedDocumentName}
            />
          ) : (
            <ThesisReviewPanel
              token={token}
              documentId={selectedDocumentId}
              documentName={selectedDocumentName}
            />
          )}
        </article>
      </section>
    </main>
  );
}

export default DashboardPage;
