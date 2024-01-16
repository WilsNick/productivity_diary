<!-- src/components/MyForm.vue -->

<template>
  <div>
      <label for="category">Category:</label>
      <select id="category" v-model="selectedCategory" @change="handleCategoryChange">
        <option value="" disabled>Select a category</option>
        <option value="programming">Programming</option>
        <option value="workout">Workout</option>
        <option value="reading">Reading</option>
        <option value="passion_project">Passion Projects</option>
      </select>
      <br>
      <br>
      
      <ProjectForm v-if="showProjects" />

  </div>
</template>

<script>
import { apiService } from "@/services/apiService";
import ProjectForm from "./ProjectForm.vue";

export default {
    data() {
        return {
            selectedCategory: "",
            name_field: "",
            timeSpent: 0,
            showProjects: false,
            existingProjects: [],
            selectedExistingProject: "",
        };
    },
    methods: {
        
        
        handleCategoryChange() {
            // Show/hide the project-related fields based on the selected category
            this.showProjects = this.selectedCategory === "passion_project";
            // If "Passion Projects" is selected, fetch the existing projects
            if (this.showProjects) {
                this.fetchExistingProjects();
            }
        },
        async fetchExistingProjects() {
            try {
                // Fetch the list of existing projects from the server
                const response = await apiService.getExistingProjects();
                // Update the existingProjects array with the fetched data
                this.existingProjects = response.data;
            }
            catch (error) {
                console.error('Error fetching existing projects:', error);
            }
        },
    },
    mounted() {
        // Fetch the list of existing projects when the component is mounted
        this.fetchExistingProjects();
    },
    components: { ProjectForm }
};
</script>

<style scoped>
/* Add some styling if desired */
</style>
