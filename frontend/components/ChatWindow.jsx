"use client";

import { useCompletion } from "ai/react";
import { useEffect, useRef, useState } from "react";

import {
  API_BASE_URL,
  createChatSession,
  listChatMessages,
  listChatSessions,
} from "../lib/api";

function createMessage(role, content) {
  return {
    id: crypto.randomUUID(),
    role,
    content,
  };
}

function ChatWindow({ token, documentId, documentName }) {
  const [chatSessions, setChatSessions] = useState([]);
  const [activeChatId, setActiveChatId] = useState("");
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [activeAssistantId, setActiveAssistantId] = useState("");
  const [localError, setLocalError] = useState("");
  const [isInitializingChats, setIsInitializingChats] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [isCreatingChat, setIsCreatingChat] = useState(false);

  const bottomRef = useRef(null);

  const { completion, complete, isLoading, error, stop, setCompletion } = useCompletion({
    api: `${API_BASE_URL}/api/chat`,
    streamProtocol: "text",
  });

  useEffect(() => {
    if (!activeAssistantId) {
      return;
    }

    setMessages((previous) =>
      previous.map((message) =>
        message.id === activeAssistantId
          ? {
              ...message,
              content: completion,
            }
          : message
      )
    );
  }, [completion, activeAssistantId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, isLoading]);

  useEffect(() => {
    setChatSessions([]);
    setActiveChatId("");
    setMessages([]);
    setQuestion("");
    setLocalError("");
    setActiveAssistantId("");
  }, [documentId]);

  const loadMessagesByChatId = async (chatId) => {
    if (!token || !chatId) {
      setMessages([]);
      return;
    }

    setIsLoadingMessages(true);
    setLocalError("");

    try {
      const rows = await listChatMessages(token, chatId);
      const normalized = (rows || []).map((row) => ({
        id: String(row.id),
        role: row.role,
        content: row.content,
      }));
      setMessages(normalized);
    } catch (requestError) {
      if (requestError instanceof Error) {
        setLocalError(requestError.message);
      } else {
        setLocalError("No se pudo cargar el historial del chat.");
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
      mode: "pdf_chat",
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
      setLocalError("");

      try {
        let nextChatId = await syncSessions();
        if (!nextChatId) {
          const created = await createChatSession(token, {
            documentId,
            mode: "pdf_chat",
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
          setLocalError(requestError.message);
        } else {
          setLocalError("No se pudieron inicializar los chats del documento.");
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
    setLocalError("");

    try {
      const created = await createChatSession(token, {
        documentId,
        mode: "pdf_chat",
      });
      setChatSessions((previous) => [created, ...previous]);
      setActiveChatId(created.id);
      await loadMessagesByChatId(created.id);
      setQuestion("");
    } catch (requestError) {
      if (requestError instanceof Error) {
        setLocalError(requestError.message);
      } else {
        setLocalError("No se pudo crear un nuevo chat para este documento.");
      }
    } finally {
      setIsCreatingChat(false);
    }
  };

  const handleSelectChat = async (event) => {
    const nextChatId = event.target.value;
    setActiveChatId(nextChatId);
    setLocalError("");
    await loadMessagesByChatId(nextChatId);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const cleanQuestion = question.trim();
    if (!cleanQuestion) {
      return;
    }

    if (!documentId) {
      setLocalError("Selecciona o sube una tesis antes de enviar preguntas.");
      return;
    }

    if (!activeChatId) {
      setLocalError("Crea o selecciona un chat para continuar.");
      return;
    }

    const userMessage = createMessage("user", cleanQuestion);
    const assistantId = crypto.randomUUID();

    setCompletion("");

    setMessages((previous) => [
      ...previous,
      userMessage,
      {
        id: assistantId,
        role: "assistant",
        content: "",
      },
    ]);

    setQuestion("");
    setLocalError("");
    setActiveAssistantId(assistantId);

    let completionSucceeded = false;

    try {
      await complete(cleanQuestion, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: {
          chat_id: activeChatId,
          message: cleanQuestion,
          match_count: 10,
        },
      });
      completionSucceeded = true;
    } catch (requestError) {
      const fallbackMessage =
        requestError instanceof Error
          ? requestError.message
          : "No se pudo completar la consulta.";

      setMessages((previous) =>
        previous.map((message) =>
          message.id === assistantId
            ? {
                ...message,
                content: fallbackMessage,
              }
            : message
        )
      );
    }

    if (completionSucceeded) {
      try {
        const refreshedChatId = await syncSessions(activeChatId);
        if (refreshedChatId && refreshedChatId !== activeChatId) {
          await loadMessagesByChatId(refreshedChatId);
        }
      } catch {
        // Si falla la sincronizacion de sesiones no se invalida la respuesta ya obtenida.
      }
    }

    setActiveAssistantId("");
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>Asesor IA</h3>
        <p>
          {documentName
            ? `Conversacion sobre: ${documentName}`
            : "Selecciona una tesis para habilitar el chat."}
        </p>
      </div>

      <div className="chat-session-controls">
        <label className="field-label" htmlFor="chat-session-select">
          Chats de este documento
        </label>
        <div className="chat-session-row">
          <select
            id="chat-session-select"
            className="field-select"
            value={activeChatId}
            onChange={handleSelectChat}
            disabled={!documentId || isInitializingChats || isCreatingChat || isLoading}
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
            disabled={!documentId || isInitializingChats || isCreatingChat || isLoading}
          >
            {isCreatingChat ? "Creando..." : "Nuevo chat"}
          </button>
        </div>
      </div>

      <div className="chat-messages">
        {isLoadingMessages ? (
          <p className="chat-placeholder">Cargando historial del chat...</p>
        ) : null}

        {!isLoadingMessages && messages.length === 0 ? (
          <p className="chat-placeholder">
            Escribe una pregunta como: "Evalua si mi marco metodologico es consistente".
          </p>
        ) : null}

        {messages.map((message) => (
          <article
            key={message.id}
            className={`message-bubble ${message.role === "user" ? "user" : "assistant"}`}
          >
            <p className="message-role">
              {message.role === "user" ? "Tu" : "Asesor IA"}
            </p>
            <p className="message-content">{message.content || "..."}</p>
          </article>
        ))}

        <div ref={bottomRef} />
      </div>

      {localError ? <p className="inline-error">{localError}</p> : null}
      {error ? <p className="inline-error">{error.message}</p> : null}

      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Pregunta sobre tu tesis..."
          rows={3}
          disabled={!documentId || !activeChatId || isLoading || isLoadingMessages}
        />

        <div className="chat-actions">
          <button
            type="submit"
            className="button button-primary"
            disabled={
              !token
              || !documentId
              || !activeChatId
              || !question.trim()
              || isLoading
              || isLoadingMessages
            }
          >
            {isLoading ? "Generando respuesta..." : "Enviar"}
          </button>
          <button
            type="button"
            className="button button-ghost"
            onClick={stop}
            disabled={!isLoading}
          >
            Detener
          </button>
        </div>
      </form>
    </div>
  );
}

export default ChatWindow;
