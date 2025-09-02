import React, { useState } from 'react';

export default function HostsDashboard() {
  const [properties] = useState([]);
  return (
    <div>
      <h1>Host Dashboard</h1>
      <p>Manage properties, inventory, pricing and availability.</p>
      <p>Analytics coming soon.</p>
      <ul>
        {properties.map(p => (
          <li key={p.id}>{p.name} - {p.location}</li>
        ))}
      </ul>
    </div>
  );
}
