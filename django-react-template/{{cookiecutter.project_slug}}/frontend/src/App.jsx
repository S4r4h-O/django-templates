import { useEffect, useState } from "react";
import { fetchHomepage } from "./services/api";

function App() {
  const [homepage, setHomepage] = useState(null);

  useEffect(() => {
    fetchHomepage()
      .then((data) => setHomepage(data))
      .catch((err) => console.error(err));
  }, []);

  if (!homepage) return <div className="font-bold text-lg">Carregando...</div>;

  const { hero, testimonials, blog_highlights, ctas } = homepage;

  return (
    <div>
      <h1>{hero?.title}</h1>
    </div>
  );
}

export default App;
