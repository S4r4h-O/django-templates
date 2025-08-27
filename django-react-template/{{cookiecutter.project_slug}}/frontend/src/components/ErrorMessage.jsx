function ErrorMessage({ message }) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center p-8">
        <h2 className="text-2xl font-bold text-red-600 mb-4">Erro</h2>
        <p className="text-gray-600">{message}</p>
      </div>
    </div>
  );
}

export default ErrorMessage;
