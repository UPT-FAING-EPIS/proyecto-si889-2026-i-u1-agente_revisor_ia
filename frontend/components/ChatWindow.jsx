"use client";

import { useCompletion } from "ai/react";
import { useEffect, useRef, useState } from "react";

import { API_BASE_URL } from "../lib/api";

function createMessage(role, content) {
  return {
    id: crypto.randomUUID(),
    role,
    content,
  };
}

function ChatWindow({ token, documentId, documentName }) {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [activeAssistantId, setActiveAssistantId] = useState("");
  const [localError, setLocalError] = useState("");

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
    setMessages([]);
    setQuestion("");
    setLocalError("");
    setActiveAssistantId("");
  }, [documentId]);

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

    const userMessage = createMessage("user", cleanQuestion);
    const assistantId = crypto.randomUUID();
    const historyPayload = [...messages, userMessage].map(({ role, content }) => ({
      role,
      content,
    }));

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

    try {
      await complete(cleanQuestion, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: {
          document_id: documentId,
          message: cleanQuestion,
          history: historyPayload,
          match_count: 10,
        },
      });
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
    } finally {
      setActiveAssistantId("");
    }
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

      <div className="chat-messages">
        {messages.length === 0 ? (
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
          disabled={!documentId || isLoading}
        />

        <div className="chat-actions">
          <button
            type="submit"
            className="button button-primary"
            disabled={!token || !documentId || !question.trim() || isLoading}
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
