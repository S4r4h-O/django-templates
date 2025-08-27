function FeaturesGrid({ features }) {
  if (!features || features.length === 0) return null;

  return (
    <section className="py-16 bg-white">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div
              key={feature.id}
              className="text-center p-6 rounded-lg border border-gray-200 hover:shadow-lg transition-shadow duration-200"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.text}</h3>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default FeaturesGrid;
