<template>
  <div class="pinterest-style-container">
    <!-- 圖片 URL 輸入區塊 -->
    <div id="app">
      <input type="text" v-model="imageUrl" placeholder="Enter Image URL" class="url-input" />
      <button @click="previewImage" :disabled="isLoading">
        {{ isLoading ? "Loading..." : "Preview Image" }}
      </button>
    </div>

    <!-- 預覽區塊 -->
    <div class="main-container">
      <!-- 圖片預覽 -->
      <div v-if="previewedImage" class="image-container">
        <img :src="previewedImage" alt="Previewed Image" class="previewed-image" />
        <button @click="searchByImage" :disabled="isLoading || !previewedImage" class="search-button">
          {{ isLoading ? "Searching..." : "Search by Image" }}
        </button>
      </div>

      <!-- 搜尋結果 -->
      <div class="result-container">
        <!-- Loading 畫面 -->
        <div v-if="isLoading" class="loading-overlay">
          <div class="loading-spinner"></div>
        </div>

        <!-- 錯誤訊息 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- 搜尋結果顯示區塊 -->
        <div class="image-grid">
          <div v-for="(base64Image, index) in searchResults" :key="index" class="image-item">
            <img :src="base64Image" :alt="'Result Image ' + index" />
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      imageUrl: "",
      previewedImage: null,
      isLoading: false,
      errorMessage: "",
      searchResults: [],
      fullResponse: null, // 儲存完整回應
    };
  },
  methods: {
    previewImage() {
      if (this.imageUrl) {
        this.previewedImage = this.imageUrl;
      } else {
        alert("Please enter a valid image URL.");
      }
    },

    async searchByImage() {
      if (!this.previewedImage) {
        alert("Please preview an image first.");
        return;
      }

      this.isLoading = true;
      this.errorMessage = "";
      this.searchResults = [];
      this.fullResponse = null; // 清空前一次的回應

      try {
        const response = await axios.post(
          "https://eijnak1098.execute-api.us-west-2.amazonaws.com/default/EntryFunction",
          {
            search_image_url: this.imageUrl,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        // 儲存完整的 API 回應（格式化 JSON 以便顯示）
        this.fullResponse = JSON.stringify(response.data, null, 2);

        // 確保 `images` 存在並且是物件
        if (response.data.images && typeof response.data.images === "object") {
          this.searchResults = Object.values(response.data.images).map((imageBase64) => {
            return `data:image/jpeg;base64,${imageBase64}`;
          });
        } else {
          console.error("Invalid image data format:", response.data.images);
          this.errorMessage = "Invalid image data format received from server.";
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || error.message || "An error occurred while searching.";
      } finally {
    this.isLoading = false;
  }
},

  },
};
</script>


<style scoped>


.pinterest-style-container {
  height: 100%;  /* Make it take the full height of the page */
  width: 100%;   /* Take full width */
  display: flex;
  justify-content: center;
  align-items: flex-start;  /* Align content to the top */
  padding: 20px;  /* Optional padding to create space around the content */
  background-color: #fff;  /* Set white background */
  box-sizing: border-box;  /* Prevent padding from affecting overall size */
}

.main-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  width: 100%;
  max-width: 1200px;  /* Optional: maximum width to avoid stretching too much */
}

.image-container,
.result-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.url-input-section {
  margin-bottom: 20px;
}

.url-input {
  padding: 10px;
  width: 60%;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  background-color: #e60023;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.previewed-image {
  max-width: 400px;
  height: auto;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-button {
  padding: 10px 20px;
  background-color: #e60023;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.search-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #e60023;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-message {
  color: red;
  margin-top: 10px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
  margin-top: 20px;
}

.image-item {
  width: 150px;
}

.image-item img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

</style>
