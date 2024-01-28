<!-- src/components/BookForm.vue -->

<template>
  <div class="book-form">
    <div class="form-row">
      <div class="form-column">
        <label for="existingBooks">Select Existing Book:</label>
        <select id="existingBooks" v-model="selectedExistingBook">
          <option value="" disabled>Select an existing book</option>
          <option v-for="book in existingBooks" :key="book.id" :value="book">{{ book }}</option>
        </select>
      </div>
      <div class="form-column">
        <label for="newBook">New Book:</label>
        <div class="new-book-row">
          <input type="text" id="newBook" v-model="newBook" class="large-input" />
          <button @click="addBook" class="small-btn">Add Book</button>
        </div>
      </div>
    </div>

    <div class="form-section">
      <label for="timeSpent">Time Spent (in pages):</label>
      <div class="input-section">
        <input type="number" id="timeSpent" v-model="timeSpent" class="small-input" />
      </div>
    </div>

    <div class="form-section">
      <label for="currentPage">Current Page:</label>
      <div class="input-section">
        <input type="number" id="currentPage" v-model="currentPage" class="small-input" />
      </div>
    </div>

    <div class="form-section" style="text-align: center;">
      <button @click="submit" class="submit-btn">Submit</button>
      <button @click="resetTable" class="reset-table-btn">Reset Table</button>
    </div>

    <div class="form-section" style="text-align: center; margin-top: 1rem;">
      <button @click="getAllSubmissions" class="get-submissions-btn">Get All Submissions</button>
    </div>


    <div v-if="allSubmissions && allSubmissions.length > 0" class="form-section">
      <h3>All Submissions:</h3>
      <ul>
        <li v-for="submission in allSubmissions" :key="submission.id">
          {{ submission.project_name }} - {{ submission.time_spent }} pages - current page {{ submission.current_page }} -
          ({{ submission.submission_date }})
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
      newBook: "",
      timeSpent: 0,
      existingBooks: [],
      selectedExistingBook: "",
      allSubmissions: [],
      currentPage: 0,
    };
  },
  methods: {
    async submit() {
      try {
        if (this.selectedExistingBook) {
          const formData = {
            category: "Books",
            project_name: this.selectedExistingBook,
            time_spent: this.timeSpent,
            current_page: this.currentPage,
          };

          const response = await apiService.submitTime(formData);

          console.log('Response from server:', response);

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
        const response = await apiService.getExistingProjects("Books");

        if (response.projects) {
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
        const dataForm = {
          category: "Books",
          title: this.newBook,
        };
        await apiService.addProject(dataForm);

        await this.fetchExistingBooks();
        const newIndex = this.existingBooks.indexOf(this.newBook);
        this.selectedExistingBook = newIndex !== -1 ? this.existingBooks[newIndex] : '';
      } catch (error) {
        console.error('Error fetching existing projects:', error);
      }
    },

    async resetTable() {
      try {
        await apiService.resetTable("Books");
        console.log('Table reset successful');
        this.fetchExistingBooks();
      } catch (error) {
        console.error('Error resetting table:', error);
      }
    },

    async getAllSubmissions() {
      try {
        const response = await apiService.getAllSubmissions("Books");
        this.allSubmissions = response.submissions;
      } catch (error) {
        console.error('Error fetching all submissions:', error);
      }
    },
  },
  mounted() {
    this.fetchExistingBooks();
  },
};
</script>


<style scoped>
.book-form {
  max-width: 800px;
  margin: auto;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  /* Increased vertical space */
  margin-bottom: 1.5rem;
}

.form-column {
  flex: 1 1 100%;
  max-width: calc(50% - 0.75rem);
  /* Widened columns */
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.new-book-row {
  display: flex;
  gap: .5rem;
}

.form-section {
  margin-bottom: 1.5rem;
  /* Increased vertical space */
}

.label-section {
  margin-top: 1rem;
  /* Increased spacing between label and input field */
}

label {
  font-weight: bold;
}

.input-section {
  width: 100%;
  margin-top: 0.5rem;
  /* Adjusted spacing between label and input field */
}

input,
select,
button {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  cursor: pointer;
  background-color: #007bff;
  /* Matching header color */
  color: white;
  border: none;
  border-radius: 4px;
  padding: 1rem;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
  /* Darker shade on hover */
}

.small-input {
  width: 50%;
  /* Reduced width for smaller inputs */
}

.large-input {
  width: 75%;
  /* Increased width for larger input */
}

.small-btn {
  width: 30%;
  /* Reduced width for smaller button */
}

.submit-btn,
.get-submissions-btn,
.reset-table-btn {
  width: 48%;
  /* Reduced width for all buttons */
  margin: 0.5%;
  /* Adjusted margin for spacing */
  display: inline-block;
  /* Display buttons in the same line */
}

/* Adjusted colors */
.submit-btn {
  background-color: #007bff;
  /* Matching header color */
}

.get-submissions-btn {
  background-color: #007bff;
  /* Matching header color */
}

.reset-table-btn {
  background-color: #dc3545;
  /* Red color for Reset Table */
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li {
  margin-bottom: 1rem;
  /* Increased vertical space */
  background-color: #fff;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}</style>
