// src/services/apiService.js


const BASE_URL = 'http://localhost:5000'; // Update with your actual backend URL

export const apiService = {

    async getExistingProjects() {
      try {
        const response = await fetch(`${BASE_URL}/get-existing-projects`);
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
    async addProject(project_title) {
      try {
        const response = await fetch(`${BASE_URL}/add-project`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ title: project_title }),  // Wrap the project_title in an object
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
    async resetTable() {
      try {
          const response = await fetch(`${BASE_URL}/reset-table`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
          });

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
      
      
  };
  