import { createSlice } from "@reduxjs/toolkit"

export interface ControlInitialSlice {
  status: string
  selectedMode: string
  query: string
  isSearching: boolean
  images: { id: number, url: string }[]
}

export const ControlInitialSlice: ControlInitialSlice = {
  status: 'idle',
  selectedMode: 'Text mode',
  query: '',
  isSearching: false,
  images: [
    { id: 1, url: 'https://i.pinimg.com/474x/7a/60/da/7a60dac331ad5fcb150635f8d72c94f5.jpg'},
    { id: 2, url: 'https://i.pinimg.com/474x/1f/62/a1/1f62a1ec569564624aac8f2b1a792f97.jpg'},
    { id: 3, url: 'https://i.pinimg.com/474x/66/b1/08/66b1082468790b1a4a345a62538263b5.jpg'},
    { id: 4, url: 'https://i.pinimg.com/474x/d4/f2/39/d4f239ebec8c7a132bd4894543c43e60.jpg'},
    { id: 5, url: 'https://i.pinimg.com/474x/2e/ef/8f/2eef8fa991b75ba997724dc6dfc59cc9.jpg'},
    { id: 6, url: 'https://i.pinimg.com/474x/37/4b/77/374b77076471d3d85b818b85baba16f5.jpg'},
    { id: 7, url: 'https://i.pinimg.com/736x/5a/fe/0b/5afe0b04759f3a6a28e7268e0ef6c6e5.jpg'},
    { id: 8, url: 'https://i.pinimg.com/474x/94/ad/8a/94ad8a70890c28f032d4b54d5904cfe0.jpg'},
    { id: 9, url: 'https://i.pinimg.com/474x/7a/60/da/7a60dac331ad5fcb150635f8d72c94f5.jpg'},
    { id: 10, url: 'https://i.pinimg.com/474x/1f/62/a1/1f62a1ec569564624aac8f2b1a792f97.jpg'},
    { id: 11, url: 'https://i.pinimg.com/474x/66/b1/08/66b1082468790b1a4a345a62538263b5.jpg'},
    { id: 12, url: 'https://i.pinimg.com/474x/d4/f2/39/d4f239ebec8c7a132bd4894543c43e60.jpg'},
    { id: 13, url: 'https://i.pinimg.com/474x/2e/ef/8f/2eef8fa991b75ba997724dc6dfc59cc9.jpg'},
  ]
}

export const ControlSlice = createSlice({
  name: "controlPanel",
  initialState: ControlInitialSlice,
  reducers: {
    setStatus: (state, action) => {
      state.status = action.payload
    },
    setSelectedMode: (state, action) => {
      state.selectedMode = action.payload
    },
    setQuery: (state, action) => {
      state.query = action.payload
    },
    setIsSearching: (state, action) => {
      state.isSearching = action.payload
    },
    setImages: (state, action) => {
      state.images = action.payload
    }
  },
  selectors: {
    getStatus: state => state.status,
    getSelectedMode: state => state.selectedMode,
    getQuery: state => state.query,
    getIsSearching: state => state.isSearching,
    getImages: state => state.images
  },
})

export const {
  setStatus,
  setSelectedMode,
  setQuery,
  setIsSearching,
  setImages,
} = ControlSlice.actions

export const {
  getStatus,
  getSelectedMode,
  getQuery,
  getIsSearching,
  getImages,
} = ControlSlice.selectors
