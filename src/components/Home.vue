<template>
  <div class="home-page">
    <div class="intro-section">
      <h1>Welcome to Your Productivity Tracker!</h1>
      <p>
        This tool helps you manage various aspects of your life. Choose a category
        below to add data and stay organized.
      </p>
    </div>

    <div class="category-section">
      <h2>Choose a Category to Add Data</h2>
      <label for="category">Category:</label>
      <select id="category" v-model="selectedCategory" @change="handleCategoryChange">
        <option value="" disabled>Select a category</option>
        <option value="thesis">Thesis</option>
        <option value="workout">Workout</option>
        <option value="reading">Reading</option>
        <option value="passion_project">Passion Projects</option>
      </select>
    </div>

    <div class="form-section">
      <ProjectForm v-if="showProjects" />
      <BookForm v-if="showBooks" />
      <ThesisForm v-if="showThesis" />
      <WorkoutForm v-if="showWorkout" />
    </div>
  </div>
</template>

<script>
import ProjectForm from "./Forms/ProjectForm.vue";
import BookForm from "./Forms/BookForm.vue";
import ThesisForm from "./Forms/ThesisForm.vue";
import WorkoutForm from "./Forms/WorkoutForm.vue";
export default {
  name: 'HomePage',
  data() {
    return {
      showProjects: false,
      showBooks: false,
      showThesis: false,
      showWorkout: false,
      selectedCategory: "", // Initialize selectedCategory
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
  },
};
</script>

<style scoped>
.home-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.intro-section {
  text-align: center;
  margin-bottom: 30px;
}

.category-section {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
  margin-right: 10px;
}

select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
