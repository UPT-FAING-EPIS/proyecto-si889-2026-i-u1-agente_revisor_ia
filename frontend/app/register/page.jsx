"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { ApiError } from "../../lib/api";
import { useAuth } from "../../lib/providers/AuthProvider";

function RegisterPage() {
  const router = useRouter();
  const { register, user, isLoading } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [feedback, setFeedback] = useState("");
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
    setFeedback("");

    if (password !== confirmPassword) {
      setError("Las contrasenas no coinciden.");
      return;
    }

    setSubmitting(true);

    try {
      const payload = await register(email, password);
      if (payload?.access_token) {
        router.push("/dashboard");
        return;
      }

      setFeedback(
        payload?.message ||
          "Cuenta creada. Si activaste confirmacion por correo, revisa tu bandeja y luego inicia sesion."
      );
    } catch (requestError) {
      if (requestError instanceof ApiError) {
        setError(requestError.message);
      } else if (requestError instanceof Error) {
        setError(requestError.message);
      } else {
        setError("No se pudo completar el registro.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="auth-shell">
      <section className="auth-card">
        <p className="auth-eyebrow">Asesor IA de tesis</p>
        <h1>Crear cuenta</h1>
        <p className="auth-description">
          Registra tu cuenta para procesar tesis y conversar con el revisor inteligente.
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Correo
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
              autoComplete="new-password"
            />
          </label>

          <label>
            Confirmar contrasena
            <input
              type="password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              placeholder="Repite la contrasena"
              required
              minLength={6}
              autoComplete="new-password"
            />
          </label>

          <button className="button button-primary" type="submit" disabled={submitting}>
            {submitting ? "Creando cuenta..." : "Crear cuenta"}
          </button>
        </form>

        {error ? <p className="inline-error">{error}</p> : null}
        {feedback ? <p className="inline-info">{feedback}</p> : null}

        <p className="auth-switch">
          Ya tienes cuenta? <Link href="/login">Iniciar sesion</Link>
        </p>
      </section>
    </main>
  );
}

export default RegisterPage;
