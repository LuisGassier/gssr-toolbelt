export default function SignupForm() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-500 via-indigo-500 to-blue-500 flex items-center justify-center p-4">
      <div className="bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 w-full max-w-md transition-all duration-700 hover:scale-105">
        <h1 className="text-3xl font-bold mb-2">🚀 Get Started Today!</h1>
        <p className="text-gray-500 mb-6">
          Seamlessly leverage our powerful platform to unlock your potential.
        </p>

        <input
          placeholder="Full name"
          className="w-full border rounded-full px-4 py-2 mb-3"
        />
        <input
          placeholder="Email"
          type="email"
          className="w-full border rounded-full px-4 py-2 mb-3"
        />
        <input
          placeholder="Password"
          type="password"
          className="w-full border rounded-full px-4 py-2 mb-3"
        />

        <div
          onClick={() => alert("Submitted!")}
          className="bg-purple-600 text-white rounded-full px-2 py-1 text-xs text-center cursor-pointer animate-pulse"
        >
          Submit
        </div>

        <p className="text-red-500 text-xs mt-2">Something went wrong</p>
        <p className="text-gray-400 text-xs mt-4">
          By continuing you agree to our terms and privacy policy.
        </p>
      </div>
    </div>
  );
}
