import { useQuery } from "@tanstack/react-query";
import { getHealth } from "./api/health";

export default function App() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
  });

  return (
    <main style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>Agendamentos</h1>
      {isLoading && <p>Consultando a API...</p>}
      {isError && <p style={{ color: "crimson" }}>Falha: {String(error)}</p>}
      {data && <p style={{ color: "green" }}>API: {data.status}</p>}
    </main>
  );
}