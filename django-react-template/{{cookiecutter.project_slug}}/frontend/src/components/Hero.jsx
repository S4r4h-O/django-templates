function Hero({ hero }) {
  if (!hero) return null;

  return (
    <section
      className="relative min-h-screen flex items-center justify-center text-white"
      style={% raw %}{{
        backgroundImage: hero.background_image
          ? `url(${hero.background_image})`
          : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}{% endraw %}
    >
      <div className="absolute inset-0 bg-black bg-opacity-40"></div>
      <div className="relative z-10 text-center max-w-4xl px-6">
        <h1 className="text-5xl md:text-6xl font-bold mb-6">{hero.title}</h1>
        {hero.subtitle && (
          <p className="text-xl md:text-2xl mb-8 opacity-90">{hero.subtitle}</p>
        )}
        {hero.features && hero.features.length > 0 && (
          <div className="flex flex-wrap justify-center gap-6 mt-8">
            {hero.features.map((feature) => (
              <div
                key={feature.id}
                className="flex items-center bg-white bg-opacity-20 rounded-lg px-4 py-2"
              >
                <span className="mr-2">{feature.icon}</span>
                <span>{feature.text}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

export default Hero;
