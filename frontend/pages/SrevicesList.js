import ServicsCard from "../components/ServicsCard.js";

export default {
  template: `
    <div>
      <h1 class="mb-4">Service List</h1>
      
      <!-- Search Box -->
      <div class="mb-4">
        <input 
          type="text" 
          class="form-control" 
          placeholder="Search services by name..." 
          v-model="searchQuery" 
        />
      </div>

      <!-- Services List -->
      <div v-if="filteredServices.length > 0">
        <ServicsCard 
          v-for="service in filteredServices" 
          :key="service.id" 
          :name="service.name" 
          :id="service.id" 
          :price="service.price" 
          :time_required="service.time_required" 
          :description="service.description"> 
        </ServicsCard>
      </div>
      
      <!-- No Results Found -->
      <div v-else>
        <p class="text-danger">No services found matching your search.</p>
      </div>
    </div>
  `,
  data() {
    return {
      services: [], // All services fetched from the backend
      searchQuery: "", // User's search input
    };
  },
  computed: {
    filteredServices() {
      // "Contains" logic: If searchQuery is empty, return all services
      return this.services.filter((service) =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  async mounted() {
    try {
      const res = await fetch(location.origin + "/api/services");
      this.services = await res.json(); // Store fetched services
      console.log("Fetched Services:", this.services); // Debugging
    } catch (error) {
      console.error("Error fetching services:", error); // Handle errors
    }
  },
  components: {
    ServicsCard,
  },
};
