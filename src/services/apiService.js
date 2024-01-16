// src/services/apiService.js


const BASE_URL = 'http://localhost:5000'; // Update with your actual backend URL

export const apiService = {
    async submitFormData(formData) {
      try {
        const response = await fetch(`${BASE_URL}/submit-form`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });
  
        if (!response.ok) {
          throw new Error('Failed to submit form data');
        }
  
        return response.json();
      } catch (error) {
        console.error('API error:', error.message);
        throw error; // Re-throw the error to propagate it to the component
      }
    },
  
    async removeAllData() {
      try {
        const response = await fetch(`${BASE_URL}/remove-all-data`, {
          method: 'POST',
        });
  
        if (!response.ok) {
          throw new Error('Failed to remove all data');
        }
  
        return response.json();
      } catch (error) {
        console.error('API error:', error.message);
        throw error; // Re-throw the error to propagate it to the component
      }
    },

    async fetchData(category = "") {
        try {
          const url = category ? `${BASE_URL}/get-data?category=${category}` : `${BASE_URL}/get-data`;
          const response = await fetch(url);
    
          if (!response.ok) {
            throw new Error(`Failed to fetch data: ${response.statusText}`);
          }
    
          return response.json();
        } catch (error) {
          console.error('API error:', error.message);
          throw error; // Re-throw the error to propagate it to the component
        }
    },
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
      
  };
  