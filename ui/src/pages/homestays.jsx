import Layout from '../components/Layout';

export default function Homestays() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Homestay Listings</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-gray-100 p-4">Sample Homestay 1</div>
        <div className="bg-gray-100 p-4">Sample Homestay 2</div>
        <div className="bg-gray-100 p-4">Sample Homestay 3</div>
      </div>
    </Layout>
  );
}
