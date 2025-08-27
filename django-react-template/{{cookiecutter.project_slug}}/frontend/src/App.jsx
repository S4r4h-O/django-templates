import { useEffect, useState } from "react";
import { fetchHomepage } from "./services/api";
import Hero from "./components/Hero";
import CallToActions from "./components/CallToActions";
import FeaturesGrid from "./components/FeaturesGrid";
import Loading from "./components/Loading";
import ErrorMessage from "./components/ErrorMessage";

function App() {
  const [homepage, setHomepage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHomepage()
      .then((data) => {
        setHomepage(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;
  if (!homepage) return <ErrorMessage message="Dados não encontrados" />;

  const { hero, ctas } = homepage;

  return (
    <div className="min-h-screen">
      <Hero hero={hero} />
      {hero?.features && <FeaturesGrid features={hero.features} />}
      <CallToActions ctas={ctas} />
    </div>
  );
}

export default App;
