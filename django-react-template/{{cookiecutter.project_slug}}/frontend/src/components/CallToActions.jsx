function CallToActions({ ctas }) {
  if (!ctas || ctas.length === 0) return null;

  return (
    <section className="py-16 bg-gray-100">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-wrap justify-center gap-6">
          {ctas.map((cta) => (
            <a
              key={cta.id}
              href={cta.url}
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
            >
              {cta.label}
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

export default CallToActions;
