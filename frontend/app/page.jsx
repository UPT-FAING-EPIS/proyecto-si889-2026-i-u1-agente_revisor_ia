"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "../lib/providers/AuthProvider";

function HomePage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (isLoading) {
      return;
    }

    if (user) {
      router.replace("/dashboard");
      return;
    }

    router.replace("/login");
  }, [isLoading, router, user]);

  return (
    <main className="center-screen">
      <div className="loading-card">Cargando plataforma...</div>
    </main>
  );
}

export default HomePage;
