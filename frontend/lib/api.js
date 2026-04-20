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
  });
}

function listChatMessages(token, chatId) {
  return apiRequest(`/api/chats/${encodeURIComponent(chatId)}/messages`, {
    method: "GET",
    token,
  });
}

function deleteDocument(token, documentId) {
  return apiRequest(`/api/documents/${encodeURIComponent(documentId)}`, {
    method: "DELETE",
    token,
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
  createChatSession,
  deleteDocument,
  evaluateThesis,
  fetchCurrentUser,
  listChatMessages,
  listChatSessions,
  listDocuments,
  loginUser,
  registerUser,
  uploadDocument,
};
