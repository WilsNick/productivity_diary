<!-- src/components/MyForm.vue -->

<template>
  <div>
    <form @submit.prevent="submitForm">
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
      <!-- Show existing projects dropdown only if the selected category is "passion_project" -->
      <label v-if="showProjects" for="existingProjects">Select Existing Project:</label>
      <select v-if="showProjects" id="existingProjects" v-model="selectedExistingProject">
        <option value="" disabled>Select an existing project</option>
        <option v-for="project in existingProjects" :key="project.id" :value="project.id">{{ project.name }}</option>
      </select>
      <br>
      <br>

      <!-- Show text field for all categories -->
      <label for="textField">Text Field:</label>
      <input type="text" id="textField" v-model="name_field" />
      <br>
      <br>

      

      <!-- Show time spent field only if the selected category is "passion_project" -->
      <label v-if="showProjects" for="timeSpent">Time Spent (in hours):</label>
      <input v-if="showProjects" type="number" id="timeSpent" v-model="timeSpent" />
      <br>
      <br>

      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import { apiService } from "@/services/apiService";

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
    async submitForm() {
      try {
        console.log("Form submitted with value:", this.name_field, "and category:", this.selectedCategory, "and time spent:", this.timeSpent);

        // Depending on whether a new or existing project is selected, handle accordingly
        if (this.selectedExistingProject) {
          // Handle existing project submission
          const formData = {
            text: this.name_field,
            category: this.selectedCategory,
            timeSpent: this.timeSpent,
            existingProjectId: this.selectedExistingProject,
          };

          const response = await apiService.submitFormData(formData);
          console.log('Response from server:', response);

        } else {
          // Handle new project submission
          const formData = {
            text: this.name_field,
            category: this.selectedCategory,
            timeSpent: this.timeSpent,
          };

          const response = await apiService.submitFormData(formData);
          console.log('Response from server:', response);
        }

        // Reset the form fields to their initial state
        this.name_field = "";
        this.selectedCategory = "";
        this.timeSpent = 0;
        this.showProjects = false;
        this.selectedExistingProject = "";

        // After submission, fetch the updated list of existing projects
        this.fetchExistingProjects();

      } catch (error) {
        console.error('Error submitting form:', error);
        // Handle the error (e.g., show an error message to the user)
      }
    },
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

      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },
  },
  mounted() {
    // Fetch the list of existing projects when the component is mounted
    this.fetchExistingProjects();
  },
};
</script>

<style scoped>
/* Add some styling if desired */
</style>
