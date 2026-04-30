const configuredBackendUrl = process.env.NEXT_PUBLIC_BACKEND_URL?.trim();
const API_BASE_URL = configuredBackendUrl
  ? configuredBackendUrl.replace(/\/$/, "")
  : "/backend";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

const chatSessionsCache = new Map();
const chatMessagesCache = new Map();

function clonePayload(payload) {
  if (payload == null) {
    return payload;
  }
  return JSON.parse(JSON.stringify(payload));
}

function buildTokenScope(token) {
  if (!token) {
    return "anon";
  }
  return token.slice(0, 16);
}

function buildSessionsCacheKey(token, { documentId = "", mode = "" } = {}) {
  return `${buildTokenScope(token)}::${documentId}::${mode}`;
}

function buildMessagesCacheKey(token, chatId) {
  return `${buildTokenScope(token)}::${chatId || ""}`;
}

function invalidateChatSessionsByDocument(token, documentId = "") {
  const tokenScope = buildTokenScope(token);
  const documentPrefix = `${tokenScope}::${documentId}::`;
  for (const cacheKey of chatSessionsCache.keys()) {
    if (cacheKey.startsWith(documentPrefix)) {
      chatSessionsCache.delete(cacheKey);
    }
  }
}

function setCachedChatSessions(token, { documentId = "", mode = "" } = {}, sessions = []) {
  const cacheKey = buildSessionsCacheKey(token, { documentId, mode });
  chatSessionsCache.set(cacheKey, clonePayload(sessions || []));
}

function setCachedChatMessages(token, chatId, messages = []) {
  if (!chatId) {
    return;
  }
  const cacheKey = buildMessagesCacheKey(token, chatId);
  chatMessagesCache.set(cacheKey, clonePayload(messages || []));
}

function clearCachedChatMessages(token, chatId) {
  if (!chatId) {
    return;
  }
  const cacheKey = buildMessagesCacheKey(token, chatId);
  chatMessagesCache.delete(cacheKey);
}

async function apiRequest(path, options = {}) {
  const {
    method = "GET",
    token,
    body,
    isFormData = false,
    headers = {},
  } = options;

  const requestHeaders = {
    ...headers,
  };

  if (token) {
    requestHeaders.Authorization = `Bearer ${token}`;
  }

  if (!isFormData) {
    requestHeaders["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: requestHeaders,
    body: body ? (isFormData ? body : JSON.stringify(body)) : undefined,
  });

  if (!response.ok) {
    let message = `Error de API (${response.status})`;
    try {
      const payload = await response.json();
      message = payload.detail || payload.message || message;
    } catch {
      // Sin payload JSON, se mantiene el mensaje por defecto.
    }
    throw new ApiError(message, response.status);
  }

  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    return null;
  }

  return response.json();
}

function registerUser(email, password) {
  return apiRequest("/api/auth/register", {
    method: "POST",
    body: { email, password },
  });
}

function loginUser(email, password) {
  return apiRequest("/api/auth/login", {
    method: "POST",
    body: { email, password },
  });
}

function fetchCurrentUser(token) {
  return apiRequest("/api/auth/me", {
    method: "GET",
    token,
  });
}

function listDocuments(token) {
  return apiRequest("/api/documents", {
    method: "GET",
    token,
  });
}

function listChatSessions(token, { documentId, mode } = {}) {
  const cacheKey = buildSessionsCacheKey(token, { documentId, mode });
  const cached = chatSessionsCache.get(cacheKey);
  if (cached) {
    return Promise.resolve(clonePayload(cached));
  }

  const query = new URLSearchParams();
  if (documentId) {
    query.set("document_id", documentId);
  }
  if (mode) {
    query.set("mode", mode);
  }

  const queryString = query.toString();
  const path = queryString ? `/api/chats?${queryString}` : "/api/chats";

  return apiRequest(path, {
    method: "GET",
    token,
  }).then((rows) => {
    const normalized = rows || [];
    setCachedChatSessions(token, { documentId, mode }, normalized);
    return clonePayload(normalized);
  });
}

function createChatSession(token, { documentId, mode, title }) {
  return apiRequest("/api/chats", {
    method: "POST",
    token,
    body: {
      document_id: documentId,
      mode,
      title,
    },
  }).then((created) => {
    if (created) {
      const cacheKey = buildSessionsCacheKey(token, { documentId, mode });
      const current = chatSessionsCache.get(cacheKey) || [];
      const deduped = [created, ...current.filter((session) => session.id !== created.id)];
      chatSessionsCache.set(cacheKey, clonePayload(deduped));
      clearCachedChatMessages(token, created.id);
    }
    return created;
  });
}

function listChatMessages(token, chatId) {
  const cacheKey = buildMessagesCacheKey(token, chatId);
  const cached = chatMessagesCache.get(cacheKey);
  if (cached) {
    return Promise.resolve(clonePayload(cached));
  }

  return apiRequest(`/api/chats/${encodeURIComponent(chatId)}/messages`, {
    method: "GET",
    token,
  }).then((rows) => {
    const normalized = rows || [];
    setCachedChatMessages(token, chatId, normalized);
    return clonePayload(normalized);
  });
}

function deleteDocument(token, documentId) {
  return apiRequest(`/api/documents/${encodeURIComponent(documentId)}`, {
    method: "DELETE",
    token,
  }).then((response) => {
    invalidateChatSessionsByDocument(token, documentId);
    return response;
  });
}

function uploadDocument(token, file, replaceDocumentId = "") {
  const formData = new FormData();
  formData.append("file", file);
  if (replaceDocumentId) {
    formData.append("replace_document_id", replaceDocumentId);
  }

  return apiRequest("/api/upload", {
    method: "POST",
    token,
    body: formData,
    isFormData: true,
  }).then((response) => {
    if (replaceDocumentId) {
      invalidateChatSessionsByDocument(token, replaceDocumentId);
    }
    return response;
  });
}

function evaluateThesis(token, documentId, chatId, message) {
  return apiRequest("/api/thesis/review", {
    method: "POST",
    token,
    body: {
      document_id: documentId,
      chat_id: chatId,
      message,
    },
  });
}

export {
  API_BASE_URL,
  ApiError,
  clearCachedChatMessages,
  createChatSession,
  deleteDocument,
  evaluateThesis,
  fetchCurrentUser,
  listChatMessages,
  listChatSessions,
  listDocuments,
  loginUser,
  registerUser,
  setCachedChatMessages,
  setCachedChatSessions,
  uploadDocument,
};
