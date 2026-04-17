import Link from "next/link";

function NotFoundPage() {
  return (
    <main className="notfound-shell">
      <section className="notfound-card">
        <p className="auth-eyebrow">Asesor IA de tesis</p>
        <p className="notfound-code">404</p>
        <h1>Pagina no encontrada</h1>
        <p className="notfound-description">
          La ruta que intentaste abrir no existe o fue movida. Puedes volver al panel
          principal o iniciar sesion nuevamente.
        </p>

        <div className="notfound-actions">
          <Link href="/dashboard" className="button button-primary notfound-link">
            Ir al dashboard
          </Link>
          <Link href="/login" className="button button-ghost notfound-link">
            Ir a login
          </Link>
        </div>
      </section>
    </main>
  );
}

export default NotFoundPage;
