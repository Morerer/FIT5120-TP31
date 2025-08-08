const HeroSection = () => {
  return (
    <div className="flex flex-col items-center text-center px-4 py-12 max-w-3xl mx-auto">
      
      <div className="w-full bg-gray-400 h-56 mb-8 rounded-md flex items-center justify-center">
        <span className="text-white text-2xl">Image</span>
      </div>

      
      <h1 className="text-4xl font-bold mb-2">IN THE CITY:</h1>
      <h2 className="text-xl mb-6 text-gray-700">MELBOURNE PARKING FOR YOU</h2>

      

      {/* Buttons */}
      <div className="mt-8 flex flex-wrap gap-4 justify-center">
        {['TRENDS', 'INSIGHTS', 'ECO', 'SEE DATA'].map((label) => (
          <button
            key={label}
            className="bg-gray-300 hover:bg-gray-400 px-4 py-2 rounded text-sm font-semibold"
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default HeroSection;
