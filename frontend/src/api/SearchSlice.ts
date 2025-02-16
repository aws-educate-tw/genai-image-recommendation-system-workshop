import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

export const SearchSlice = createApi({
  reducerPath: "search",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
  }),
  endpoints: builder => ({
    searchByImage: builder.mutation({
      query: (payload) => {
        return {
        url: "/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: { search_image: payload }, 
      }
    },
    }),
    searchByText: builder.mutation({
      query: (payload) => {
        return {
        url: "/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: { search_image: payload }, 
      }
    },
    }),
  }),
})

export const {
  useSearchByTextMutation,
  useSearchByImageMutation,
} = SearchSlice
