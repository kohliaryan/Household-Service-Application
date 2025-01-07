import ServicsCard from "../components/ServicsCard.js";

export default {
  template: `
    <div>
      <h1> Service List </h1>
      <ServicsCard 
        v-for="service in services" 
        :key="service.id" 
        :name="service.name" 
        :id="service.id" 
        :price="service.price" 
        :time_required="service.time_required" 
        :description="service.description"> 
      </ServicsCard>
    </div>
  `,
  data() {
    return {
      services: [],
    };
  },
  async mounted() {
    try {
      const res = await fetch(location.origin + "/api/services", {
        headers: {
          Authorization: this.$store.state.auth_token,
        },
      });
      this.services = await res.json();
      console.log(this.services);
    } catch (error) {
      console.error("Error fetching services:", error);
    }
  },
  components: {
    ServicsCard,
  },
};
