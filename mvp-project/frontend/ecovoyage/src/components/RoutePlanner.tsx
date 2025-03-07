import React, { useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const RoutePlanner: React.FC = () => {
  const [start, setStart] = useState<string>('');
  const [end, setEnd] = useState<string>('');
  const [transport, setTransport] = useState<string>('bike');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Маршрут: от ${start} до ${end} на ${transport}`);
  };

  return (
    <div className="w-full max-w-lg mx-auto bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold text-green-700 mb-4">Планирование эко-маршрута</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col">
          <label className="text-green-600 mb-1">Откуда:</label>
          <input
            type="text"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            placeholder="Введите начальную точку"
            className="p-2 border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-green-600 mb-1">Куда:</label>
          <input
            type="text"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            placeholder="Введите конечную точку"
            className="p-2 border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-green-600 mb-1">Способ передвижения:</label>
          <select
            value={transport}
            onChange={(e) => setTransport(e.target.value)}
            className="p-2 border border-green-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500 text-green-800"
          >
            <option value="bike">Велосипед</option>
            <option value="walk">Пешком</option>
            <option value="public">Общественный транспорт</option>
          </select>
        </div>
        <button
          type="submit"
          className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700 transition"
        >
          Построить маршрут
        </button>
      </form>
      <div className="mt-6">
        <MapContainer
          center={[55.751244, 37.618423]}
          zoom={13}
          style={{ height: '300px', width: '100%' }}
          className="rounded-lg shadow-md"
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
        </MapContainer>
      </div>
    </div>
  );
};

export default RoutePlanner;