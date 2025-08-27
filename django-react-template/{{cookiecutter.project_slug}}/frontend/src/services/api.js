const API_URL = import.meta.env.VITE_API_URL;

export async function fetchHomepage() {
  const res = await fetch(`${API_URL}/homepage/`);
  if (!res.ok) {
    throw new Error("Erro ao buscar homepage");
  }
  return res.json();
}
