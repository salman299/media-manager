import React from "react";
import { Provider } from "react-redux";
import { store } from "./store/store";
import Header from "./components/Header";
import Footer from "./components/Footer";
import SearchPage from "./components/SearchPage";

function App() {
  return (
    <Provider store={store}>
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          <SearchPage />
        </main>
        <Footer />
      </div>
    </Provider>
  );
}

export default App;
