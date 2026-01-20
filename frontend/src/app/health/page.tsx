export default async function HealthPage() {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  const res = await fetch(`${baseUrl}/health`, { cache: "no-store" });
  const data = await res.json();

  return (
    <main style={{ padding: 20 }}>
      <h1>Backend Healh</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </main>
  );
}
