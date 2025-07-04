import { useState } from "react";
import PriceCard from "./components/PriceCard";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { LatLngExpression } from "leaflet";
type City = "Chicago" | "New York City";

function App() {
  const [city, setCity] = useState<City>("Chicago");

  const cityCoord: Record<City, LatLngExpression> = {
    Chicago: [41.8781, -87.6298],
    "New York City": [40.7128, -74.006],
  };

  return (
    <div className="p-4">
      <div className="w-full text-center">
        <select
          defaultValue="Chicago"
          className="select select-info"
          onChange={(e) => setCity(e.target.value as City)}
        >
          <option disabled={true}>Pick a City</option>
          <option>Chicago</option>
          <option>New York City</option>
        </select>
      </div>
      <MapContainer
        className="mx-auto mt-4"
        key={city}
        center={cityCoord[city]}
        zoom={13}
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      </MapContainer>
      <PriceCard />
    </div>
  );
}

export default App;
