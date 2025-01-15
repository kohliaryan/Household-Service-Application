export default {
    template: `
    <div class="container mt-5">
        <h1 class="text-center mb-4">All Services</h1>
        <div class="card shadow">
            <div class="card-body">
                <!-- Table for displaying services -->
                <table class="table table-hover table-bordered text-center align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Price (₹)</th>
                            <th>Time Required (mins)</th>
                            <th>Description</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="service in services" :key="service.id">
                            <td>{{ service.id }}</td>
                            <td>{{ service.name }}</td>
                            <td>₹{{ service.price }}</td>
                            <td>{{ service.time_required }} mins</td>
                            <td>{{ service.description }}</td>
                            <td>
                                <router-link :to="'/editService/' + service.id" class="btn btn-primary btn-sm">
                                    Edit
                                </router-link>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-if="loading" class="text-center mt-3">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div v-if="error" class="alert alert-danger mt-3">
                    Failed to load services. Please try again later.
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            services: [], // To store fetched services
            loading: false, // To show/hide the loading spinner
            error: false, // To handle errors
        };
    },
    methods: {
        async fetchServices() {
            this.loading = true; // Show the loading spinner
            this.error = false; // Reset the error state

            try {
                const response = await fetch("http://127.0.0.1:5000/api/services");

                if (!response.ok) {
                    throw new Error("Failed to fetch services");
                }
                const data = await response.json();
                this.services = data; // Populate services data
            } catch (err) {
                console.error(err);
                this.error = true; // Show the error message
            } finally {
                this.loading = false; // Hide the loading spinner
            }
        },
    },
    created() {
        this.fetchServices(); // Fetch services when the component is created
    },
};
