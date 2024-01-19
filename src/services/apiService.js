// src/services/apiService.js


const BASE_URL = 'http://localhost:5000'; // Update with your actual backend URL

export const apiService = {

    async getExistingProjects(category) {
      try {
        const response = await fetch(`${BASE_URL}/get-existing-projects?category=${category}`);
        const data = await response.json();
  
        if (response.ok) {
          return data;
        } else {
          throw new Error(`Failed to get existing projects: ${data.error}`);
        }
      } catch (error) {
        throw new Error(`Error getting existing projects: ${error.message}`);
      }
    },

    async getAllSubmissions(category) {
      try {
          const response = await fetch(`${BASE_URL}/get-all-submissions?category=${category}`);
          const data = await response.json();

          if (response.ok) {
              return data;
          } else {
              throw new Error(`Failed to get all submissions: ${data.error}`);
          }
      } catch (error) {
          throw new Error(`Error getting all submissions: ${error.message}`);
      }
    },

    async addProject(data_form) {
      try {
        const response = await fetch(`${BASE_URL}/add-project`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data_form),  // Wrap the project_title in an object
        });
        const data = await response.json();
    
        if (response.ok) {
          return data;
        } else {
          throw new Error(`Failed to add project: ${data.error}`);
        }
      } catch (error) {
        throw new Error(`Error adding project: ${error.message}`);
      }
    },
    async resetTable(category) {
      try {
          const response = await fetch(`${BASE_URL}/reset-table?category=${category}`);

          const data = await response.json();

          if (response.ok) {
              return data;
          } else {
              throw new Error(`Failed to reset table: ${data.error}`);
          }
      } catch (error) {
          throw new Error(`Error resetting table: ${error.message}`);
      }
    },
    async submitTime(formData) {
      try {
          const response = await fetch(`${BASE_URL}/submit-time`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(formData),
          });

          const data = await response.json();

          if (response.ok) {
              return data;
          } else {
              throw new Error(`Failed to submit time: ${data.error}`);
          }
      } catch (error) {
          throw new Error(`Error submitting time: ${error.message}`);
      }
    },
      
      
  };
  