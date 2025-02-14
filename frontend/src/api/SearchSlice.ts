import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

export const SearchSlice = createApi({
  reducerPath: "search",
  baseQuery: fetchBaseQuery({
    baseUrl: "",
  }),
  endpoints: builder => ({
    basic: builder.query({
      query: () => ({
        url: `/`,
        method: "GET",
      }),
    }),
    searchByText: builder.mutation({
      query: payload => {
        return {
          url: "search",
          method: "POST",
          body: { query: payload },
        }
      },
    }),
    searchByImage: builder.mutation({
      query: payload => {
        return {
          url: "search",
          method: "POST",
          body: { query: payload },
        }
      },
    }),
  }),
})

export const {
  useSearchByTextMutation,
  useSearchByImageMutation,
} = SearchSlice
