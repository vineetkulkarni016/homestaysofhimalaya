import Layout from '../components/Layout';

export default function Profile() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">User Profile</h1>
      <div className="max-w-md space-y-4">
        <div className="flex flex-col md:flex-row md:items-center">
          <label className="md:w-1/3">Name</label>
          <input className="border p-2 w-full md:w-2/3" placeholder="Your name" />
        </div>
        <div className="flex flex-col md:flex-row md:items-center">
          <label className="md:w-1/3">Email</label>
          <input className="border p-2 w-full md:w-2/3" placeholder="you@example.com" />
        </div>
      </div>
    </Layout>
  );
}
