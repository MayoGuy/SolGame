import React from "react";

function Navbar() {
  return (
    <nav className="bg-gray-700 p-6">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <div className="text-white text-lg font-bold">Sol Game (logo??)</div>

        {/* Links */}
        <a href="#" className="text-white hover:text-gray-400">
          Instructions
        </a>
      </div>
    </nav>
  );
}

export default Navbar;
