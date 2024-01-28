import { apiService } from "@/services/apiService";

export const projectsPageMethods = {

    // Handle the change in draggable columns
    async handleChange(event) {
        console.log('Column changed:', event);

        if (event.added || event.moved) {
            // Update status for items in different lists
            for (const item of this.list1) {
                item.status = "Todo";
            }
            for (const item of this.list2) {
                item.status = "In Progress";
            }
            for (const item of this.list3) {
                item.status = "Done";
            }
            // Combine lists and update server
            let combinedList = this.list1.concat(this.list2, this.list3);
            const form = {
                items: combinedList,
                project_id: this.selectedProject.id,
            };
            await apiService.updateTodo(form);
            await this.selectProject(this.selectedProject.id);
        }
    },

    // Fetch all submissions from the server
    async getAllSubmissions() {
        try {
            const response = await apiService.getAllSubmissions("Projects");
            console.log(response);
            // Update allSubmissions array with fetched data
            this.allSubmissions = response.submissions;

        } catch (error) {
            console.error('Error fetching all submissions:', error);
        }
    },

    // Fetch existing projects from the server
    async fetchExistingProjects() {
        try {
            const response = await apiService.getExistingProjects("Projects");
            if (response.projects) {
                this.existingProjects = response.projects;
            } else {
                console.error('Error: Unexpected response format from the server.');
            }
        } catch (error) {
            console.error('Error fetching existing projects:', error);
        }
    },

    // Toggle the display of the project form
    toggleProjectForm() {
        this.showProjects = !this.showProjects;
    },

    // Select a project and fetch its details
    async selectProject(project) {
        this.selectedProject.id = project;
        try {
            const response = await apiService.getProjectInfo(project);
            if (response.project) {
                let project = response.project;
                this.selectedProject.description = project.description;
                this.selectedProject.title = project.title;
                let todos = project.todos;
                this.list1 = [];
                this.list2 = [];
                this.list3 = [];
                this.list4 = [];
                for (const todo of todos) {
                    if (todo.status === "Todo" && !this.list1.some(item => item.id === todo.id)) {
                        this.list1.push(todo);
                    } else if (todo.status === "In Progress" && !this.list2.some(item => item.id === todo.id)) {
                        this.list2.push(todo);
                    } else if (todo.status === "Done" && !this.list3.some(item => item.id === todo.id)) {
                        this.list3.push(todo);
                    }
                }
                const response2 = await apiService.getTimeSpent(project.title);
                this.selectedProject.totalTimeSpent = response2.total_time_spent;

            } else {
                console.error('Error: Unexpected response format from the server.');
            }
        } catch (error) {
            console.error('Error fetching existing projects:', error);
        }
    },

    // Toggle the editing mode for a project
    toggleEditing() {
        if (this.isEditing) {
            // If in editing mode, save the changes directly
            this.saveProject();
        } else {
            // If not in editing mode, start editing
            this.editedProject = {
                id: this.selectedProject.id,
                title: this.selectedProject.title,
                description: this.selectedProject.description,
            };
        }
        // Toggle the editing mode
        this.isEditing = !this.isEditing;
    },

    // Cancel the current editing operation
    cancelEditing() {
        this.editedProject = {};
        this.isEditing = false;
    },

    // Save the changes made to a project
    async saveProject() {
        try {
            const response = await apiService.updateProject(this.editedProject);
            console.log('Response from server:', response);
            await this.fetchExistingProjects();

            await this.selectProject(this.editedProject.id);
            this.isEditing = false;
            this.editedProject = {
                id: null,
                title: '',
                description: '',
            };
        } catch (error) {
            console.error('Error updating project:', error);
        }
    },

    // Start the process of adding an item to a list
    startAddingItem(list) {
        this.addingItem = list;
        this.newItemTitle = '';
        this.$nextTick(() => this.$refs.newItemInput.focus());
    },

    // Add a new item to the selected list
    async addItemToList(list) {
        if (this.newItemTitle.trim() !== '') {
            let status = "";
            if (list === this.list1) {
                status = "Todo";
            } else if (list === this.list2) {
                status = "In Progress";
            } else if (list === this.list3) {
                status = "Done";
            }
            const newItem = {
                project_id: this.selectedProject.id,
                status: status,
                task: this.newItemTitle.trim(),
            };
            const response = await apiService.addTodo(newItem);

            list.push(response);
            await this.selectProject(this.selectedProject.id);
        }
        this.addingItem = null;
        this.newItemTitle = '';
    },

    // Start the process of editing an item in a list
    startEditingItem(list, index) {
        this.editingItem = { list, index };
        this.editedItemTitle = list[index].task;
        this.$nextTick(() => this.$refs.editItemInput && this.$refs.editItemInput.focus());
    },

    // Save the changes made to an item in a list
    async saveEditedItem() {
        if (this.editedItemTitle.trim() !== '') {
            this.editingItem.list[this.editingItem.index].task = this.editedItemTitle;
            await apiService.updatedSingleTodo(this.editingItem.list[this.editingItem.index]);

            this.editingItem = null;
            this.editedItemTitle = '';
        }
    },
};
