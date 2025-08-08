export default function HomePage() {
  return (
    <div className="min-h-screen bg-cover bg-center text-white" style={{ backgroundImage: `url('/background.jpg')` }}>
      {/* Navbar */}
      {/* <header className="bg-black/60 backdrop-blur-sm p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Melbourne Parking</h1>
        <nav className="space-x-4">
          <a href="#" className="hover:underline">Home</a>
          <a href="#" className="hover:underline">Trends</a>
          <a href="#" className="hover:underline">Insights</a>
          <a href="#" className="hover:underline">Eco</a>
        </nav>
      </header> */}

      {/* Hero Section */}
      <main className="flex flex-col items-center justify-center text-center py-32 px-4">
        <h2 className="text-4xl md:text-6xl font-extrabold">In the City:</h2>
        <p className="text-2xl mt-4 font-semibold">Melbourne Parking For You</p>

        {/* Buttons */}
        <div className="mt-8 flex flex-wrap gap-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">Map</button>
          <button className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg">Trends</button>
          <button className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg">Eco</button>
          <button className="bg-gray-800 hover:bg-gray-900 text-white px-6 py-3 rounded-lg">See Data</button>
        </div>
      </main>
    </div>
  );
}
