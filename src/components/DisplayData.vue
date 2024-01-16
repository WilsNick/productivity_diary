<!-- src/components/DisplayData.vue -->

<template>
  <div>
    <h2>Display Data</h2>
    <label for="categoryFilter">Filter by Category:</label>
    <select id="categoryFilter" v-model="selectedCategory" @change="fetchData">
      <option value="">All</option>
      <option value="programming">Programming</option>
      <option value="workout">Workout</option>
      <option value="reading">Reading</option>
      <option value="passion_project">Passion Project</option>
    </select>

    <button @click="fetchData">Fetch Data</button>

    <ul v-if="data.length">
      <li v-for="item in data" :key="item.id">
        {{ item.text_field_value }} ({{ item.category }}) - Time Spent: {{ item.time_spent }} minutes
      </li>
    </ul>
    <p v-else>No data available</p>
  </div>
</template>

<script>
import { apiService } from "@/services/apiService";

export default {
  data() {
    return {
      data: [],
      selectedCategory: "",
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await apiService.fetchData(this.selectedCategory);

        // Handle the response
        this.data = response.data;

      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Add some styling if desired */
</style>
