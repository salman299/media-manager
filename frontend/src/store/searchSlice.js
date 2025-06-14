import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

// Async thunk for fetching search results
export const fetchSearchResults = createAsyncThunk(
  "search/fetchResults",
  async (
    { query, selectedDb, selectedPhotographer, page, pageSize },
    { rejectWithValue }
  ) => {
    try {
      const params = new URLSearchParams();
      params.append("query", query);
      if (selectedDb) params.append("db", selectedDb);
      if (selectedPhotographer)
        params.append("photographer", selectedPhotographer);
      params.append("page", page);
      params.append("page_size", pageSize);

      const url = `${API_BASE_URL}/api/search/?${params.toString()}`;
      console.log("Fetching from URL:", url); // Debug log

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });

      // Log response details for debugging
      console.log("Response status:", response.status);
      console.log(
        "Response headers:",
        Object.fromEntries(response.headers.entries())
      );

      if (!response.ok) {
        // Try to get error details from response
        const contentType = response.headers.get("content-type");
        let errorMessage;

        if (contentType && contentType.includes("application/json")) {
          const errorData = await response.json();
          errorMessage =
            errorData.message || errorData.detail || "Search failed";
        } else {
          const text = await response.text();
          console.error("Non-JSON error response:", text);
          errorMessage = `Search failed: ${response.status} ${response.statusText}`;
        }

        throw new Error(errorMessage);
      }

      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await response.text();
        console.error("Non-JSON response:", text);
        throw new Error("Server returned non-JSON response");
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Search error details:", error);
      return rejectWithValue(error.message || "Failed to fetch search results");
    }
  }
);

const initialState = {
  results: [],
  aggregations: {
    db_terms: { buckets: [] },
    photographer_terms: { buckets: [] },
  },
  total: 0,
  searchQuery: "",
  selectedDb: null,
  selectedPhotographer: null,
  page: 1,
  isLoading: false,
  error: null,
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    setSearchQuery: (state, action) => {
      state.searchQuery = action.payload;
      state.page = 1;
      state.results = [];
    },
    setSelectedDb: (state, action) => {
      state.selectedDb =
        action.payload === state.selectedDb ? null : action.payload;
      state.page = 1;
      state.results = [];
    },
    setSelectedPhotographer: (state, action) => {
      state.selectedPhotographer =
        action.payload === state.selectedPhotographer ? null : action.payload;
      state.page = 1;
      state.results = [];
    },
    incrementPage: (state) => {
      state.page += 1;
    },
    clearFilters: (state) => {
      state.selectedDb = null;
      state.selectedPhotographer = null;
      state.page = 1;
      state.results = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchSearchResults.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchSearchResults.fulfilled, (state, action) => {
        state.isLoading = false;
        if (state.page === 1) {
          state.results = action.payload.results;
        } else {
          state.results = [...state.results, ...action.payload.results];
        }
        state.aggregations = action.payload.aggregations;
        state.total = action.payload.total;
      })
      .addCase(fetchSearchResults.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || "Failed to fetch search results";
      });
  },
});

export const {
  setSearchQuery,
  setSelectedDb,
  setSelectedPhotographer,
  incrementPage,
  clearFilters,
} = searchSlice.actions;

export default searchSlice.reducer;
