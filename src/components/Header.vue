<template>
  <nav class="app-header">
    <div class="brand">
      <span class="brand-highlight">My</span>Productivity
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/projects" class="nav-link">Projects</router-link>
      <router-link to="/thesis" class="nav-link">Thesis</router-link>
      <router-link to="/books" class="nav-link">Books</router-link>
      <router-link to="/workout" class="nav-link">Workout</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppHeader',
};
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 0 0 8px 8px; /* Adjust border-radius as needed */
}

.brand {
  font-family: 'Pacifico', cursive;
  font-size: 2rem;
  font-weight: bold;
}

.brand-highlight {
  color: #22d3ee;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: 600;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  transition: background 0.3s ease, color 0.3s ease;
}

.nav-link:hover {
  background: #ffffff;
  color: #764ba2;
}
</style>


<!-- 
<style scoped>
  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    background: #3498db; 
    color: #ffffff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 0 0 8px 8px; /* Adjust border-radius as needed */
  }
  

  .brand {
    font-family: 'Arial', sans-serif; 
    font-size: 2rem;
    font-weight: bold;
  }

  .brand-highlight {
    color: #22d3ee;
  }

  .nav-links {
    display: flex;
    gap: 1.5rem;
  }

  .nav-link {
    text-decoration: none;
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 600;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    transition: background 0.3s ease, color 0.3s ease;
  }

  .nav-link:hover {
    background: #ffffff;
    color: #3498db; 
  }
</style> -->



