import React, { useEffect, useRef, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchSearchResults,
  setSearchQuery,
  setSelectedDb,
  setSelectedPhotographer,
  incrementPage,
  fetchAggregations,
} from "../store/searchSlice";

function SearchPage() {
  const dispatch = useDispatch();
  const {
    results,
    aggregations,
    total,
    searchQuery,
    selectedDbs,
    selectedPhotographers,
    page,
    isLoading,
    error,
    globalAggregations,
    aggregationsLoading,
    aggregationsError,
  } = useSelector((state) => state.search);

  const [inputValue, setInputValue] = React.useState("");
  const pageSize = 20;
  const observer = useRef();

  // Ref for the last element in the list to observe for infinite scroll
  const lastResultElementRef = useCallback(
    (node) => {
      if (isLoading) return;
      if (observer.current) observer.current.disconnect();
      observer.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && results.length < total) {
          dispatch(incrementPage());
        }
      });
      if (node) observer.current.observe(node);
    },
    [isLoading, results.length, total, dispatch]
  );

  // Fetch search results when dependencies change
  useEffect(() => {
    dispatch(
      fetchSearchResults({
        query: searchQuery,
        selectedDbs,
        selectedPhotographers,
        page,
        pageSize,
      })
    );
  }, [dispatch, searchQuery, selectedDbs, selectedPhotographers, page, pageSize]);

  // Fetch global aggregations when component mounts
  useEffect(() => {
    dispatch(fetchAggregations());
  }, [dispatch]);

  const handleSearch = (e) => {
    e.preventDefault();
    dispatch(setSearchQuery(inputValue.trim()));
  };

  const handleDbFilter = (db) => {
    dispatch(setSelectedDb(db));
  };

  const handlePhotographerFilter = (photographer) => {
    dispatch(setSelectedPhotographer(photographer));
  };

  // Helper function to format large numbers
  const formatCount = (count) => {
    if (count >= 1000) {
      return `${(count / 1000).toFixed(1).replace(/\.0$/, "")}K`;
    }
    return count.toString();
  };

  return (
    <div className="flex flex-col md:flex-row gap-6">
      {/* Left: Images Grid */}
      <div className="flex-1">
        <div className="mb-4">
          <form onSubmit={handleSearch} className="flex max-w-xl">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Search images..."
              className="w-full px-4 py-2 border border-gray-300 rounded-l-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Search
            </button>
          </form>

          {/* Results Count */}
          {!isLoading && (
            <div className="mt-3 text-sm text-gray-600">
              Viewing {results.length} of {total} results
            </div>
          )}

          {/* Filter Tags */}
          {(selectedDbs.length > 0 || selectedPhotographers.length > 0) && (
            <div className="mt-3 flex flex-wrap gap-2">
              {selectedDbs.map((db) => (
                <div
                  key={db}
                  className="inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                >
                  <span>Database: {db}</span>
                  <button
                    onClick={() => handleDbFilter(db)}
                    className="ml-2 text-blue-600 hover:text-blue-800 focus:outline-none"
                  >
                    ×
                  </button>
                </div>
              ))}
              {selectedPhotographers.map((photographer) => (
                <div
                  key={photographer}
                  className="inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                >
                  <span>Photographer: {photographer}</span>
                  <button
                    onClick={() => handlePhotographerFilter(photographer)}
                    className="ml-2 text-blue-600 hover:text-blue-800 focus:outline-none"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-4">
            {error}
          </div>
        )}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((result, index) => {
            if (results.length === index + 1) {
              return (
                <div
                  ref={lastResultElementRef}
                  key={result.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden flex flex-col"
                >
                  <img
                    src={result.source.thumbnail_url}
                    alt={result.source.search_text?.slice(0, 40) || "Image"}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4 flex-1 flex flex-col">
                    <div className="text-sm text-gray-500 mb-1 truncate">
                      {result.source.photographers}
                    </div>
                    <div className="font-semibold text-gray-800 mb-2 truncate">
                      {result.source.search_text?.slice(0, 60)}
                    </div>
                    <div className="text-xs text-gray-400 mt-auto">
                      {result.source.database}
                    </div>
                  </div>
                </div>
              );
            } else {
              return (
                <div
                  key={result.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden flex flex-col"
                >
                  <img
                    src={result.source.thumbnail_url}
                    alt={result.source.search_text?.slice(0, 40) || "Image"}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4 flex-1 flex flex-col">
                    <div className="text-sm text-gray-500 mb-1 truncate">
                      {result.source.photographers}
                    </div>
                    <div className="font-semibold text-gray-800 mb-2 truncate">
                      {result.source.search_text?.slice(0, 60)}
                    </div>
                    <div className="text-xs text-gray-400 mt-auto">
                      {result.source.database}
                    </div>
                  </div>
                </div>
              );
            }
          })}
        </div>
        {isLoading && (
          <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}
        {/* Adjusted conditional rendering for no results / end of results */}
        {!isLoading && results.length === 0 && searchQuery && !error && (
          <div className="text-center py-8">
            <p className="text-gray-600">
              No results found for your current search or filters.
            </p>
          </div>
        )}
        {!isLoading && results.length > 0 && results.length >= total && (
          <div className="text-center py-8 text-gray-500">
            <p>You've reached the end of the results.</p>
          </div>
        )}
      </div>
      {/* Right: Filters */}
      <aside className="w-full md:w-72 bg-white rounded-lg shadow-md p-6 h-fit">
        <h3 className="text-lg font-bold mb-4">Refine Your Search</h3>

        {aggregationsLoading && (
          <div className="flex justify-center items-center py-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        )}

        {aggregationsError && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-4 text-sm">
            Error loading filters: {aggregationsError}
          </div>
        )}

        {!aggregationsLoading && !aggregationsError && (
          <>
            {/* DB Filter */}
            <div className="mb-6">
              <div className="font-semibold text-gray-700 mb-2">Database</div>
              <ul className="max-h-60 overflow-y-auto pr-1">
                {globalAggregations.db_terms?.buckets.map((bucket) => (
                  <li key={bucket.key}>
                    <button
                      className={`flex items-center justify-between w-full px-2 py-1 rounded hover:bg-blue-50 mb-1 text-left ${
                        selectedDbs.includes(bucket.key)
                          ? "bg-blue-100 text-blue-700 font-bold"
                          : ""
                      }`}
                      onClick={() => handleDbFilter(bucket.key)}
                      type="button"
                    >
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          checked={selectedDbs.includes(bucket.key)}
                          onChange={() => {}}
                          className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span>{bucket.key}</span>
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
            {/* Photographer Filter */}
            <div>
              <div className="font-semibold text-gray-700 mb-2">Photographer</div>
              <ul className="max-h-60 overflow-y-auto pr-1">
                {globalAggregations.photographer_terms?.buckets.map((bucket) => (
                  <li key={bucket.key}>
                    <button
                      className={`flex items-center justify-between w-full px-2 py-1 rounded hover:bg-blue-50 mb-1 text-left ${
                        selectedPhotographers.includes(bucket.key)
                          ? "bg-blue-100 text-blue-700 font-bold"
                          : ""
                      }`}
                      onClick={() => handlePhotographerFilter(bucket.key)}
                      type="button"
                    >
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          checked={selectedPhotographers.includes(bucket.key)}
                          onChange={() => {}}
                          className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span>{bucket.key}</span>
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}
      </aside>
    </div>
  );
}

export default SearchPage;
