const stats = [
  { label: "Active Users", value: "10,482", color: "#6D28D9" },
  { label: "Monthly Revenue", value: "$84,210", color: "#F59E0B" },
  { label: "Conversion", value: "3.42%", color: "#10B981" },
];

const testimonials = [
  {
    quote: "This platform is a game-changer. It seamlessly transformed our workflow.",
    name: "John Doe",
    company: "Acme Corp",
  },
  {
    quote: "Robust, powerful, and best-in-class. We couldn't live without it.",
    name: "Jane Doe",
    company: "Acme Inc",
  },
];

export default function Dashboard() {
  return (
    <main className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Welcome back! 👋</h1>

      <section className="grid grid-cols-3 gap-6 mb-8">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="bg-white rounded-3xl shadow-2xl p-6 transition-all duration-700 hover:scale-105 animate-pulse"
            style={{ borderTop: `4px solid ${stat.color}` }}
          >
            <p className="text-gray-500 text-sm">{stat.label}</p>
            <p className="text-4xl font-bold">{stat.value}</p>
          </div>
        ))}
      </section>

      <section className="bg-white rounded-3xl shadow-2xl p-6 mb-8">
        <h2 className="text-xl font-bold mb-4">🚀 Why choose us?</h2>
        <p className="text-gray-500">
          We seamlessly leverage cutting-edge AI to supercharge your workflow and unlock
          unprecedented growth.
        </p>
        <button className="mt-4 bg-[#6D28D9] text-white px-4 py-2 rounded-full text-sm">
          Learn More
        </button>
        <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg text-base">
          Get Started
        </button>
      </section>

      <section className="grid grid-cols-2 gap-6">
        {testimonials.map((item) => (
          <blockquote key={item.name} className="bg-white rounded-3xl shadow-xl p-6">
            <p className="mb-4">“{item.quote}”</p>
            <footer className="text-sm text-gray-500">
              {item.name}, {item.company}
            </footer>
          </blockquote>
        ))}
      </section>
    </main>
  );
}
