import Layout from '../components/Layout';

export default function Bookings() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Your Bookings</h1>
      <div className="space-y-4">
        <div className="p-4 bg-gray-100">No bookings yet.</div>
      </div>
    </Layout>
  );
}
