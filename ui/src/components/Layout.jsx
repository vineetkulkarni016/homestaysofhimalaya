import Link from 'next/link';

export default function Layout({ children }) {
  return (
    <div>
      <nav className="bg-blue-600 p-4 flex justify-between items-center">
        <div className="text-white font-bold">Himalaya</div>
        <button aria-label="Open menu" className="text-white md:hidden">Menu</button>
        <div className="hidden md:flex space-x-4 text-white">
          <Link href="/">Home</Link>
          <Link href="/homestays">Homestays</Link>
          <Link href="/bookings">Bookings</Link>
          <Link href="/profile">Profile</Link>
        </div>
      </nav>
      <main className="p-4">{children}</main>
    </div>
  );
}
