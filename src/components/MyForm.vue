<!-- src/components/MyForm.vue -->

<template>
  <div>
      <label for="category">Category:</label>
      <select id="category" v-model="selectedCategory" @change="handleCategoryChange">
        <option value="" disabled>Select a category</option>
        <option value="thesis">Thesis</option>
        <option value="workout">Workout</option>
        <option value="reading">Reading</option>
        <option value="passion_project">Passion Projects</option>
      </select>
      <br>
      <br>
      
      <ProjectForm v-if="showProjects" />
      <BookForm v-if="showBooks" />
      <ThesisForm v-if="showThesis" />
      <WorkoutForm v-if="showWorkout" />

  </div>
</template>

<script>
import ProjectForm from "./ProjectForm.vue";
import BookForm from "./BookForm.vue";
import ThesisForm from "./ThesisForm.vue";
import WorkoutForm from "./WorkoutForm.vue";

export default {
    data() {
        return {
            showProjects: false,
            showBooks: false,
            showThesis: false,
            showWorkout: false,
        };
    },
    methods: {
        
        
        handleCategoryChange() {
            // Show/hide the project-related fields based on the selected category
            this.showProjects = this.selectedCategory === "passion_project";
            this.showBooks = this.selectedCategory === "reading";
            this.showThesis = this.selectedCategory === "thesis";
            this.showWorkout = this.selectedCategory === "workout";

        },
    },
    components: { 
        ProjectForm,
        BookForm,
        ThesisForm,
        WorkoutForm,
    }
};
</script>

<style scoped>
/* Add some styling if desired */
</style>
