"use client";

import { useState } from "react";

export default function Home() {
  const [customerName, setCustomerName] = useState("");
  const [orderId, setOrderId] = useState("");
  const [items, setItems] = useState("");
  const [region, setRegion] = useState("");
  const [priority, setPriority] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult("");
    const payload = {
      customer_name: customerName,
      order_id: orderId,
      items,
      region,
      priority,
    };
    const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/assign-warehouse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setResult(data.result);
    setLoading(false);
  }

  return (
    <main style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Warehouse Assignment Agent</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Customer Name: </label>
          <input value={customerName} onChange={e => setCustomerName(e.target.value)} required />
        </div>
        <div>
          <label>Order ID: </label>
          <input value={orderId} onChange={e => setOrderId(e.target.value)} required />
        </div>
        <div>
          <label>Items: </label>
          <input value={items} onChange={e => setItems(e.target.value)} required />
        </div>
        <div>
          <label>Region: </label>
          <input value={region} onChange={e => setRegion(e.target.value)} required />
        </div>
        <div>
          <label>Priority: </label>
          <input value={priority} onChange={e => setPriority(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading}>Assign Warehouse</button>
      </form>
      {loading && <p>Thinking...</p>}
      {result && (
        <div style={{ marginTop: 24, padding: 12, background: "#f0f0f0" }}>
          <strong>Agent Response:</strong>
          <div>{result}</div>
        </div>
      )}
    </main>
  );
}
