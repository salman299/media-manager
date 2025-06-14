import React from "react";

function Footer() {
  return (
    <footer className="bg-white border-t">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col items-center justify-center">
          <p className="text-gray-600 text-sm">
            © {new Date().getFullYear()} Media Manager. All rights reserved.
          </p>
          <div className="mt-2 flex space-x-4">
            <a
              href="/privacy"
              className="text-gray-500 hover:text-gray-900 text-sm"
            >
              Privacy Policy
            </a>
            <a
              href="/terms"
              className="text-gray-500 hover:text-gray-900 text-sm"
            >
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
