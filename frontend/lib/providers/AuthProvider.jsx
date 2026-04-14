"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { fetchCurrentUser, loginUser, registerUser } from "../api";

const TOKEN_STORAGE_KEY = "thesis-ai-access-token";

const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [authError, setAuthError] = useState("");

  const persistToken = (nextToken) => {
    if (typeof window === "undefined") {
      return;
    }

    if (nextToken) {
      window.localStorage.setItem(TOKEN_STORAGE_KEY, nextToken);
    } else {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
  };

  const hydrateUser = async (candidateToken) => {
    try {
      const currentUser = await fetchCurrentUser(candidateToken);
      setToken(candidateToken);
      setUser(currentUser);
      setAuthError("");
      return currentUser;
    } catch {
      persistToken(null);
      setToken(null);
      setUser(null);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (typeof window === "undefined") {
      setIsLoading(false);
      return;
    }

    const storedToken = window.localStorage.getItem(TOKEN_STORAGE_KEY);
    if (!storedToken) {
      setIsLoading(false);
      return;
    }

    void hydrateUser(storedToken);
  }, []);

  const login = async (email, password) => {
    setAuthError("");
    const payload = await loginUser(email, password);

    if (!payload?.access_token) {
      throw new Error("No se recibio un access token al iniciar sesion.");
    }

    persistToken(payload.access_token);
    setToken(payload.access_token);
    const resolvedUser = payload.user || (await fetchCurrentUser(payload.access_token));
    setUser(resolvedUser || null);
    return payload;
  };

  const register = async (email, password) => {
    setAuthError("");
    const payload = await registerUser(email, password);

    if (payload?.access_token) {
      persistToken(payload.access_token);
      setToken(payload.access_token);
      const resolvedUser = payload.user || (await fetchCurrentUser(payload.access_token));
      setUser(resolvedUser || null);
    }

    if (payload?.message) {
      setAuthError(payload.message);
    }

    return payload;
  };

  const logout = () => {
    persistToken(null);
    setToken(null);
    setUser(null);
    setAuthError("");
  };

  const value = useMemo(
    () => ({
      token,
      user,
      isLoading,
      authError,
      login,
      register,
      logout,
    }),
    [token, user, isLoading, authError]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth debe usarse dentro de AuthProvider.");
  }
  return context;
}

export { AuthProvider, useAuth };
