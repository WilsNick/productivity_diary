<!-- src/components/BookForm.vue -->

<template>
  <div>
      <!-- Show existing projects dropdown only if the selected category is "passion_project" -->
      <label for="existingBooks">Select Existing Book:</label>
      <select id="existingBooks" v-model="selectedExistingBook">
        <option value="" disabled>Select an existing book</option>
        <option v-for="book in existingBooks" :key="book.id" :value="book">{{ book }}</option>
      </select>

      <label for="NewBook">New book:</label>
      <input type="text" id="NewBook" v-model="NewBook" />

      <button @click="addBook">Add book</button>

      <button @click="resetTable">Reset Table</button>

      <br><br>

      <label for="timeSpent">Time Spent (in pages):</label>
      <input type="number" id="timeSpent" v-model="timeSpent" />

      <br><br>

      <label for="currentPage">Current page:</label>
      <input type="number" id="currentPage" v-model="currentPage" />

      <br><br>
      <button @click="submit">Submit</button>

      <br><br>
      <button @click="getAllSubmissions">Get All Submissions</button>

    <!-- Display the fetched submissions -->
    <div v-if="allSubmissions && allSubmissions.length > 0">
      <h3>All Submissions:</h3>
      <ul>
        <li v-for="submission in allSubmissions" :key="submission.id">
          {{ submission.project_name }} - {{ submission.time_spent }} pages - current page {{ submission.current_page }} - ({{ submission.submission_date }})
        </li>
      </ul>
    </div>
  </div>

</template>

<script>
import { apiService } from "@/services/apiService";

export default {
  data() {
    return {
      NewBook:"",
      timeSpent: 0,
      existingBooks: [],
      selectedExistingBook: "",
      allSubmissions: [], 
      currentPage:0,

    };
  },
  methods: {
    
    async submit() {
      try {
        // console.log(this.selectedExistingBook)
        // Check if selectedExistingProject is not empty and a number
        if (this.selectedExistingBook) {
          const formData = {
            category: "Books",
            project_name: this.selectedExistingBook,
            time_spent: this.timeSpent,
            current_page: this.currentPage
          };

          // Call the API endpoint to submit the time data
          const response = await apiService.submitTime(formData);

          console.log('Response from server:', response);

          // Reset the form fields to their initial state
          this.timeSpent = 0;
          this.currentPage = 0;
        } else {
          console.error('Invalid selectedExistingBook value.');
          console.error(this.selectedExistingBook);
        }
      } catch (error) {
        console.error('Error submitting time:', error);
      }
    },

    async fetchExistingBooks() {
      try {

        // Fetch the list of existing projects from the server
        const response = await apiService.getExistingProjects("Books");

        // Ensure that the 'projects' property exists in the response
        if (response.projects) {
          // Extract the 'title' from each project and update the existingProjects array
          this.existingBooks = response.projects.map(book => book.title);
          console.log(this.existingBooks);
        } else {
          console.error('Error: Unexpected response format from the server.');
        }

      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },


    async addBook() {
      try {
        const data_form = {
          category: "Books",
          title: this.NewBook
        }
        // Fetch the list of existing projects from the server
        await apiService.addProject(data_form);

        // Update the existingProjects array with the fetched data
        await this.fetchExistingBooks()
        const newIndex = this.existingBooks.indexOf(this.NewBook);

        // Set selectedExistingProject to the newly added project title
        this.selectedExistingBook = newIndex !== -1 ? this.existingBooks[newIndex] : '';

        // this.selectedExistingProject = this.NewProject;

      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },

    async resetTable() {
        try {
            // Call the resetTable method from your apiService
            await apiService.resetTable("Books");
            console.log('Table reset successful');

            // After resetting the table, fetch the updated list of existing projects
            this.fetchExistingBooks();
        } catch (error) {
            console.error('Error resetting table:', error);
        }
    },

    async getAllSubmissions() {
        try {

            // Fetch all submissions from the server
            const response = await apiService.getAllSubmissions("Books");

            // Update the allSubmissions array with the fetched data
            this.allSubmissions = response.submissions;

        } catch (error) {
            console.error('Error fetching all submissions:', error);
        }
    },
  },
  mounted() {
    // Fetch the list of existing projects when the component is mounted
    this.fetchExistingBooks();
  },
};
</script>

<style scoped>
/* Add some styling if desired */
</style>
