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
    { id: 1, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/animals-kaggle/cat/3f3a2aaef2.jpg'},
    { id: 2, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/food/1600003.jpg'},
    { id: 3, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/Landscape/Training+Data/Coast/Coast-Train+(1054).jpeg'},
    { id: 4, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/animals-kaggle/cat/31ae8d36b6.jpg'},
    { id: 5, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/weather/dataset/snow/0897.jpg'},
    { id: 6, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/Landscape/Training+Data/Coast/Coast-Train+(1023).jpeg'},
    { id: 7, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/animals-kaggle/dog/9bd48a19a4.jpg'},
    { id: 8, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/weather/dataset/snow/0861.jpg'},
    { id: 9, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/weather/dataset/rime/4940.jpg'},
    { id: 10, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/animals-kaggle/dog/4df813f7f1.jpg'},
    { id: 11, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/food/1050813.jpg' },
    { id: 12, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/Landscape/Training+Data/Coast/Coast-Train+(101).jpeg' },
    { id: 13, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/Landscape/Testing+Data/Desert/Desert-Test+(10).jpeg' },
    { id: 14, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/human/1748463.jpg' },
    { id: 15, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/animals-kaggle/cat/9fd544a838.jpg' },
    { id: 16, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/animals-kaggle/dog/82a669ccf6.jpg' },
    { id: 17, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/Landscape/Testing+Data/Desert/Desert-Test+(33).jpeg' },
    { id: 18, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/human/1486809.jpg' },
    { id: 19, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/food/101636.jpg' },
    { id: 20, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/Landscape/Testing+Data/Desert/Desert-Test+(35).jpeg' },
    { id: 21, url: 'https://20250307-aws-educate-genai-workshop-bucket.s3.ap-northeast-1.amazonaws.com/photo-gallery/human/261195.jpg' }
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
