"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { ApiError } from "../../lib/api";
import { useAuth } from "../../lib/providers/AuthProvider";

function LoginPage() {
  const router = useRouter();
  const { login, user, isLoading, authError } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!isLoading && user) {
      router.replace("/dashboard");
    }
  }, [isLoading, router, user]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (requestError) {
      if (requestError instanceof ApiError) {
        setError(requestError.message);
      } else if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudo iniciar sesion.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <p className="auth-eyebrow">Asesor IA de tesis</p>
        <h1>Iniciar sesion</h1>
        <p className="auth-description">
          Entra para subir tu tesis, generar embeddings y conversar con el asesor.
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Correo institucional
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="estudiante@universidad.edu"
              required
              autoComplete="email"
            />
          </label>

          <label>
            Contrasena
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Minimo 6 caracteres"
              required
              minLength={6}
              autoComplete="current-password"
            />
          </label>

          <button className="button button-primary" type="submit" disabled={submitting}>
            {submitting ? "Ingresando..." : "Entrar"}
          </button>
        </form>

        {error ? <p className="inline-error">{error}</p> : null}
        {authError ? <p className="inline-info">{authError}</p> : null}

        <p className="auth-switch">
          Aun no tienes cuenta? <Link href="/register">Crear cuenta</Link>
        </p>
      </section>
    </main>
  );
}

export default LoginPage;
