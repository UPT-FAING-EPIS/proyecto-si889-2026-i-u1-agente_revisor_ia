"use client";

import { useEffect, useState } from "react";

import {
  createChatSession,
  evaluateThesis,
  listChatMessages,
  listChatSessions,
} from "../lib/api";

function ThesisReviewPanel({ token, documentId, documentName }) {
  const [chatSessions, setChatSessions] = useState([]);
  const [activeChatId, setActiveChatId] = useState("");
  const [messages, setMessages] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [stats, setStats] = useState(null);
  const [isReviewing, setIsReviewing] = useState(false);
  const [isInitializingChats, setIsInitializingChats] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [isCreatingChat, setIsCreatingChat] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setChatSessions([]);
    setActiveChatId("");
    setMessages([]);
    setPrompt("");
    setStats(null);
    setError("");
  }, [documentId]);

  const loadMessagesByChatId = async (chatId) => {
    if (!token || !chatId) {
      setMessages([]);
      return;
    }

    setIsLoadingMessages(true);
    setError("");

    try {
      const rows = await listChatMessages(token, chatId);
      setMessages((rows || []).map((row) => ({
        id: String(row.id),
        role: row.role,
        content: row.content,
      })));
    } catch (requestError) {
      if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudo cargar el historial de revision.");
      }
      setMessages([]);
    } finally {
      setIsLoadingMessages(false);
    }
  };

  const syncSessions = async (preferredChatId = "") => {
    if (!token || !documentId) {
      setChatSessions([]);
      setActiveChatId("");
      setMessages([]);
      return "";
    }

    const sessions = (await listChatSessions(token, {
      documentId,
      mode: "thesis_review",
    })) || [];
    setChatSessions(sessions);

    const hasPreferred = preferredChatId && sessions.some((session) => session.id === preferredChatId);
    const nextChatId = hasPreferred ? preferredChatId : sessions[0]?.id || "";
    setActiveChatId(nextChatId);
    return nextChatId;
  };

  useEffect(() => {
    let cancelled = false;

    const bootstrapSessions = async () => {
      if (!token || !documentId) {
        return;
      }

      setIsInitializingChats(true);
      setError("");

      try {
        let nextChatId = await syncSessions();
        if (!nextChatId) {
          const created = await createChatSession(token, {
            documentId,
            mode: "thesis_review",
          });

          if (cancelled) {
            return;
          }

          setChatSessions([created]);
          nextChatId = created.id;
          setActiveChatId(nextChatId);
        }

        if (!cancelled && nextChatId) {
          await loadMessagesByChatId(nextChatId);
        }
      } catch (requestError) {
        if (cancelled) {
          return;
        }

        if (requestError instanceof Error) {
          setError(requestError.message);
        } else {
          setError("No se pudieron inicializar los chats de revision.");
        }
      } finally {
        if (!cancelled) {
          setIsInitializingChats(false);
        }
      }
    };

    void bootstrapSessions();
    return () => {
      cancelled = true;
    };
  }, [documentId, token]);

  const handleCreateChat = async () => {
    if (!token || !documentId || isCreatingChat) {
      return;
    }

    setIsCreatingChat(true);
    setError("");

    try {
      const created = await createChatSession(token, {
        documentId,
        mode: "thesis_review",
      });
      setChatSessions((previous) => [created, ...previous]);
      setActiveChatId(created.id);
      setStats(null);
      setPrompt("");
      await loadMessagesByChatId(created.id);
    } catch (requestError) {
      if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudo crear un nuevo chat de revision.");
      }
    } finally {
      setIsCreatingChat(false);
    }
  };

  const handleSelectChat = async (event) => {
    const nextChatId = event.target.value;
    setActiveChatId(nextChatId);
    setStats(null);
    setError("");
    await loadMessagesByChatId(nextChatId);
  };

  const onReview = async () => {
    if (!token || !documentId || !activeChatId) {
      return;
    }

    const cleanPrompt = prompt.trim()
      || "Evalua integralmente esta tesis y prioriza las mejoras de mayor impacto.";

    setIsReviewing(true);
    setError("");

    try {
      const response = await evaluateThesis(token, documentId, activeChatId, cleanPrompt);
      setStats({
        totalChunks: response?.total_chunks || 0,
        analyzedChunks: response?.analyzed_chunks || 0,
        analyzedCharacters: response?.analyzed_characters || 0,
      });
      setPrompt("");

      await loadMessagesByChatId(activeChatId);
      await syncSessions(activeChatId);
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

      <div className="chat-session-controls">
        <label className="field-label" htmlFor="review-chat-session-select">
          Chats de revision
        </label>
        <div className="chat-session-row">
          <select
            id="review-chat-session-select"
            className="field-select"
            value={activeChatId}
            onChange={handleSelectChat}
            disabled={!documentId || isInitializingChats || isCreatingChat || isReviewing}
          >
            <option value="">
              {documentId ? "Selecciona un chat" : "Primero selecciona una tesis"}
            </option>
            {chatSessions.map((session) => (
              <option key={session.id} value={session.id}>
                {session.title}
              </option>
            ))}
          </select>
          <button
            type="button"
            className="button button-secondary"
            onClick={handleCreateChat}
            disabled={!documentId || isInitializingChats || isCreatingChat || isReviewing}
          >
            {isCreatingChat ? "Creando..." : "Nuevo chat"}
          </button>
        </div>
      </div>

      <div className="chat-form review-chat-form">
        <textarea
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          rows={3}
          placeholder="Ejemplo: Evalua solo coherencia metodologica y consistencia entre objetivos e hipotesis"
          disabled={!documentId || !activeChatId || isReviewing || isLoadingMessages}
        />
      </div>

      <div className="review-actions">
        <button
          type="button"
          className="button button-primary"
          disabled={!token || !documentId || !activeChatId || isReviewing || isLoadingMessages}
          onClick={onReview}
        >
          {isReviewing ? "Analizando tesis completa..." : "Evaluar tesis"}
        </button>
      </div>

      {!messages.length && !isReviewing ? (
        <div className="review-placeholder">
          <p>
            La IA guardara cada revision en este chat para que puedas seguir iterando sobre
            tu tesis con contexto acumulado.
          </p>
        </div>
      ) : null}

      {stats ? (
        <div className="review-stats">
          <span>Fragmentos: {stats.analyzedChunks}/{stats.totalChunks}</span>
          <span>Caracteres analizados: {stats.analyzedCharacters}</span>
        </div>
      ) : null}

      <div className="chat-messages review-chat-messages">
        {isLoadingMessages ? <p className="chat-placeholder">Cargando historial...</p> : null}
        {!isLoadingMessages && !messages.length ? (
          <p className="chat-placeholder">Aun no hay revisiones en este chat.</p>
        ) : null}
        {messages.map((message) => (
          <article
            key={message.id}
            className={`message-bubble ${message.role === "user" ? "user" : "assistant"}`}
          >
            <p className="message-role">
              {message.role === "user" ? "Tu solicitud" : "Evaluador IA"}
            </p>
            {message.role === "assistant" ? (
              <pre className="review-content">{message.content}</pre>
            ) : (
              <p className="message-content">{message.content}</p>
            )}
          </article>
        ))}
      </div>

      {error ? <p className="inline-error">{error}</p> : null}
    </div>
  );
}

export default ThesisReviewPanel;
