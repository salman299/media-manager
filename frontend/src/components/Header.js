import React from "react";

function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-gray-800">Media Manager</h1>
          </div>
          <nav className="flex items-center space-x-4">
            <a
              href="/"
              className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              Home
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;
